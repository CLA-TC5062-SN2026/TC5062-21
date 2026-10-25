"""Lectura del contrato consolidado y validación de solicitudes."""
import copy
import json
from pathlib import Path

import yaml
from jsonschema import Draft4Validator, FormatChecker

from .errors import APIError

ROOT = Path(__file__).resolve().parents[2]
SPEC = yaml.safe_load((ROOT / "S05_S06_A1/openapi_equipo.yaml").read_text())
METHODS = {"get", "post", "put", "patch", "delete"}


def json_schema(value):
    """OpenAPI 3.0 nullable se traduce para JSON Schema Draft 4."""
    value = copy.deepcopy(value)
    if isinstance(value, dict):
        nullable = value.pop("nullable", False)
        value = {k: json_schema(v) for k, v in value.items()}
        if nullable:
            if "$ref" in value: return {"anyOf": [value, {"type": "null"}]}
            if "type" in value: value["type"] = [value["type"], "null"]
        return value
    if isinstance(value, list): return [json_schema(v) for v in value]
    return value


VALIDATION_SPEC = json_schema(SPEC)


def resolve(value):
    if "$ref" in value:
        result = SPEC
        for part in value["$ref"].removeprefix("#/").split("/"): result = result[part]
        return result
    return value


def validate(value, schema, field="body"):
    root_schema = {"$schema": "http://json-schema.org/draft-04/schema#",
                   "components": VALIDATION_SPEC["components"], "allOf": [json_schema(schema)]}
    errors = sorted(Draft4Validator(root_schema, format_checker=FormatChecker()).iter_errors(value), key=lambda e: str(e.path))
    if errors:
        # No reutilizar e.message: puede contener la contraseña enviada o el token.
        details = [{"campo": field + ("." + ".".join(map(str, e.absolute_path)) if e.absolute_path else ""),
                    "motivo": "No cumple el tipo, formato o restricciones del contrato."} for e in errors[:10]]
        raise APIError(422, "DATO_INVALIDO", "La solicitud no cumple el contrato.", details)


async def request_data(request, item, operation):
    path = dict(request.path_params)
    query = {}
    params = [resolve(p) for p in item.get("parameters", []) + operation.get("parameters", [])]
    for param in params:
        name, schema = param["name"], param["schema"]
        if param["in"] == "path":
            validate(path[name], schema, name)
        elif param["in"] == "query":
            values = request.query_params.getlist(name)
            if len(values) > 1: raise APIError(422, "DATO_INVALIDO", "No se permiten parámetros repetidos.")
            value = request.query_params.get(name)
            if value is None:
                if param.get("required"): raise APIError(422, "DATO_INVALIDO", "Falta un parámetro obligatorio.")
                if "default" in schema: query[name] = schema["default"]
                continue
            if schema.get("type") == "integer":
                try: value = int(value)
                except ValueError: raise APIError(422, "DATO_INVALIDO", "El parámetro debe ser entero.")
            elif schema.get("type") == "boolean":
                if value.lower() not in ("true", "false"): raise APIError(422, "DATO_INVALIDO", "El parámetro debe ser true o false.")
                value = value.lower() == "true"
            validate(value, schema, name)
            query[name] = value
    body = {}
    if "requestBody" in operation:
        if request.headers.get("content-type", "").split(";")[0].strip().lower() != "application/json":
            raise APIError(415, "TIPO_CONTENIDO", "Content-Type debe ser application/json.")
        raw = await request.body()
        if len(raw) > 1024 * 1024: raise APIError(413, "CUERPO_GRANDE", "El cuerpo excede 1 MiB.")
        try:
            def reject_constant(value): raise ValueError("Número no JSON")
            body = json.loads(raw, parse_constant=reject_constant)
        except (ValueError, UnicodeDecodeError):
            raise APIError(400, "JSON_INVALIDO", "El cuerpo no es JSON válido.")
        schema = operation["requestBody"]["content"]["application/json"]["schema"]
        validate(body, schema)
    return path, query, body
