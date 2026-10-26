# S05-S06-A1 — Diseño de base de datos y servicios CRUD

El diseño consolidado, DDL, revisión y colecciones están listos. Se incorporó el video de Gregorio `pruebas_postman.mp4` (50.41 segundos), dentro del máximo de 1 minuto. **Pendiente:** corregir la visibilidad del video antes del ZIP definitivo: Volver a grabar mostrando Body en el panel de respuesta de al menos cinco operaciones, con sus JSON y códigos HTTP visibles. En el video recibido capa, tipo y consultas muestran principalmente Test Results; el JSON sí se ve en alta y baja de elemento. Las decisiones de consolidación quedan disponibles para revisión del equipo.

## Archivos

- `openapi_equipo.yaml`: contrato final compartido con A2; conserva los 56 criterios canónicos y BearerAuth.
- `diagrama_clases_equipo.puml`, `arquitectura_equipo.md`, `diferencias_diseno.md`: diseño consolidado y resoluciones.
- `esquema_bd.sql`, `revision_sql.md`: esquema PostgreSQL y revisión verificada.
- `insumos/`: originales de los tres integrantes, SRS e inventario de comparación.
- `coleccion_crud.postman_collection.json`, `guion_video.md`, `evidencias/`: recorrido y resultados.

## Reproducir el video sin autenticación

La rama final usa seguridad A2. Para la evidencia histórica CRUD A1, desde la raíz y después del arranque local descrito en `backend/README.md`:

```sh
.venv/bin/python backend/scripts/prepare_a1_demo.py
cd .local/a1_snapshot
../../.venv/bin/python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8001
```

La copia usa la base separada `arquitectura21_a1`; no desactiva seguridad en la API final. Si el servidor 8001 ya está activo no lo arranques otra vez. Importa la colección en Postman y sigue `guion_video.md`. Al terminar detén ese servidor con Ctrl+C. No se publica esta etapa sin seguridad.

Los scripts regeneran artefactos desde los modelos y contratos; las fuentes originales están incluidas para reproducir la consolidación.
