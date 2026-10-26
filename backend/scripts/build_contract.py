"""Consolida los insumos originales conservados; no modifica sus bytes."""
import copy
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SOURCES = ROOT / "S05_S06_A1/insumos"


def ref(name):
    return {"$ref": f"#/components/schemas/{name}"}


def build():
    source = yaml.safe_load((SOURCES / "gregorio/openapi.yaml").read_text())
    spec = copy.deepcopy(source)
    spec["info"] = {
        "title": "Plataforma de Arquitectura Empresarial — Equipo 21",
        "version": "2.0.0",
        "description": "Contrato consolidado de Gregorio Escobedo, Jean Paul Lozano y Liciel. "
        "Decisiones técnicas documentadas en diferencias_diseno.md. "
        "SRS canónico: insumos/SRS_equipo.md, 19 RF y 56 criterios. "
        "CRUD y dominio bajo /api/v1; autenticación académica bajo /api/auth. "
        "El registro público crea únicamente cuentas Consulta; los roles los asigna un Administrador. "
        "Las sesiones JWT se comprueban en PostgreSQL, vencen en un máximo de 8 horas o 30 minutos de inactividad. "
        "Toda escritura de negocio y su bitácora se confirman en una transacción; no hay eliminación física del dominio.",
        "contact": {"name": "Equipo 21 — TC5062"},
    }
    spec["servers"] = [{"url": "/api", "description": "Mismo origen; desarrollo http://127.0.0.1:8000/api. HTTPS en despliegue."}]
    spec["security"] = [{"BearerAuth": []}]
    spec["components"]["securitySchemes"] = {"BearerAuth": {
        "type": "http", "scheme": "bearer", "bearerFormat": "JWT",
        "description": "JWT HS256 con sub, sid, jti, iat, exp, iss y aud; cuenta activa y sesión vigente verificadas en servidor.",
    }}
    spec["x-source-documents"] = ["insumos/gregorio", "insumos/jean_paul", "insumos/liciel", "insumos/SRS_equipo.md"]
    # La descripción anterior queda preservada en los insumos, no como promesa incompatible.
    spec.pop("x-design-rules", None)
    spec["paths"] = {"/v1" + path: op for path, op in spec["paths"].items()}
    schemas = spec["components"]["schemas"]
    schemas["NombreCatalogo"]["maxLength"] = 120
    schemas["OpcionCampoEscritura"]["properties"]["etiqueta"]["maxLength"] = 120
    for name in ("TipoRelacionAlta", "TipoRelacionCambio", "TipoRelacion"):
        schemas[name]["properties"]["nombre"]["maxLength"] = 120
        schemas[name]["properties"]["descripcion"]["maxLength"] = 10000
    schemas["ValorCampo"]["description"] += " El campo base Nombre admite hasta 500 caracteres."
    email = {"type": "string", "format": "email", "maxLength": 254}
    password = {"type": "string", "minLength": 10, "maxLength": 72, "format": "password", "writeOnly": True,
                "description": "Entre 10 caracteres y 72 bytes UTF-8; bcrypt rechaza entradas mayores, sin truncarlas."}
    schemas["Credenciales"] = {"type": "object", "additionalProperties": False,
        "properties": {"correo": email, "contrasena": {"type": "string", "minLength": 1, "maxLength": 72, "writeOnly": True}},
        "required": ["correo", "contrasena"]}
    schemas["RegistroUsuario"] = {"type": "object", "additionalProperties": False,
        "properties": {"correo": email, "nombre": {"type": "string", "minLength": 1, "maxLength": 120, "pattern": r"\S"}, "contrasena": password},
        "required": ["correo", "nombre", "contrasena"]}
    user = schemas["Usuario"]
    user["properties"].pop("identificadorAcceso")
    user["properties"].update(correo=email, nombre={"type": "string", "minLength": 1, "maxLength": 120})
    user["required"] = ["id", "correo", "nombre", "rol", "activo", "capasEditables"]
    alta = schemas["UsuarioAlta"]
    alta["properties"].pop("identificadorAcceso")
    alta["properties"].update(correo=email, nombre=schemas["RegistroUsuario"]["properties"]["nombre"], contrasenaInicial=password)
    alta["required"] = ["correo", "nombre", "contrasenaInicial", "rol"]
    alta["description"] = "Alta administrativa; capasEditables solo para Editor. Nunca devuelve contraseñas ni hashes."
    schemas["RestablecimientoContrasena"]["properties"]["nuevaContrasena"] = password
    schemas["Salud"] = {"type": "object", "additionalProperties": False,
                        "properties": {"estado": {"type": "string", "enum": ["ok"]}}, "required": ["estado"]}

    def op(operation_id, summary, request_schema, response_schema, status, criteria, public=False):
        value = {"operationId": operation_id, "tags": ["Autenticación"], "summary": summary,
            "description": summary + ". JSON; errores sin credenciales ni trazas internas.",
            "x-acceptance-criteria": criteria,
            "x-roles": [] if public else ["Administrador", "Editor", "Consulta"],
            "responses": {str(status): {"description": "Operación completada", "content": {"application/json": {"schema": ref(response_schema)}}},
                "400": {"$ref": "#/components/responses/400"}, "401": {"$ref": "#/components/responses/401"},
                "409": {"$ref": "#/components/responses/409"}, "422": {"$ref": "#/components/responses/422"},
                "500": {"$ref": "#/components/responses/500"}}}
        if public: value["security"] = []
        if request_schema:
            value["requestBody"] = {"required": True, "content": {"application/json": {"schema": ref(request_schema)}}}
        return value

    spec["tags"].append({"name": "Autenticación", "description": "Extensión académica S05-S06-A2"})
    spec["paths"]["/auth/register"] = {"post": op("registrarUsuario", "Registrar cuenta con rol Consulta", "RegistroUsuario", "Usuario", 201, ["RF-02-AC-1"], True)}
    spec["paths"]["/auth/register"]["post"]["x-academic-extension"] = "Alta pública de mínimo privilegio exigida por S05-S06-A2; amplía RF-02 sin atribuir aprobación al cliente."
    spec["paths"]["/auth/login"] = {"post": op("autenticarUsuario", "Autenticar correo y contraseña", "Credenciales", "TokenSesion", 200, ["RF-01-AC-1", "RF-01-AC-2"], True)}
    spec["paths"]["/auth/me"] = {"get": op("consultarPerfil", "Consultar usuario autenticado", None, "Usuario", 200, ["RF-01-AC-2", "RF-02-AC-2"])}
    spec["paths"]["/v1/tipos-elemento/{tipoId}/campos/{campoId}"]["get"] = op("consultarCampo", "Consultar definición de campo", None, "Campo", 200, ["RF-05-AC-1"])
    spec["paths"]["/salud"] = {"get": {"operationId": "consultarSalud", "summary": "Comprobar disponibilidad de PostgreSQL", "description": "No expone configuración ni secretos.", "tags": ["Autenticación"], "security": [],
        "responses": {"200": {"description": "Disponible", "content": {"application/json": {"schema": ref("Salud")}}}, "503": {"description": "No disponible", "content": {"application/json": {"schema": ref("Error")}}}}}}
    # Corrige el patrón doblemente escapado hallado en el contrato individual.
    def fix(value):
        if isinstance(value, dict):
            if value.get("pattern") == r"\\S": value["pattern"] = r"\S"
            for v in value.values(): fix(v)
        elif isinstance(value, list):
            for v in value: fix(v)
    fix(spec)
    for path, item in spec["paths"].items():
        for method, operation in item.items():
            if method not in ("get", "post", "put", "patch", "delete"): continue
            if operation.get("security", spec["security"]):
                operation["security"] = [{"BearerAuth": []}]
                operation["responses"].setdefault("401", {"$ref": "#/components/responses/401"})
                operation["responses"].setdefault("403", {"$ref": "#/components/responses/403"})
            if "requestBody" in operation:
                operation["responses"]["415"] = {"description": "Content-Type debe ser application/json", "content": {"application/json": {"schema": ref("Error")}}}
                operation["responses"]["413"] = {"description": "El cuerpo excede 1 MiB", "content": {"application/json": {"schema": ref("Error")}}}
            operation["responses"].setdefault("422", {"$ref": "#/components/responses/422"})
            operation["responses"].setdefault("503", {"description": "Base de datos no disponible", "content": {"application/json": {"schema": ref("Error")}}})
    dest = ROOT / "S05_S06_A1/openapi_equipo.yaml"
    dest.write_text(yaml.safe_dump(spec, allow_unicode=True, sort_keys=False, width=110))
    summary = []
    for who in ("gregorio", "jean_paul", "liciel"):
        file = next((SOURCES / who).glob("openapi.*"))
        s = yaml.safe_load(file.read_text())
        operations = [{"metodo": m.upper(), "ruta": p, "operationId": o["operationId"]}
            for p,i in s["paths"].items() for m,o in i.items() if m in ("get","post","put","patch","delete")]
        summary.append({"integrante": who, "version": s["info"]["version"], "operaciones": operations})
    (ROOT / "S05_S06_A1/insumos/comparacion_operaciones.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2)+"\n")
    print(f"Contrato: {sum(1 for item in spec['paths'].values() for method in item if method in ('get','post','put','patch','delete'))} operaciones")


if __name__ == "__main__":
    build()
