# Video A1 — máximo 1 minuto, continuo

## Preparación fuera de la grabación

1. Servidor de la copia A1 en `http://127.0.0.1:8001`. `README.md` explica cómo generarla. La base de datos debe permanecer activa.
2. Importa `coleccion_crud.postman_collection.json` en Postman. Selecciona **sin entorno** para evitar que baseUrl de A2 cambie el destino. La colección apunta al puerto 8001.
3. En la versión completa de Postman los scripts encadenan capaId, tipoId, campoNombreId y elementoId mediante variables de colección. Comprueba el recorrido antes de grabar. Si usas el cliente Lightweight, inicia sesión para importar o copia manualmente los IDs: su almacenamiento de variables no persistió entre peticiones en el ensayo local.
4. Prepara las seis pestañas; mantén visibles método, URL, body cuando corresponda, respuesta JSON y estado. Puedes usar `{{$timestamp}}` como runId o establecer un nombre nuevo si repites una toma.

## Toma sugerida (50–58 segundos)

| Tiempo | Acción | Mostrar |
|---|---|---|
| 0–8 s | POST /api/v1/capas | Body nombre; 201 e ID |
| 8–16 s | GET /api/v1/capas/{capaId} | 200 y el mismo ID: persistencia |
| 16–25 s | POST /api/v1/tipos-elemento | Body capaId/nombre; 201 y campo Nombre |
| 25–35 s | POST /api/v1/elementos | Body valores; 201 con nombre |
| 35–45 s | GET /api/v1/elementos/{elementoId} | 200 y valor guardado |
| 45–55 s | DELETE /api/v1/elementos/{elementoId} | 200 y estado baja |

Son seis combinaciones de método y ruta, con POST, GET y DELETE. Usa un solo recorrido sin cortes. Guarda como `S05_S06_A1/pruebas_postman.mp4`. Después detén la copia A1 sin autenticación; la API final del puerto 8000 conserva JWT.

## Ajuste del video recibido

Volver a grabar mostrando Body en el panel de respuesta de al menos cinco operaciones, con sus JSON y códigos HTTP visibles. En el video recibido capa, tipo y consultas muestran principalmente Test Results; el JSON sí se ve en alta y baja de elemento.

Antes de grabar, abre cada petición y selecciona **Body en el panel inferior de respuesta**. Después de Send, deja visibles el código HTTP y el JSON; no basta con el resultado PASSED del test. La preparación y la revisión de variables pueden quedar fuera de la toma para reservar tiempo a las respuestas. La toma final debe ser continua y de máximo 60 segundos.
