# Actividades S05-S06 — Equipo 21

Implementación y documentación preparadas el 25 de octubre de 2026 a partir de los diseños de Gregorio, Jean Paul y Liciel. La rama conserva el SRS del equipo y sus 56 criterios canónicos. El equipo debe revisar las decisiones de consolidación antes de presentar la entrega.

- [A1: diseño, SQL y CRUD](S05_S06_A1/README.md)
- [A2: autenticación y seguridad](S05_S06_A2/README.md)
- [Arranque del backend](backend/README.md)

## Pendiente a cargo de Gregorio

Grabar los videos continuos, de máximo 1 minuto cada uno:

1. `S05_S06_A1/pruebas_postman.mp4` siguiendo [guion A1](S05_S06_A1/guion_video.md).
2. `S05_S06_A2/pruebas_auth.mp4` siguiendo [guion A2](S05_S06_A2/guion_video.md).

Los archivos de video todavía no están incluidos. Después de guardarlos, desde la raíz:

```sh
.venv/bin/python backend/scripts/empaquetar_entregas.py
```

Se crean `entregas/S05_S06_A1.zip` y `entregas/S05_S06_A2.zip` para subir a las tareas correspondientes de Canvas. El script se niega a crear ZIP definitivos si falta un video. `--borrador` crea archivos claramente marcados `_pendiente_video.zip` para revisión previa. Los ZIP incluyen la carpeta de cada actividad; backend se entrega por GitHub como pide la consigna.

Añadir y commitear los dos MP4 al repositorio del equipo tras grabar. Si se necesita revisar este trabajo en otra máquina, clonar la rama e instalar las dependencias según backend/README.md; los secretos locales no se comparten ni están en los ZIP.

## Comprobaciones realizadas

- PostgreSQL real: 15 tablas, 15 PK, 29 FK y 45 índices.
- 50 pruebas de integración aprobadas; 46 operaciones cubiertas con respuestas validadas contra OpenAPI.
- Postman A1: 6 peticiones / 21 aserciones, sin fallas.
- Postman A2: 6 peticiones / 22 aserciones y firma alterada 1 petición / 3 aserciones, sin fallas.
- curl real: sin token 401, firma alterada 401, Consulta 403 y Administrador 201.
- Validación semántica OpenAPI y lint de sintaxis Postman sin violaciones. La colección generada tiene 46 peticiones sin errores de lint.

La evidencia automatizada complementa los videos; no los reemplaza. La ejecución verificada fue nativa en macOS; Docker Compose se incluye sin afirmar que se haya ejecutado.
