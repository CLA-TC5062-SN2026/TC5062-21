# S05-S06-A2 — Autenticación y seguridad del API

Implementación en `../backend/` y contrato consolidado en `../S05_S06_A1/openapi_equipo.yaml`. Revisión de seguridad y evidencias listas. Se incorporó el video de Gregorio `pruebas_auth.mp4` (46.40 segundos), dentro del máximo de 1 minuto. **Pendiente:** corregir la visibilidad del video antes del ZIP definitivo: Volver a grabar mostrando Body en el panel de respuesta de los seis pasos, incluido accessToken visible después del login y JSON en los casos 201, 200, 401 y 403. En el video recibido el flujo muestra Test Results y no el JWT del login.

## Archivos

- `revision_seguridad.md`: revisión, correcciones, tabla de las 42 operaciones protegidas y casos curl reales.
- `coleccion_auth.postman_collection.json`: recorrido de 6 peticiones.
- `coleccion_firma.postman_collection.json`: caso adicional de firma alterada.
- `entorno_ejemplo.postman_environment.json`: variables sin credenciales.
- `guion_video.md`, `evidencias/`: preparación y reportes ejecutados.

Para preparar un entorno local de demostración vigente, con la API en puerto 8000:

```sh
.venv/bin/python backend/scripts/prepare_postman_runtime.py
```

Importa `.local/desktop.postman_environment.json` en Postman y selecciona ese entorno solo para A2. Contiene únicamente cuentas ficticias locales, pero debe mantenerse fuera de Git y de los ZIP. Los JWT vencen a los 30 minutos de inactividad; vuelve a ejecutar el script e importar el entorno justo antes de grabar. Haz lo mismo para repetir el recorrido con un runId nuevo y evitar registro duplicado.
