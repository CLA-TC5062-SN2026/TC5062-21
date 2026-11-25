import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / "backend/.env")


@dataclass(frozen=True)
class Settings:
    database_url: str
    jwt_secret: str
    jwt_expiration: int
    jwt_issuer: str = "tc5062-equipo21"
    jwt_audience: str = "arquitectura-api"
    idle_seconds: int = 1800

    @classmethod
    def from_env(cls):
        url = os.environ.get("DATABASE_URL", "")
        secret = os.environ.get("JWT_SECRET", "")
        expiration = int(os.environ.get("JWT_EXPIRATION", "28800"))
        if not url.startswith("postgresql+psycopg://"):
            raise ValueError("DATABASE_URL debe usar PostgreSQL y psycopg.")
        if len(secret.encode()) < 32 or secret.startswith("CAMBIAR"):
            raise ValueError("JWT_SECRET requiere al menos 32 bytes aleatorios.")
        if not 1 <= expiration <= 28800:
            raise ValueError("JWT_EXPIRATION debe ser entre 1 y 28800 segundos.")
        return cls(url, secret, expiration)
