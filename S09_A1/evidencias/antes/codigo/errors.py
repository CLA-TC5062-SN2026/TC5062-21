class APIError(Exception):
    def __init__(self, status, code, message, details=None):
        self.status = status
        self.body = {"codigo": code, "mensaje": message, "detalles": details or []}
        super().__init__(message)


def invalid(message, field=""):
    raise APIError(422, "DATO_INVALIDO", message, [{"campo": field, "motivo": message}])
