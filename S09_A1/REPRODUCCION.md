# Reproducción de la auditoría

## Preparación

Se usó macOS ARM64, Python 3.12.16 y PostgreSQL 17.11 con ICU. El esquema usa la colación `und-x-icu`; SQLite no reproduce este entorno.

En el repositorio completo, trabajar desde su raíz. En el ZIP, entrar a `S09_A1/codigo/`. Instalar las versiones guardadas:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r backend/requirements-quality.lock.txt
```

El archivo de versiones incluye las dependencias transitivas observadas. Los requisitos principales se conservan también en `requirements.txt`, `requirements-dev.txt` y `requirements-quality.txt`.

Configurar un PostgreSQL de desarrollo con permiso para crear la base aislada de pruebas. El ayudante crea un clúster local en `.local/postgres`, puerto 55432, y genera `backend/.env` con permisos restringidos:

```sh
PG_BIN=/ruta/a/postgresql/bin .venv/bin/python backend/scripts/setup_local.py
```

La ruta PG_BIN se adapta a la instalación local. El esquema ya se incluye en `S05_S06_A1/esquema_bd.sql`. Como alternativa, configurar `backend/.env` a partir de `backend/.env.example` con una conexión real de desarrollo y un JWT_SECRET aleatorio de al menos 32 bytes. El paquete no contiene credenciales ni el entorno privado de ejecución.

## Pruebas y medición

La suite crea o reconstruye exclusivamente `arquitectura21_test`; no elimina el esquema de la base de trabajo. **Ejecutar la suite y la medición secuencialmente**, porque ambas utilizan la misma base aislada.

```sh
mkdir -p S09_A1/evidencias/reproduccion
.venv/bin/python -m pytest backend/tests -q --junitxml=S09_A1/evidencias/reproduccion/pytest.xml
.venv/bin/python backend/scripts/medir_consultas_s09.py --output S09_A1/evidencias/reproduccion/consultas.json
.venv/bin/python backend/scripts/auditar_calidad.py --output S09_A1/evidencias/reproduccion
```

La suite final tiene 84 casos. La medición siembra temporalmente 60 y 300 elementos, compara tres operaciones y revierte cada muestra. Requiere ejecutar pytest primero para disponer del esquema y una cuenta ficticia administradora.

El análisis estático final devuelve **28**, porque hay observaciones C/W/R pendientes. Guarda la salida completa y el código de salida. No convertir ese resultado en una afirmación de “linter sin problemas”.

El recorrido histórico escribe `S05_S06_A2/evidencias/cobertura_operaciones.json`. Es un resultado de prueba, no una modificación del contrato. En el repositorio de trabajo se copió a la evidencia de Semana 9 y se restauró el archivo histórico.

## Interpretación de la comparación

El código entregado corresponde al estado final. Ejecutarlo reproduce ese estado. La línea base conserva su código original, hashes, pruebas y conteos en `evidencias/antes/`; no se regeneran resultados “antes” con el código refactorizado.

Para repetir la comparación inicial en una copia aislada, restaurar los ocho archivos de `evidencias/antes/codigo/` en `backend/app/` y retirar de esa copia los dos módulos que no existían (`pagination.py` y `value_rules.py`). Ejecutar solo `backend/tests/test_integration.py` para las 50 pruebas originales, y usar el mismo script de medición y las mismas dependencias. No ejecutar las pruebas nuevas de reglas contra una versión que todavía no contiene ese módulo.

La comparación cuenta SELECT que salen de SQLAlchemy. No incluye las sentencias ejecutadas dentro de triggers, autenticación HTTP ni preparación de la muestra. La reducción de consultas no mide latencia, capacidad de concurrencia ni cobertura de código.

## Archivos de referencia y límites

El contrato y el esquema se incluyen sin cambios. Las operaciones públicas conservan su interfaz. Los reportes finales documentan deudas pendientes y una advertencia de deprecación de Starlette/httpx. No se ejecutó Docker, no se configuró un pipeline remoto y no se publicó esta rama.
