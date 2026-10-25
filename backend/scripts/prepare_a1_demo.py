"""Genera una copia LOCAL de la etapa A1, con base separada y sin autenticación.

No modifica la aplicación final. Solo para grabar el CRUD académico en loopback.
"""
from pathlib import Path
import shutil
import sys

from dotenv import dotenv_values
import psycopg
from psycopg import sql
from sqlalchemy import create_engine, select
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from backend.app.models import Usuario

values = dotenv_values(ROOT / "backend/.env")
url = make_url(values["DATABASE_URL"])
if url.host not in {"127.0.0.1", "localhost"}:
    raise SystemExit("La demostración A1 solo admite PostgreSQL local.")
target_url = url.set(database="arquitectura21_a1")
admin_url = url.set(drivername="postgresql", database="postgres")
with psycopg.connect(admin_url.render_as_string(hide_password=False), autocommit=True) as conn:
    if not conn.execute("SELECT 1 FROM pg_database WHERE datname=%s", [target_url.database]).fetchone():
        conn.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(target_url.database)))
with psycopg.connect(target_url.set(drivername="postgresql").render_as_string(hide_password=False), autocommit=True) as conn:
    if not conn.execute("SELECT to_regclass('public.usuarios')").fetchone()[0]:
        conn.execute((ROOT / "S05_S06_A1/esquema_bd.sql").read_text(), prepare=False)
source_engine = create_engine(values["DATABASE_URL"])
target_engine = create_engine(target_url)
with Session(source_engine) as source, Session(target_engine) as target, target.begin():
    if not target.scalar(select(Usuario.id).where(Usuario.rol == "Administrador", Usuario.activo.is_(True)).limit(1)):
        admin = source.scalar(select(Usuario).where(Usuario.rol == "Administrador", Usuario.activo.is_(True)).limit(1))
        if not admin: raise SystemExit("Primero provisiona el administrador local.")
        target.add(Usuario(correo=admin.correo, nombre="Administrador ficticio A1", hash_contrasena=admin.hash_contrasena,
                           rol="Administrador", activo=True))
snapshot = ROOT / ".local/a1_snapshot"
shutil.copytree(ROOT / "backend/app", snapshot / "backend/app", dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__"))
main = (ROOT / "backend/app/main.py").read_text()
main = main.replace("create_engine, text", "create_engine, text, select")
start = main.index("                user, session = None, None")
end = main.index("                request.state.service", start)
main = main[:start] + '''                # Etapa A1 local; A2 usa JWT en la aplicación final.
                user = await run_in_threadpool(db.scalar, select(Usuario).where(Usuario.rol == 'Administrador', Usuario.activo.is_(True)).limit(1))
                session = None
''' + main[end:]
(snapshot / "backend/app/main.py").write_text(main)
spec = yaml.safe_load((ROOT / "S05_S06_A1/openapi_equipo.yaml").read_text())
spec["paths"] = {p: item for p, item in spec["paths"].items() if not p.startswith(("/auth/", "/v1/sesiones"))}
spec["info"]["version"] = "2.0.0-a1"
spec["security"] = []
for item in spec["paths"].values():
    for method, operation in item.items():
        if method in {"get", "post", "put", "patch", "delete"}: operation["security"] = []
contract = snapshot / "S05_S06_A1/openapi_equipo.yaml"
contract.parent.mkdir(parents=True, exist_ok=True)
contract.write_text(yaml.safe_dump(spec, allow_unicode=True, sort_keys=False))
env = snapshot / "backend/.env"
env.write_text("DATABASE_URL=" + target_url.render_as_string(hide_password=False) + "\nJWT_SECRET=" + values["JWT_SECRET"] + "\nJWT_EXPIRATION=28800\n")
env.chmod(0o600)
print("Copia A1 preparada; base independiente arquitectura21_a1.")
print("Desde la raíz: cd .local/a1_snapshot")
print("../../.venv/bin/python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8001")
