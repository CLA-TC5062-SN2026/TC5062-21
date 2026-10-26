# Video A2 — máximo 1 minuto, continuo

## Preparación fuera de la grabación

1. Mantén PostgreSQL y la API final en `http://127.0.0.1:8000` activos.
2. Desde la raíz, ejecuta `.venv/bin/python backend/scripts/prepare_postman_runtime.py`. Genera runId nuevo y tokens vigentes; no imprime secretos.
3. Importa `coleccion_auth.postman_collection.json` y el archivo local `.local/desktop.postman_environment.json` en Postman; selecciona ese entorno. No compartas ese archivo privado: el entregable es el entorno de ejemplo vacío.
4. La cuenta registrada es Consulta. El paso 2 usa un Administrador ficticio ya provisionado para demostrar POST de una capa. El último paso usa el token de otra cuenta Consulta, obtenido antes de grabar. Las variables reales se completan en el entorno local.
5. Abre las seis peticiones en orden. Verifica que los scripts de la colección guardan adminToken y que la vista de cabeceras puede mostrar Authorization resuelto, no solo la variable. El token JWT debe verse en la respuesta del login. Prueba antes de iniciar la grabación; vuelve a generar el entorno para cada toma.
6. En Postman Lightweight las variables no persistieron entre pestañas durante el ensayo; usa Postman completo con la colección importada o prepara cabeceras manualmente copiando el token de login. El paso 3 debe usar el token que acabas de obtener.

## Toma sugerida (55–59 segundos)

| Tiempo | Acción | Mostrar |
|---|---|---|
| 0–9 s | POST /api/auth/register | Body correo/nombre/contrasena ficticios; 201 sin contraseña en respuesta |
| 9–19 s | POST /api/auth/login | Body Administrador ficticio; 200 y accessToken visible |
| 19–29 s | GET /api/auth/me | Authorization Bearer del login; 200 identidad/rol |
| 29–39 s | POST /api/v1/capas | Body nombre y Bearer Admin; 201 |
| 39–49 s | Misma POST /api/v1/capas sin token | Sin Authorization; 401 y JSON |
| 49–58 s | Misma POST con Bearer de Consulta | Cabecera de Consulta; 403 y JSON |

Sin cortes de edición. Guarda como `S05_S06_A2/pruebas_auth.mp4`. La prueba de firma alterada se entrega adicionalmente como evidencia de terminal y colección independiente; no hace falta añadirla a los seis pasos del video.

## Ajuste del video recibido

Volver a grabar mostrando Body en el panel de respuesta de los seis pasos, incluido accessToken visible después del login y JSON en los casos 201, 200, 401 y 403. En el video recibido el flujo muestra Test Results y no el JWT del login.

Antes de grabar, abre cada petición y selecciona **Body en el panel inferior de respuesta**. Después de Send, deja visibles el código HTTP y el JSON; no basta con el resultado PASSED del test. La preparación y la revisión de variables pueden quedar fuera de la toma para reservar tiempo a las respuestas. La toma final debe ser continua y de máximo 60 segundos.
