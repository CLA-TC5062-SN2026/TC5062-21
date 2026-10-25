"""Aplicación ASGI. Arranque: uvicorn backend.app.main:app --host 127.0.0.1."""
import logging
import re

from fastapi import FastAPI, Request
from sqlalchemy import create_engine, text
from sqlalchemy.exc import DataError, IntegrityError, OperationalError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from .config import Settings
from .contract import METHODS, SPEC, request_data
from .errors import APIError
from .models import Usuario
from .security import authenticate
from .services import Service

logger = logging.getLogger("equipo21")
settings = Settings.from_env()
engine = create_engine(settings.database_url, pool_pre_ping=True)
app = FastAPI(title=SPEC["info"]["title"], docs_url="/docs", redoc_url="/redoc")
app.openapi = lambda: SPEC

ROUTES = []
for path, item in SPEC["paths"].items():
    for method, operation in item.items():
        if method not in METHODS: continue
        expression = re.sub(r"\{[^}]+\}", "[^/]+", "/api" + path)
        ROUTES.append((re.compile("^" + expression + "$"), method.upper(), operation))


def error_response(error):
    headers = {"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff"}
    if error.status == 401: headers["WWW-Authenticate"] = "Bearer"
    return JSONResponse(error.body, status_code=error.status, headers=headers)


@app.middleware("http")
async def transaction_and_security(request, call_next):
    operation = next((op for pattern, method, op in ROUTES
        if request.method == method and pattern.fullmatch(request.url.path)), None)
    if operation is None:
        return await call_next(request)
    try:
        with Session(engine, expire_on_commit=False) as db:
            with db.begin():
                # Un único orden de bloqueo evita carreras en último administrador,
                # unicidad entre propuestas/relaciones y aprobación revalidada.
                # Adecuado a la carga académica; su capacidad se debe medir antes de escalar.
                if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
                    await run_in_threadpool(db.execute, text("SELECT pg_advisory_xact_lock(506221)"))
                user, session = None, None
                if operation.get("security", SPEC.get("security")):
                    user, session = await run_in_threadpool(authenticate, db, request.headers.get("authorization"), settings)
                    roles = operation.get("x-roles", [])
                    if roles and user.rol not in roles:
                        raise APIError(403, "SIN_PERMISO", "El rol no tiene permiso para esta operación.")
                request.state.service = Service(db, user, session, settings)
                response = await call_next(request)
                if response.status_code >= 400:
                    db.rollback()
                # La confirmación ocurre antes de entregar cabeceras al cliente.
            response.headers["Cache-Control"] = "no-store"
            response.headers["X-Content-Type-Options"] = "nosniff"
            return response
    except APIError as exc:
        return error_response(exc)
    except IntegrityError:
        return error_response(APIError(409, "CONFLICTO_INTEGRIDAD", "La operación entra en conflicto con datos existentes o restricciones del dominio."))
    except DataError:
        return error_response(APIError(422, "DATO_INVALIDO", "Un dato excede los límites del almacenamiento."))
    except OperationalError:
        return error_response(APIError(503, "BASE_NO_DISPONIBLE", "La base de datos no está disponible."))
    except Exception:
        # No registrar cuerpo, Authorization, SQL parametrizado ni valores sensibles.
        logger.error("Fallo interno en %s %s", request.method, request.url.path)
        return error_response(APIError(500, "ERROR_INTERNO", "No fue posible completar la operación."))


@app.exception_handler(APIError)
async def api_error_handler(request, error):
    return error_response(error)


def endpoint_factory(path, item, operation):
    async def endpoint(request: Request):
        p, q, b = await request_data(request, item, operation)
        data = await run_in_threadpool(request.state.service.dispatch, operation["operationId"], p, q, b)
        status = next(int(code) for code in operation["responses"] if code.startswith("2"))
        if operation["operationId"] == "cargarDemostracion": status = 201 if data["creada"] else 200
        headers = {}
        if status == 201:
            base = request.url.path
            if "entradaBitacoraId" in data: location = "/api/v1/entradas-bitacora/" + data["entradaBitacoraId"]
            elif operation["operationId"] == "iniciarSesion": location = "/api/v1/sesiones/actual"
            elif operation["operationId"] == "registrarUsuario": location = "/api/v1/usuarios/" + data["id"]
            elif operation["operationId"] == "restablecerContrasena": location = "/api/v1/entradas-bitacora/" + data["id"]
            elif operation["operationId"] == "cargarDemostracion": location = base
            else: location = base + "/" + data["id"]
            headers["Location"] = location
        return JSONResponse(data, status_code=status, headers=headers)
    endpoint.__name__ = operation["operationId"]
    return endpoint


for path, item in SPEC["paths"].items():
    for method, operation in item.items():
        if method in METHODS:
            app.add_api_route("/api" + path, endpoint_factory(path, item, operation),
                              methods=[method.upper()], name=operation["operationId"], include_in_schema=False)
