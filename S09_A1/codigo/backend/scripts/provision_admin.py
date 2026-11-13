"""Alta técnica del primer administrador; contraseña mediante entrada enmascarada."""
import argparse
from getpass import getpass
from pathlib import Path
import sys

from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from backend.app.config import Settings
from backend.app.models import Usuario
from backend.app.security import correo_normalizado, hash_password

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--correo',required=True)
parser.add_argument('--nombre',required=True)
args=parser.parse_args()
password=getpass('Contraseña del primer administrador: ')
if password != getpass('Confirmar contraseña: '): raise SystemExit('Las contraseñas no coinciden.')
with Session(create_engine(Settings.from_env().database_url)) as db,db.begin():
    db.execute(text('SELECT pg_advisory_xact_lock(506221)'))
    if db.scalar(select(Usuario.id).where(Usuario.activo.is_(True),Usuario.rol=='Administrador').limit(1)):
        raise SystemExit('Ya existe un administrador activo; usa la gestión autenticada de cuentas.')
    user=Usuario(correo=correo_normalizado(args.correo),nombre=args.nombre.strip(),
        hash_contrasena=hash_password(password),rol='Administrador',activo=True)
    if not user.nombre or len(user.nombre)>120: raise SystemExit('Nombre inválido.')
    db.add(user)
print('Primer administrador creado. No se imprimió la contraseña.')
