"""Errores de dominio traducibles al contrato HTTP, sin datos sensibles."""
from typing import NoReturn


class APIError(Exception):
    def __init__(self, status, code, message, details=None):
        self.status = status
        self.body = {"codigo": code, "mensaje": message, "detalles": details or []}
        super().__init__(message)


def invalid(message, field="") -> NoReturn:
    raise APIError(422, "DATO_INVALIDO", message, [{"campo": field, "motivo": message}])
