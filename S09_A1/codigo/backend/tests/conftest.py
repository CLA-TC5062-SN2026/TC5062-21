"""Pruebas de integración contra PostgreSQL aislado, nunca contra la base de trabajo."""
import os
from pathlib import Path
import sys

import psycopg
from psycopg import sql
import pytest
from dotenv import dotenv_values
from sqlalchemy.engine import make_url

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
values = dotenv_values(ROOT / "backend/.env")
url = make_url(values["DATABASE_URL"])
TEST_NAME = "arquitectura21_test"
admin_url = url.set(drivername="postgresql", database="postgres").render_as_string(hide_password=False)
test_url = url.set(database=TEST_NAME)


@pytest.fixture(scope="session")
def api():
    assert test_url.database == TEST_NAME
    with psycopg.connect(admin_url, autocommit=True) as conn:
        if not conn.execute("SELECT 1 FROM pg_database WHERE datname=%s", [TEST_NAME]).fetchone():
            conn.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(TEST_NAME)))
    plain = test_url.set(drivername="postgresql").render_as_string(hide_password=False)
    with psycopg.connect(plain, autocommit=True) as conn:
        conn.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
        conn.execute((ROOT / "S05_S06_A1/esquema_bd.sql").read_text(), prepare=False)
    os.environ.update(DATABASE_URL=test_url.render_as_string(hide_password=False),
                      JWT_SECRET=values["JWT_SECRET"], JWT_EXPIRATION="28800")
    from backend.app.main import app, engine
    from backend.app.models import Capa, Usuario
    from backend.app.security import hash_password
    from sqlalchemy.orm import Session
    password = "PasswordPrueba21!"
    with Session(engine) as db, db.begin():
        for role in ("Administrador", "Editor", "Consulta"):
            db.add(Usuario(correo=role.lower()+"@prueba.test", nombre="Prueba " + role,
                           hash_contrasena=hash_password(password), rol=role, activo=True))
        db.add(Capa(nombre="Negocio"))
    from fastapi.testclient import TestClient
    with TestClient(app) as client:
        client.test_password = password
        client.test_engine = engine
        yield client


@pytest.fixture
def admin_token(api):
    r = api.post("/api/auth/login", json={"correo": "administrador@prueba.test", "contrasena": api.test_password})
    assert r.status_code == 200, r.text
    return r.json()["accessToken"]
