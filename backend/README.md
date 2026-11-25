# Backend — Equipo 21

FastAPI, SQLAlchemy y PostgreSQL 17. El backend principal incorpora la refactorización auditada de S09; `S09_A1/codigo/` permanece como evidencia histórica. El contrato canónico es `../S05_S06_A1/openapi_equipo.yaml` y `../postman/specs/openapi.yaml` enlaza a él.

## Preparación y arranque

La [guía completa de la raíz](../README.md#instalación-y-ejecución-local) incluye clonado, requisitos, variables, frontend y contenedores. Desde la raíz, en macOS con Python 3.12 y PostgreSQL 17 con ICU:

```sh
python3 scripts/configurar_entorno.py
python3.12 -m venv .venv
.venv/bin/python -m pip install -r backend/requirements-quality.lock.txt
.venv/bin/python backend/scripts/setup_local.py
.venv/bin/python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

`setup_local.py` utiliza `PG_BIN` o `/opt/homebrew/opt/postgresql@17/bin`, crea un clúster privado en `.local/postgres` y escucha en el puerto 55432. El puerto debe estar libre. Conserva datos al repetirse y no modifica un servicio PostgreSQL global.

Las cuentas ficticias se guardan en `.local/demo_credentials.json` con permisos restringidos. Con la API iniciada, ejecutar en otra terminal `.venv/bin/python backend/scripts/prepare_frontend_demo.py` para preparar la muestra completa. Los archivos `.env` y `.local/` están ignorados por Git.

## API y seguridad

- Swagger: `http://127.0.0.1:8000/docs`.
- Base de datos: `GET /api/salud`.
- Registro público: `POST /api/auth/register`, siempre crea Consulta.
- Login: `POST /api/auth/login`, devuelve `accessToken`.
- Perfil: `GET /api/auth/me`, con Bearer token.
- Cierre individual: `DELETE /api/v1/sesiones/actual`.
- Dominio: `/api/v1/...`, protegido por sesión, rol y capa según operación.

`DATABASE_URL` debe usar `postgresql+psycopg`. `JWT_SECRET` es obligatorio, aleatorio y de al menos 32 bytes. `JWT_EXPIRATION` admite 1–28800 segundos y tiene un máximo adicional de 30 minutos de inactividad. Un cambio de rol, desactivación o restablecimiento revoca las sesiones de la cuenta; el cierre individual conserva otras sesiones.

El Administrador administra configuración y cuentas. El Editor escribe solo en capas asignadas. Consulta lee. La baja de un elemento es lógica mediante DELETE; su reactivación usa PATCH con `estado=activo`. La carga de demostración usa PUT. Ver el contrato para cuerpos y códigos exactos.

## Verificación

```sh
.venv/bin/python -m pytest backend/tests -q
postman spec lint postman/specs/openapi.yaml --issueType=syntax --no-report-events
```

La suite usa exclusivamente `arquitectura21_test` en el clúster de desarrollo y reconstruye su esquema. Requiere permiso para crear esa base. No debe apuntarse a producción ni ejecutarse simultáneamente con la medición de consultas de S09.

S11: 88 pruebas aprobadas y una advertencia Starlette/httpx. La [matriz](../S11_A1/matriz_trazabilidad.md) distingue operaciones probadas, criterios sin prueba específica e interfaz pendiente. Los conteos no representan cobertura de código ni cumplimiento de todos los RNF.

## Organización

- `app/main.py`: rutas, transacción y seguridad.
- `app/contract.py`: contrato y validación de entradas.
- `app/security.py`: hash, JWT y sesiones.
- `app/services.py`: servicios, permisos por capa y bitácora.
- `app/value_rules.py`: reglas de valores independientes de persistencia.
- `app/pagination.py`: paginación SQL.
- `app/models.py`: modelo y restricciones.
- `tests/`: integración, regresión, reglas y aceptación S11.
