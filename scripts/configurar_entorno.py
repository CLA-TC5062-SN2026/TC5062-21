"""Genera configuración local sin sobrescribir archivos existentes ni mostrar secretos."""
from pathlib import Path
import secrets

ROOT = Path(__file__).resolve().parents[1]
backend_env = ROOT / 'backend/.env'
if not backend_env.exists():
    password = secrets.token_urlsafe(24)
    backend_env.write_text(
        'DATABASE_URL=postgresql+psycopg://equipo21:' + password + '@127.0.0.1:55432/arquitectura21\n'
        'JWT_SECRET=' + secrets.token_urlsafe(48) + '\n'
        'JWT_EXPIRATION=28800\nDB_PASSWORD=' + password + '\n')
    backend_env.chmod(0o600)
frontend_env = ROOT / 'frontend/.env'
if not frontend_env.exists():
    frontend_env.write_text((ROOT / 'frontend/.env.example').read_text())
print('Configuración local lista en backend/.env y frontend/.env. Los archivos existentes se conservan.')
print('Si usas PostgreSQL nativo fuera de Homebrew, define PG_BIN con la carpeta de sus binarios.')
