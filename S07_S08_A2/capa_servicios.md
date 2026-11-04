# Capa de servicios e integración frontend–backend

Equipo 21 · TC5062 · 3 de noviembre de 2026.

Se consume `S05_S06_A1/openapi_equipo.yaml` 2.0.0 y el backend de semana 6. Recorrido: login → panel protegido → inventario → búsqueda → detalle. Los cinco elementos de demostración son ficticios y están persistidos en PostgreSQL; la interfaz informa ese carácter.

## Organización y contrato

| Archivo en frontend/src/services | Responsabilidad | Operaciones relativas a la URL base |
| --- | --- | --- |
| client.ts | URL, JSON, JWT, errores, cancelación y tiempo límite | createApiClient y ApiError |
| authService.ts | Acceso, perfil y cierre | POST /auth/login, GET /auth/me, DELETE /v1/sesiones/actual |
| elementosService.ts | Listado y detalle | GET /v1/elementos, GET /v1/elementos/{id} |
| capasService.ts | Catálogo de capas | GET /v1/capas |
| tiposService.ts | Catálogo de tipos | GET /v1/tipos-elemento |
| session.ts y types.ts | Token, evento de expiración y tipos | Sin llamadas adicionales |

`VITE_API_URL` configura la base; el ejemplo usa `/api`. Las vistas no duplican prefijos HTTP. Filtros se codifican con URLSearchParams e identificadores con encodeURIComponent. El login envía `correo` y `contrasena`; recibe `accessToken` y `usuario`.

Las páginas invocan servicios y useResource administra carga, cancelación y reintento. El listado usa nombre, capa, tipo y página; el tamaño definido por el API es 25. Cero resultados produce un estado vacío. Las cantidades del panel se calculan con respuestas del servidor.

## Cliente HTTP y equivalente de interceptor

Fetch se encapsula en una función común, como punto central de intervención de solicitudes/respuestas. Agrega Accept JSON, Content-Type al enviar cuerpo y Authorization Bearer cuando existe token y la operación no es pública. Login utiliza `auth: false`. `credentials: 'omit'` evita depender de cookies.

Se aplica un límite de 12 segundos y se combina la cancelación externa con AbortController. Cancelar por navegación no muestra un error; el tiempo agotado sí. ApiError conserva estado/código y un mensaje útil. Se rechaza una respuesta exitosa que no puede interpretarse como JSON. Los tipos de TypeScript describen respuestas esperadas; no validan exhaustivamente todos sus campos en tiempo de ejecución.

| Situación | Respuesta en la interfaz |
| --- | --- |
| 401 del login público | Correo/contraseña incorrectos; no invalida otra sesión por ese rechazo |
| 401 con token vigente | Borra token, informa al contexto y redirige al login con aviso |
| 403, 404, 422, 429 | Mensaje según permiso, recurso, validación o límite |
| 5xx, incluido HTML del proxy | Servicio indisponible; no muestra trazas |
| Red o API detenida | Aviso de conexión/servicio y Reintentar |
| Tiempo agotado o cambio de vista | Mensaje de demora o cancelación silenciosa, respectivamente |

No se reintentan escrituras automáticamente. Un 401 antiguo no elimina una sesión nueva: el token de la solicitud se compara con el actual antes de invalidarlo.

## Autenticación y almacenamiento

AuthProvider mantiene identidad y comprobación. El token permanece en memoria y sessionStorage bajo `equipo21.accessToken`. Si el almacenamiento está bloqueado, funciona en memoria durante la visita. No se conservan contraseñas. sessionStorage permite recargar la misma pestaña sin persistencia deliberada entre sesiones del navegador. El token es accesible a JavaScript y esta elección no protege frente a XSS; el alcance no incorpora cookies HttpOnly.

Al recargar, GET /auth/me valida con el servidor antes de mostrar contenido protegido. Sin identidad se redirige al login conservando el destino interno. El acceso correcto vuelve al destino o al panel. Un fallo temporal de red al recuperar el perfil conserva el token y permite reintentar, sin revelar la vista protegida antes de verificar. El 401 elimina la sesión. El backend determina expiración e inactividad; React no extiende ni valida por su cuenta el JWT.

El cierre solicita revocación y limpia el estado local incluso si falla la red. En ese caso no se garantiza revocación remota hasta expirar; la tarea no exige logout completo. La autorización sigue en el servidor: una ruta protegida de React no reemplaza permisos.

## Entorno y datos

Verificado con Node 24.17.0, React 19.3.1, Vite 8.3.5, TypeScript 7.0.2, Python 3.12.16 y PostgreSQL 17.11 con ICU. API local 8000; frontend 5173 (5174 en la toma de arranque); base 55432.

Vite reenvía /api al backend sin ampliar CORS. Producción requiere un proxy real o configuración de orígenes y HTTPS. No se incluyen archivos .env, credenciales, tokens ni base local en Git/ZIP.

`backend/scripts/prepare_frontend_demo.py` usa una cuenta Administrador ficticia local, el endpoint idempotente de demostración y PATCH de campos para nombrar cinco elementos. Hay objetivos, proyectos, capacidades, procesos y aplicaciones. Postman puede agregar otra capa ficticia; por eso los catálogos pueden variar entre capturas.

## Verificación ejecutada

- **14 pruebas frontend:** nueve del cliente con servidor HTTP local de prueba, tres de componentes y dos de sesión. Cubren bearer, login público, 401, 503 HTML, formato, timeout, cancelación, red y recuperación de perfil.
- **50 pruebas existentes del backend** contra PostgreSQL de pruebas aislado.
- **Postman contra API real:** seis solicitudes, 22 aserciones y cero fallos. Sin publicación de credenciales o resultados en un workspace externo.
- Construcción de producción correcta. Revisión estática sin errores y con cinco advertencias de Fast Refresh/actualizaciones de estado en efectos, conservadas en frontend_lint.txt.
- Chrome: validación vacía, credenciales erróneas, login, panel, elementos, búsqueda vacía, detalle y recuperación tras detener/reiniciar el servicio. Protección de rutas y navegación móvil verificadas.

Reportes en evidencias: frontend_vitest.xml, backend_pytest.xml, postman_auth.txt y cobertura_operaciones.json. Capturas de login rechazado, panel, detalle, vacío, error y carga.

`flujo_auth.mp4` y `flujo_e2e.mp4` duran menos de 30 segundos. Se grabaron con Google Vids y se extrajeron los tramos pertinentes, a velocidad normal y sin audio. La carga es breve por usar una API local; carga.jpg conserva el estado visible de esa solicitud real. Duración/origen en evidencias/videos.json.
