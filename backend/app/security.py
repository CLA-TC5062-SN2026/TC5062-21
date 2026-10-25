"""bcrypt y JWT con algoritmo fijo, expiración y sesión revocable en PostgreSQL."""
import hashlib
import hmac
from datetime import timedelta

import bcrypt
import jwt
from email_validator import EmailNotValidError, validate_email
from sqlalchemy import select

from .errors import APIError, invalid
from .models import Sesion, Usuario, now, uid

# Iguala el trabajo bcrypt cuando el correo no existe; no es una contraseña de acceso.
DUMMY_HASH = bcrypt.hashpw(b"timing-only-unusable-placeholder", bcrypt.gensalt(rounds=12))


def correo_normalizado(value):
    try:
        return validate_email(value.strip(), check_deliverability=False, test_environment=True).normalized.lower()
    except (EmailNotValidError, AttributeError):
        invalid("El correo no tiene un formato válido.", "correo")


def hash_password(value):
    raw = value.encode("utf-8")
    if len(value) < 10 or len(raw) > 72:
        invalid("La contraseña requiere al menos 10 caracteres y no más de 72 bytes UTF-8.", "contrasena")
    return bcrypt.hashpw(raw, bcrypt.gensalt(rounds=12)).decode("ascii")


def verify_password(value, encoded):
    try:
        raw = value.encode("utf-8")
        return len(raw) <= 72 and bcrypt.checkpw(raw, encoded.encode("ascii") if isinstance(encoded, str) else encoded)
    except (ValueError, AttributeError, UnicodeError):
        return False


def unauthorized():
    raise APIError(401, "NO_AUTENTICADO", "Credenciales o sesión inválidas.")


def issue_token(db, user, settings):
    instant = now()
    expires = instant + timedelta(seconds=settings.jwt_expiration)
    sid, jti = uid(), uid()
    token = jwt.encode({"sub": user.id, "sid": sid, "jti": jti,
        "iat": int(instant.timestamp()), "exp": int(expires.timestamp()),
        "iss": settings.jwt_issuer, "aud": settings.jwt_audience}, settings.jwt_secret, algorithm="HS256")
    session = Sesion(id=sid, usuario_id=user.id, jti=jti,
        hash_token=hashlib.sha256(token.encode()).hexdigest(), creada_en=instant,
        ultima_actividad_en=instant, expira_en=expires)
    db.add(session)
    db.flush()
    return token, session


def authenticate(db, header, settings):
    if not header or len(header.split()) != 2:
        unauthorized()
    scheme, token = header.split()
    if scheme.lower() != "bearer": unauthorized()
    try:
        claims = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"],
            issuer=settings.jwt_issuer, audience=settings.jwt_audience,
            options={"require": ["sub", "sid", "jti", "iat", "exp", "iss", "aud"]})
        # Formato UUID antes de enviar parámetros a PostgreSQL.
        from uuid import UUID
        for name in ("sub", "sid", "jti"): UUID(claims[name])
    except (jwt.InvalidTokenError, ValueError, TypeError, KeyError, AttributeError):
        unauthorized()
    session = db.scalar(select(Sesion).where(Sesion.id == claims["sid"]).with_for_update())
    user = db.get(Usuario, claims["sub"])
    instant = now()
    if (not session or not user or not user.activo or session.usuario_id != user.id
            or session.jti != claims["jti"] or session.revocada_en is not None
            or session.expira_en <= instant
            or session.ultima_actividad_en <= instant - timedelta(seconds=settings.idle_seconds)
            or not hmac.compare_digest(session.hash_token, hashlib.sha256(token.encode()).hexdigest())):
        unauthorized()
    session.ultima_actividad_en = instant
    return user, session
