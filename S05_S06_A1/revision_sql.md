# Revisión del esquema y del código CRUD

Fecha: 25 de octubre de 2026. Motor ejecutado: PostgreSQL 17.11. Python 3.12, FastAPI, SQLAlchemy y psycopg. Esta revisión registra verificaciones realizadas sobre la implementación; el equipo conserva la responsabilidad de revisar y aceptar la consolidación.

## Correspondencia entre diseño, API y SQL

Se importó `esquema_bd.sql` en una base PostgreSQL real con `psql -v ON_ERROR_STOP=1`. Se verificaron 15 tablas, 15 claves primarias, 29 claves foráneas y 45 índices, incluidos los índices que respaldan restricciones. El inventario está en `evidencias/validacion_estructura.json` y la consulta del catálogo en `evidencias/catalogo_postgresql.txt`.

| Clases / tablas | Representación y restricciones revisadas |
|---|---|
| Usuario / usuarios | UUID, correo normalizado único, nombre obligatorio, bcrypt interno, rol y estado válidos. Correo sin distinguir mayúsculas. |
| Sesion / sesiones | Usuario 1:N sesiones; hash del token único, fechas de creación, actividad, expiración y revocación. El JWT completo no se almacena. |
| Capa / capas; Permiso / permisos_edicion_capa | Nombre de capa único sin distinguir mayúsculas; asignación única por usuario/capa, con autor y fecha. |
| TipoElemento / tipos_elemento | Pertenece a una capa; nombre único dentro de ella. |
| Campo / definiciones_campo | Pertenece a un tipo; tipo de dato, obligatoriedad y marca de Nombre base. Índices parciales garantizan un único Nombre por tipo. |
| Opcion / opciones_campo | Pertenece a un campo; etiqueta, orden y estado. Opciones reemplazadas se conservan inactivas. |
| Elemento / elementos; Valor / valores_campo | Un valor por elemento/campo; exactamente una columna de texto, número, fecha u opción; FK a elemento, campo y opción. |
| TipoRelacion / tipos_relacion | FK a tipos de origen y destino; nombre único y restricciones de compatibilidad en el servicio. |
| Relacion / relaciones_validadas | FK a extremos, tipo y autor; versión y estado; unicidad de vínculo vigente. |
| Propuesta / propuestas_relacion | Autor, extremos, operación y relación objetivo opcional según operación; estado, justificación y versión esperada. |
| Decision / decisiones_propuesta | Una decisión por propuesta mediante UNIQUE; decisor, resolución y fecha. |
| Bitacora / entradas_bitacora | Actor, acción, fecha e instantáneas JSONB; trigger impide UPDATE y DELETE ordinarios. |
| CargaDemostracion / cargas_demostracion | Identificador de muestra único y resultado persistente para PUT idempotente. |

El diagrama de clases presenta atributos camelCase equivalentes a las columnas snake_case. Los schemas públicos son proyecciones del dominio: excluyen hashes y metadatos internos; valores y decisiones se anidan en respuestas. Nombre del elemento se deriva del campo base y se mantiene como columna de búsqueda en la misma transacción. Las opciones y decisiones tienen tablas propias, aunque aparezcan anidadas en JSON. No se equipara cada schema de request con una tabla.

## Hallazgos y correcciones al SQL

| Hallazgo | Corrección y comprobación |
|---|---|
| Diferencias entre valores JSON, subclases y tabla de valores de las fuentes | Tabla tipada con CHECK de exclusión y trigger de compatibilidad con definición, tipo del elemento y opción seleccionada. Se conservan FK consultables. |
| Ausencia de una entidad explícita para la idempotencia de demostración | Tabla `cargas_demostracion`; repetir PUT devuelve 200 y los mismos IDs, sin duplicar. |
| UNIQUE simple distinguía mayúsculas en nombres | Índices funcionales `lower(...)` y nombres con colación ICU `und-x-icu`. Se detectó que `locale=C` no convertía correctamente Á mayúscula; se corrigió y se verificó Árbol/árbol → 409 y búsqueda ÁRBOL por árbol. No se promete búsqueda sin acentos. |
| Riesgo de duplicar vínculo o propuesta pendiente | Índices únicos parciales más revalidación transaccional y serialización de escrituras. |
| Ediciones de catálogos podían destruir valores históricos | Se bloquea modificar estructuras con elementos y se conservan opciones previas inactivas; no hay cascadas de borrado de negocio. |
| Bitácora modificable por SQL ordinario | Trigger de inmutabilidad y ausencia de endpoints de edición. No protege contra el propietario/superusuario del motor; la conexión de desarrollo no se presenta como cuenta limitada de producción. |
| Números no finitos y longitudes sin límite coherente | Restricciones para números finitos y límites compartidos entre contrato, validación y almacenamiento. |

UUID se usa para identidades; `timestamptz` para instantes; `date` para campos de fecha; booleanos reales para estados lógicos internos; texto limitado para nombres/correos; números de doble precisión como el schema number; JSONB solo para instantáneas y resultado de muestra. Los estados y roles se restringen con CHECK. Las FK usan referencias conservadoras; la baja de elementos es lógica.

## Correcciones al código generado

- Las rutas y métodos se registran desde el contrato consolidado. Los estados y errores se ajustaron a sus schemas; el restablecimiento de contraseña devuelve una entrada de bitácora, como especifica el contrato, sin devolver credenciales.
- Se corrigieron patrones de texto doblemente escapados (`\\S` frente a `\S`), validación de cuerpos con propiedades desconocidas y formatos de correo/UUID/fecha. JSON mal formado → 400; media type incorrecto → 415; datos inválidos → 422; inexistente → 404; conflicto persistente → 409.
- Se añadieron límites de 1 MiB (413), manejo seguro de indisponibilidad de BD (503), Location en creaciones y mensajes sin valores sensibles.
- Se confirmó la transacción antes de enviar la respuesta y se revierte ante errores; escritura y bitácora son atómicas.
- Una prueba concurrente detectó bloqueo del bucle ASGI al esperar el bloqueo asesor desde una llamada SQL síncrona. Se trasladó SQL/servicios al pool de hilos; dos altas con el mismo nombre terminan en una 201 y una 409.
- El diagrama y DDL se regeneraron desde el modelo corregido; OpenAPI se actualizó con los mismos límites, campos y respuestas. Los 56 IDs de criterios canónicos se conservaron; la trazabilidad no significa que todos los RNF o pantallas estén probados.

## Ejecución y resultados

La prueba A1 se ejecutó en una copia local de la etapa CRUD, sin autenticación, en `127.0.0.1:8001` y base separada `arquitectura21_a1`. La aplicación final A2 usa puerto 8000 y base `arquitectura21`, con seguridad. El script `backend/scripts/prepare_a1_demo.py` permite reproducir la copia A1 sin cambiar el arranque final.

| Secuencia Postman A1 | Esperado / observado | Verificación |
|---|---|---|
| POST /api/v1/capas | 201 / 201 | ID de capa devuelto |
| GET /api/v1/capas/{id} | 200 / 200 | Mismo ID después de crear |
| POST /api/v1/tipos-elemento | 201 / 201 | Tipo y campo Nombre base |
| POST /api/v1/elementos | 201 / 201 | Valor tipado persistido |
| GET /api/v1/elementos/{id} | 200 / 200 | Nombre y valor recuperados |
| DELETE /api/v1/elementos/{id} | 200 / 200 | Estado baja; identidad conservada |

Resultado Postman: 6 peticiones, 21 aserciones, 0 fallas (`evidencias/postman_crud.txt`). La suite final A2 prueba las 46 operaciones, sus respuestas exitosas contra schema y errores de negocio, sobre PostgreSQL aislado; resultado: 50 pruebas aprobadas. Evidencias en `../S05_S06_A2/evidencias/`.

Se incorporó el video `pruebas_postman.mp4` proporcionado por Gregorio, con duración de 50.41 segundos. Su tamaño, duración y SHA-256 están en `evidencias/video_recibido.json`. Docker Compose se incluye como alternativa de reproducción, pero no se ejecutó: la comprobación de persistencia fue con PostgreSQL nativo.
