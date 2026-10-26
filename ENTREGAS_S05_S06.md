# Actividades S05-S06 — Equipo 21

Implementación y documentación preparadas el 25 de octubre de 2026 a partir de los diseños de Gregorio, Jean Paul y Liciel. La rama conserva el SRS del equipo y sus 56 criterios canónicos. El equipo debe revisar las decisiones de consolidación antes de presentar la entrega.

- [A1: diseño, SQL y CRUD](S05_S06_A1/README.md)
- [A2: autenticación y seguridad](S05_S06_A2/README.md)
- [Arranque del backend](backend/README.md)

## Videos incorporados

Gregorio proporcionó los dos videos. Ambos cumplen el límite de duración de 1 minuto:

1. `S05_S06_A1/pruebas_postman.mp4` (50.41 segundos); [guion A1](S05_S06_A1/guion_video.md).
2. `S05_S06_A2/pruebas_auth.mp4` (46.40 segundos); [guion A2](S05_S06_A2/guion_video.md).

Los videos recibidos están incluidos en sus carpetas; sus hashes, metadatos y observaciones constan en `evidencias/video_recibido.json`. **Requieren corregir la visibilidad de respuestas JSON; en A2 también debe verse accessToken del login.** Tras sustituirlos por las tomas corregidas y actualizar su revisión, generar los ZIP definitivos desde la raíz:

```sh
.venv/bin/python backend/scripts/empaquetar_entregas.py
```

Se crean `entregas/S05_S06_A1.zip` y `entregas/S05_S06_A2.zip` para subir a las tareas correspondientes de Canvas. El script se niega a crear ZIP definitivos si falta un video o su revisión visual requiere ajustes. `--borrador` crea archivos claramente marcados `_pendiente_video.zip` para revisión previa. Los ZIP incluyen la carpeta de cada actividad; backend se entrega por GitHub como pide la consigna.

Los dos MP4 se incluyen en el repositorio del equipo junto con su documentación actualizada. Si se necesita revisar este trabajo en otra máquina, clonar la rama e instalar las dependencias según backend/README.md; los secretos locales no se comparten ni están en los ZIP.

## Comprobaciones realizadas

- PostgreSQL real: 15 tablas, 15 PK, 29 FK y 45 índices.
- 50 pruebas de integración aprobadas; 46 operaciones cubiertas con respuestas validadas contra OpenAPI.
- Postman A1: 6 peticiones / 21 aserciones, sin fallas.
- Postman A2: 6 peticiones / 22 aserciones y firma alterada 1 petición / 3 aserciones, sin fallas.
- curl real: sin token 401, firma alterada 401, Consulta 403 y Administrador 201.
- Validación semántica OpenAPI y lint de sintaxis Postman sin violaciones. La colección generada tiene 46 peticiones sin errores de lint.

La evidencia automatizada complementa los videos; no los reemplaza. La ejecución verificada fue nativa en macOS; Docker Compose se incluye sin afirmar que se haya ejecutado.
