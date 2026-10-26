# Revisión de autenticación y protección de rutas

Fecha: 25 de octubre de 2026. Backend FastAPI, PostgreSQL 17 y contrato consolidado `../S05_S06_A1/openapi_equipo.yaml` versión 2.0.0. Se ejecutaron verificaciones contra la API y una base de pruebas independiente.

## Módulo de autenticación

| Requisito / revisión | Implementación y evidencia |
|---|---|
| POST /api/auth/register | 201, correo normalizado, nombre y contraseña. bcrypt coste 12. Respuesta Usuario sin contraseña ni hash. Registro público crea Consulta; intentar inyectar rol devuelve 422. |
| POST /api/auth/login | Correo y contraseña; 200 con `accessToken`, tipo Bearer y expiración. Contraseña incorrecta o cuenta inactiva devuelve 401 con mensaje genérico. |
| GET /api/auth/me | JWT Bearer válido; devuelve la identidad actual del servidor. Sin token o inválido → 401. |
| Expiración explícita | JWT incluye exp e iat. JWT_EXPIRATION configurable entre 1 y 28800 segundos; sesión vence además tras 30 minutos de inactividad. |
| Secret externo | JWT_SECRET obligatorio por entorno, mínimo 32 bytes, sin valor funcional en código. `.env.example` contiene placeholders. Archivos reales solo locales e ignorados por Git. |
| Firma y claims | Solo HS256; firma, exp, iat, iss, aud, sub, sid y jti obligatorios. También se comprueban usuario, estado, sesión persistida, hash del token y revocación. |
| Persistencia de sesión | Se almacena SHA-256 del JWT, sin token completo. Cierre individual revoca esa sesión; cambio de rol, desactivación y restablecimiento revocan las de la cuenta. |
| Autorización | Rol y capas se consultan en BD; el cliente no elige privilegios por claims. Admin administra catálogos/cuentas y decide propuestas; Editor modifica solo sus capas; Consulta lee. |

Los endpoints usan `correo` y `contrasena` conforme a la convención del contrato en español. El alias heredado POST `/api/v1/sesiones` conserva 201; el login exigido en A2 devuelve 200.

## Hallazgos y correcciones

1. Los diseños originales tenían nombres diferentes para el esquema Bearer. Se unificaron como `BearerAuth`, definido en `components.securitySchemes` y referenciado por cada operación protegida.
2. El registro no estaba presente con la ruta académica en las fuentes. Se añadió con privilegio Consulta fijo; los roles y asignaciones solo se modifican desde rutas administrativas autenticadas.
3. bcrypt tiene límite de 72 bytes: se valida explícitamente longitud UTF-8, además del mínimo de 10 caracteres, y se devuelve 422. No se trunca una contraseña silenciosamente.
4. Se evita distinguir correo inexistente por el costo de bcrypt mediante hash ficticio de comparación. Esto no constituye una medición formal de resistencia a ataques de tiempo.
5. No se confía en roles del JWT; se consulta la cuenta en cada solicitud y se revocan sesiones ante cambios relevantes. Se protege al último Administrador activo.
6. Se prueban firma alterada, algoritmo distinto, audiencia incorrecta, claims faltantes, expiración, identificadores mal formados, inactividad y revocación; todos rechazan con 401. Una revocación individual conserva otra sesión válida.
7. Respuestas de validación y errores internos omiten contraseñas, hashes, encabezados Authorization y SQL parametrizado. La bitácora guarda cambios de dominio y excluye secretos. Se añaden `Cache-Control: no-store`, `X-Content-Type-Options: nosniff` y desafío `WWW-Authenticate: Bearer` en 401.
8. El token solo se entrega en login; el registro y las altas administrativas nunca lo devuelven. Se separan las variables privadas de Postman de las colecciones compartidas.

## Protección de rutas

A = Administrador; E = Editor; C = Consulta. Todas las rutas de la tabla requieren JWT. En escrituras de elementos y propuestas, E también requiere asignación a la capa correspondiente; no basta con su rol. Las 42 operaciones protegidas se prueban automáticamente sin token y con token inválido. Los estados de éxito se verificaron con datos válidos y rol permitido en la suite integral; no se afirma haber ejecutado manualmente cada fila.

| Método y ruta protegida | Roles | Éxito según contrato | Sin token / inválido (suite) |
|---|---|---|---|
| GET `/api/v1/sesiones/actual` | A/E/C | 200 | 401 / 401 |
| DELETE `/api/v1/sesiones/actual` | A/E/C | 200 | 401 / 401 |
| GET `/api/v1/usuarios` | A | 200 | 401 / 401 |
| POST `/api/v1/usuarios` | A | 201 | 401 / 401 |
| GET `/api/v1/usuarios/{usuarioId}` | A | 200 | 401 / 401 |
| PATCH `/api/v1/usuarios/{usuarioId}` | A | 200 | 401 / 401 |
| POST `/api/v1/usuarios/{usuarioId}/restablecimientos-contrasena` | A | 201 | 401 / 401 |
| GET `/api/v1/usuarios/{usuarioId}/capas-editables` | A | 200 | 401 / 401 |
| PUT `/api/v1/usuarios/{usuarioId}/capas-editables` | A | 200 | 401 / 401 |
| GET `/api/v1/capas` | A/E/C | 200 | 401 / 401 |
| POST `/api/v1/capas` | A | 201 | 401 / 401 |
| GET `/api/v1/capas/{capaId}` | A/E/C | 200 | 401 / 401 |
| PATCH `/api/v1/capas/{capaId}` | A | 200 | 401 / 401 |
| GET `/api/v1/tipos-elemento` | A/E/C | 200 | 401 / 401 |
| POST `/api/v1/tipos-elemento` | A | 201 | 401 / 401 |
| GET `/api/v1/tipos-elemento/{tipoId}` | A/E/C | 200 | 401 / 401 |
| PATCH `/api/v1/tipos-elemento/{tipoId}` | A | 200 | 401 / 401 |
| GET `/api/v1/tipos-elemento/{tipoId}/campos` | A/E/C | 200 | 401 / 401 |
| POST `/api/v1/tipos-elemento/{tipoId}/campos` | A | 201 | 401 / 401 |
| PUT `/api/v1/tipos-elemento/{tipoId}/campos/{campoId}` | A | 200 | 401 / 401 |
| GET `/api/v1/tipos-elemento/{tipoId}/campos/{campoId}` | A/E/C | 200 | 401 / 401 |
| GET `/api/v1/elementos` | A/E/C | 200 | 401 / 401 |
| POST `/api/v1/elementos` | A/E | 201 | 401 / 401 |
| GET `/api/v1/elementos/{elementoId}` | A/E/C | 200 | 401 / 401 |
| PATCH `/api/v1/elementos/{elementoId}` | A/E | 200 | 401 / 401 |
| DELETE `/api/v1/elementos/{elementoId}` | A/E | 200 | 401 / 401 |
| GET `/api/v1/tipos-relacion` | A/E/C | 200 | 401 / 401 |
| POST `/api/v1/tipos-relacion` | A | 201 | 401 / 401 |
| GET `/api/v1/tipos-relacion/{tipoRelacionId}` | A/E/C | 200 | 401 / 401 |
| PATCH `/api/v1/tipos-relacion/{tipoRelacionId}` | A | 200 | 401 / 401 |
| GET `/api/v1/propuestas-relacion` | A/E/C | 200 | 401 / 401 |
| POST `/api/v1/propuestas-relacion` | A/E | 201 | 401 / 401 |
| GET `/api/v1/propuestas-relacion/{propuestaId}` | A/E/C | 200 | 401 / 401 |
| PATCH `/api/v1/propuestas-relacion/{propuestaId}` | A/E | 200 | 401 / 401 |
| POST `/api/v1/propuestas-relacion/{propuestaId}/decisiones` | A | 201 | 401 / 401 |
| GET `/api/v1/relaciones` | A/E/C | 200 | 401 / 401 |
| GET `/api/v1/relaciones/{relacionId}` | A/E/C | 200 | 401 / 401 |
| GET `/api/v1/mapas/{elementoId}` | A/E/C | 200 | 401 / 401 |
| GET `/api/v1/entradas-bitacora` | A/E/C | 200 | 401 / 401 |
| GET `/api/v1/entradas-bitacora/{entradaId}` | A/E/C | 200 | 401 / 401 |
| PUT `/api/v1/demostraciones/arquitectura-ficticia-v1` | A | 201/200 | 401 / 401 |
| GET `/api/auth/me` | A/E/C | 200 | 401 / 401 |

Operaciones públicas explícitas: POST `/api/auth/register`, POST `/api/auth/login`, POST `/api/v1/sesiones` y GET `/api/salud`. `/docs`, `/redoc` y `/openapi.json` exponen documentación, sin datos privados. La etapa A1 es una copia temporal independiente; el backend final no tiene un interruptor para quitar autenticación.

### Pruebas desde terminal

Se ejecutó curl real con POST `/api/v1/capas` y un mismo cuerpo válido. El token inválido se generó cambiando un carácter de su firma. Los valores de tokens se suministraron mediante archivos locales de cabeceras y no se incluyen en el reporte.

| Caso | Esperado | Observado |
|---|---|---|
| Sin Authorization | 401 | 401 |
| Firma alterada | 401 | 401 |
| JWT de Consulta | 403 | 403 |
| JWT de Administrador | 201 | 201 |

Respuestas completas sanitizadas: `evidencias/pruebas_terminal.json`. Reproducción: `backend/scripts/prepare_postman_runtime.py` y `backend/scripts/check_terminal_security.py` desde la raíz, con API local activa y cuentas ficticias provisionadas.

## Postman y suite de integración

- Recorrido A2: 6 peticiones, 22 aserciones, 0 fallas; registro 201 → login 200 → me 200 → POST capa 201 → sin token 401 → Consulta 403.
- Colección adicional de firma alterada: 1 petición, 3 aserciones, 0 fallas.
- pytest sobre PostgreSQL real aislado: 50 pruebas aprobadas, incluidas las 46 operaciones con validación de respuesta contra OpenAPI, roles/capas, revocación, duplicados concurrentes e integridad SQL. El reporte conserva una advertencia de deprecación de la dependencia de TestClient; no afectó las aserciones.
- Evidencias: `evidencias/pytest.xml`, `evidencias/cobertura_operaciones.json`, `evidencias/postman_auth_salida_final.txt`, `evidencias/postman_firma.txt` y `evidencias/pruebas_terminal.json`.

El registro crea Consulta y la colección provista inicia sesión con un Administrador ficticio previamente provisionado para demostrar una escritura administrativa y el rechazo 403. En esa colección, el token de GET /auth/me y de la escritura procede del login del paso 2. La cuenta Consulta usada en el último paso tiene su propio token, preparado antes de grabar. No se eleva el rol del usuario registrado para facilitar la demostración.

## Alcance y video incorporado

Se incorporó `pruebas_auth.mp4` proporcionado por Gregorio, con duración de 46.40 segundos. Su tamaño, duración y SHA-256 están en `evidencias/video_recibido.json`. El video recibido utiliza login de la cuenta Consulta registrada y un token administrativo preparado antes del flujo para la escritura. La revisión visual requiere repetir la toma: se muestran Test Results en lugar de los JSON y no se ve accessToken en la respuesta del login. El guion, las colecciones y las evidencias complementarias permanecen en esta carpeta.

Se verificó ejecución local con PostgreSQL nativo. HTTPS y una cuenta de BD limitada deben configurarse en el despliegue; no se anuncia un despliegue público ni una auditoría de penetración. No se midieron carga o límites de intentos de login en esta actividad. Referencias técnicas: [JWT con FastAPI](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) y [variables de Postman](https://learning.postman.com/docs/sending-requests/variables/variables/).
