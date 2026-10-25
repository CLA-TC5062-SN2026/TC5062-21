"""Prepara un clúster privado de desarrollo. No modifica el servicio PostgreSQL global."""
import json
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
LOCAL = ROOT / ".local"
LOCAL.mkdir(exist_ok=True)
pgbin = Path(os.environ.get("PG_BIN", "/opt/homebrew/opt/postgresql@17/bin"))
if not (pgbin / "initdb").exists():
    raise SystemExit("Indica PG_BIN con los binarios PostgreSQL 17, o usa Docker Compose según backend/README.md.")
envfile = ROOT / "backend/.env"
if not envfile.exists():
    password = secrets.token_urlsafe(24)
    secret = secrets.token_urlsafe(48)
    envfile.write_text(f"DATABASE_URL=postgresql+psycopg://equipo21:{password}@127.0.0.1:55432/arquitectura21\nJWT_SECRET={secret}\nJWT_EXPIRATION=28800\n")
    envfile.chmod(0o600)
from dotenv import dotenv_values
from sqlalchemy.engine import make_url
values = dotenv_values(envfile)
url = make_url(values["DATABASE_URL"])
pg_env = {**os.environ, "PGPASSWORD": url.password}
data = LOCAL / "postgres"
if not (data / "PG_VERSION").exists():
    pwfile = LOCAL / ".pg-password"
    pwfile.write_text(url.password)
    pwfile.chmod(0o600)
    try:
        subprocess.run([str(pgbin/"initdb"), "-D", str(data), "-U", "equipo21", "--auth=scram-sha-256", "--pwfile="+str(pwfile), "--encoding=UTF8", "--locale=C"], check=True, stdout=subprocess.DEVNULL)
    finally: pwfile.unlink(missing_ok=True)
if subprocess.run([str(pgbin/"pg_ctl"), "-D", str(data), "status"], stdout=subprocess.DEVNULL).returncode:
    subprocess.run([str(pgbin/"pg_ctl"), "-D", str(data), "-l", str(LOCAL/"postgres.log"), "-o", "-p 55432 -h 127.0.0.1 -c unix_socket_directories=''", "start"], check=True)
check = subprocess.run([str(pgbin/"psql"), "-h", "127.0.0.1", "-p", "55432", "-U", "equipo21", "-d", "postgres", "-Atc", "SELECT 1 FROM pg_database WHERE datname='arquitectura21'"], env=pg_env, capture_output=True, text=True, check=True)
if check.stdout.strip() != "1":
    subprocess.run([str(pgbin/"createdb"), "-h", "127.0.0.1", "-p", "55432", "-U", "equipo21", "arquitectura21"], env=pg_env, check=True)
from sqlalchemy import create_engine, text
from backend.app.models import Base, Capa, Usuario, now
from backend.app.security import hash_password
from sqlalchemy.orm import Session
engine = create_engine(values["DATABASE_URL"])
with engine.connect() as connection:
    exists = connection.scalar(text("SELECT to_regclass('public.usuarios')"))
if not exists:
    subprocess.run([str(pgbin/"psql"), "-v", "ON_ERROR_STOP=1", "-h", "127.0.0.1", "-p", "55432", "-U", "equipo21", "-d", "arquitectura21", "-f", str(ROOT/"S05_S06_A1/esquema_bd.sql")], env=pg_env, check=True, stdout=subprocess.DEVNULL)
credentials_path = LOCAL / "demo_credentials.json"
if not credentials_path.exists():
    credentials = {"password": secrets.token_urlsafe(15), "admin": "admin@equipo21.test", "editor": "editor@equipo21.test", "consulta": "consulta@equipo21.test"}
    with Session(engine) as db, db.begin():
        for key, role in (("admin", "Administrador"), ("editor", "Editor"), ("consulta", "Consulta")):
            db.add(Usuario(correo=credentials[key], nombre=f"Cuenta ficticia {role}", hash_contrasena=hash_password(credentials["password"]), rol=role, activo=True))
        for name in ("Negocio", "Datos", "Aplicaciones", "Tecnología"):
            db.add(Capa(nombre=name))
    credentials_path.write_text(json.dumps(credentials, indent=2)+"\n")
    credentials_path.chmod(0o600)
print("PostgreSQL listo en 127.0.0.1:55432; esquema importado. Credenciales ficticias solo en .local/demo_credentials.json.")
