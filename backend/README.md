# Backend — Equipo 21

Python 3.12, FastAPI, SQLAlchemy, psycopg y PostgreSQL 17. El contrato canónico es `../S05_S06_A1/openapi_equipo.yaml`; `../postman/specs/openapi.yaml` es un enlace a ese archivo, no otra especificación editable.

## Arranque en macOS con PostgreSQL instalado

Desde la raíz del repositorio:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r backend/requirements-dev.txt
.venv/bin/python backend/scripts/export_sql.py
.venv/bin/python backend/scripts/setup_local.py
.venv/bin/python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

`setup_local.py` usa por defecto `/opt/homebrew/opt/postgresql@17/bin`; puede configurarse con `PG_BIN`. Crea un clúster aislado en `.local/postgres`, puerto 55432, con SCRAM y conexiones TCP desde loopback. Importa el SQL con `ON_ERROR_STOP` y prepara cuentas exclusivamente ficticias. No habilita un servicio de inicio automático. El archivo `backend/.env` y `.local/demo_credentials.json` se generan con permisos 0600 y están ignorados por Git. Ejecutarlo otra vez conserva los datos.

Para usar otro PostgreSQL, copiar `.env.example` como `.env`, configurar la conexión, generar un secret aleatorio e importar `S05_S06_A1/esquema_bd.sql` en una base vacía. El SQL requiere PostgreSQL y no usa un fallback SQLite. La primera cuenta Administrador debe provisionarse mediante un procedimiento técnico restringido; el registro público siempre crea Consulta.

## Alternativa Docker Compose

Configurar `DB_PASSWORD`, `JWT_SECRET` y `JWT_EXPIRATION` en `backend/.env`; utilizar contraseñas URL seguras. Ejecutar `docker compose --env-file backend/.env up --build`. PostgreSQL importa el SQL al inicializar un volumen vacío y la API queda disponible solo por el puerto local 8000. Después, crear el primer administrador con `docker compose --env-file backend/.env exec api python backend/scripts/provision_admin.py --correo admin@equipo21.test --nombre Administrador`; el programa pide la contraseña de forma enmascarada. Esta alternativa se proporciona para reproducción; en esta entrega se ejecutó PostgreSQL nativo, porque Docker no está instalado en el equipo de verificación.

## API

- Documentación interactiva: `http://127.0.0.1:8000/docs`.
- Estado de base de datos: `GET /api/salud`.
- Registro: `POST /api/auth/register` con `correo`, `nombre`, `contrasena` → 201, sin contraseña ni hash.
- Login: `POST /api/auth/login` con `correo`, `contrasena` → 200 con `accessToken`.
- Perfil: `GET /api/auth/me` con `Authorization: Bearer <accessToken>`.
- Dominio: `/api/v1/...`; todas sus operaciones están protegidas excepto el alias de inicio de sesión `POST /api/v1/sesiones`.

JWT_SECRET es obligatorio y debe tener al menos 32 bytes; no existe un valor predeterminado de desarrollo. `JWT_EXPIRATION` expresa segundos entre 1 y 28800. Se valida firma HS256, exp, iat, iss, aud, sub, sid, jti, hash del token, cuenta activa, revocación y 30 minutos de inactividad. Un cambio de rol, desactivación o restablecimiento revoca todas las sesiones de la cuenta; el cierre individual conserva las demás.

No se aceptan roles en el registro público. Administrador administra cuentas y catálogos; Editor escribe solo en sus capas; Consulta lee. Ni passwords ni tokens se escriben en bitácora o logs del backend.

## Verificación

```sh
.venv/bin/python -m pytest backend/tests -q --junitxml=S05_S06_A2/evidencias/pytest.xml
postman spec lint postman/specs/openapi.yaml --issueType=syntax --no-report-events
postman collection lint postman/collections/S05-S06-A1-CRUD
postman collection lint postman/collections/S05-S06-A2-Autenticacion
```

La suite usa una base aislada llamada `arquitectura21_test` y reconstruye únicamente su esquema; requiere una conexión local de pruebas con permiso para crear esa base. Nunca elimina el esquema de `arquitectura21`. Los recorridos importables de Postman y sus resultados están en las carpetas de entrega. El entorno de ejemplo no contiene credenciales; las variables reales de demostración permanecen solo en `.local/`.

## Organización

- `app/contract.py`: contrato y validación de solicitudes.
- `app/main.py`: rutas y middleware de transacción/autenticación.
- `app/security.py`: bcrypt, emisión y validación de JWT.
- `app/services.py`: reglas de negocio, permisos por capa y bitácora.
- `app/models.py`: modelo relacional y restricciones.
- `scripts/`: generación reproducible de artefactos y entorno local.
- `tests/`: integración contra PostgreSQL real.

Para detener el clúster de desarrollo: `PG_BIN/pg_ctl -D .local/postgres stop` sustituyendo PG_BIN por su ruta real. En despliegue, usar HTTPS y una cuenta de base de datos limitada a la aplicación; no publicar los puertos de desarrollo.
