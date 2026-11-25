# Consolidación de diseños — Equipo 21

Fecha: 25 de octubre de 2026. Fuentes individuales originales conservadas en `insumos/`, con hashes SHA-256 en `insumos/manifest.json`. Línea base funcional: `insumos/SRS_equipo.md` (19 RF, 56 criterios canónicos). Las resoluciones siguientes documentan las decisiones técnicas aplicadas en la implementación.

## Aportaciones de cada integrante

| Integrante | OpenAPI | Clases | Arquitectura |
|---|---|---|---|
| Gregorio Escobedo | 41 operaciones; recursos en español; separación de propuestas y relaciones; extensiones `x-roles` y trazabilidad | Valores tipados, autoría, versión de relación y conservación histórica | FastAPI, React/Vite, PostgreSQL y monolito modular |
| Jean Paul Lozano | Contrato 1.1.0, catálogo de criterios, semántica detallada de decisiones e idempotencia | `Cuenta`, jerarquía de valores y `DecisionPropuesta` separada | Contenedores explícitos con FastAPI/PostgreSQL y transacciones |
| Liciel | Recursos en inglés, correo de acceso, `GET /users/me`, errores Problem JSON y ETag/If-Match | Correo, sesiones con hash de token, asignación por capa y propuesta de valores JSON | Módulos de autenticación, autorización, configuración, mapas y bitácora; despliegue y secretos externos |

El inventario completo de operaciones por fuente está en `insumos/comparacion_operaciones.json`. El `.txt` recibido de Liciel contiene YAML; se conserva su contenido como `insumos/liciel/openapi.yaml`. Sus diagramas se recibieron como PNG y se utilizaron como fuentes visuales, sin afirmar que fueran archivos editables.

## OpenAPI: consenso, diferencias y resoluciones

Los tres contratos cubren cuentas y sesiones, capas, tipos, campos, elementos, tipos de relación, propuestas, relaciones validadas, mapas, bitácora y demostración. La comparación se hace por propósito funcional: nombres diferentes de recursos no significan automáticamente una función ausente.

| Tema / conflicto o gap | Resolución y motivo |
|---|---|
| `/usuarios` (Gregorio), `/cuentas` (Jean Paul), `/users` (Liciel) | `/api/v1/usuarios`, con `correo` y `nombre`; se conserva la convención en español de dos propuestas y el correo requerido en A2. |
| Identificador de acceso genérico o usuario frente a correo | Correo normalizado, único sin distinguir mayúsculas; contraseña individual con hash. Cambian las entradas y salidas del contrato consolidado. |
| Roles `Administrador/Editor/Consulta`, mayúsculas completas o `admin/editor/viewer` | Se usan los tres términos del SRS: `Administrador`, `Editor`, `Consulta`. Se leen del servidor y se conserva edición por capa. |
| `/propuestas-relacion`, `/propuestas`, `/relationship-proposals` | Se adopta `/api/v1/propuestas-relacion`; la decisión es una operación separada y no una escritura directa sobre una relación. |
| Cierre de sesión 200 frente a 204 | 200 con mensaje JSON; revocación de una sola sesión. El alias histórico de login en `/v1/sesiones` conserva 201; `/auth/login` devuelve 200 por la consigna A2. |
| Ningún contrato individual incluye exactamente el registro/login/me de A2 | Se añaden `/api/auth/register`, `/api/auth/login`, `/api/auth/me`. El registro público es una extensión académica explícita, con rol Consulta fijo y sin elección de privilegios. La administración de roles sigue reservada al Administrador. |
| `BearerToken`, `bearerAuth` y exigencia `BearerAuth` | Se consolida el nombre `BearerAuth` y se aplica de forma explícita a cada operación protegida. Es un nombre del esquema OpenAPI, no un algoritmo diferente. |
| `GET /users/me` en Liciel; consulta de sesión en Gregorio y Jean Paul | Se conserva consulta de sesión y se incorpora `GET /api/auth/me`, que devuelve la identidad actual sin metadatos secretos. |
| Lectura individual de campo en Jean Paul frente a listado en Gregorio | Se incorpora GET del campo para dar un URI consultable a la definición creada. |
| Problem JSON y `x-required-roles` de Liciel frente a Error JSON y `x-roles` | Se elige `{codigo,mensaje,detalles}` y `x-roles`, aplicados también al código; se evita mantener dos formatos de error o dos matrices de permisos. |
| ETag/If-Match solo en Liciel | No se incorpora un mecanismo parcial: se utilizan transacciones, restricciones persistentes, versión de relaciones y serialización de escrituras. No se anuncia control optimista HTTP que el código no implemente. |
| DELETE de elemento o subrecurso de estado | DELETE realiza baja lógica idempotente; PATCH con `estado: activo` reactiva. No se borran físicamente elementos ni relaciones. |
| Demostración POST frente a PUT | PUT identificado por versión de muestra; 201 al crear, 200 en repeticiones, con los mismos IDs y sin recargar datos existentes. |
| Extensiones de criterios con nombres coincidentes entre SRS individuales | Solo se usan IDs del SRS canónico del equipo; se conservan los 56 criterios, sin atribuir pruebas de interfaz o rendimiento al backend. |
| Patrones `\\S` doblemente escapados en el YAML de Gregorio | Se corrige a `\S`, que expresa texto con al menos un carácter no blanco. Se verifica con solicitudes reales. |

## Clases: consenso, diferencias y resoluciones

| Tema | Resolución |
|---|---|
| `Usuario` / `Cuenta` | Clase persistente Usuario; API `/usuarios`; `correo` y `nombre` públicos, hash interno. |
| Permiso / asignación de edición | Tabla de asignaciones actuales única por (usuario,capa), con asignador y fecha; la bitácora conserva su historial al reemplazar el conjunto. |
| Valor abstracto y cuatro subclases (Jean Paul), tabla tipada (Gregorio), JSON en Elemento (Liciel) | Una tabla `valores_campo`, con un valor exclusivo de texto/número/fecha/opción, unicidad por elemento/campo y trigger que comprueba la definición. Nombre se deriva del campo base; la columna de búsqueda se mantiene en el mismo servicio/transacción. |
| Opciones como entidad o JSON | `opciones_campo` con identidad, etiqueta, orden y estado interno activo. Reemplazar opciones conserva las anteriores inactivas; el tipo queda bloqueado al tener elementos. |
| Decisión separada o atributos dentro de propuesta | Se adopta la entidad separada de Jean Paul, una por propuesta. La respuesta pública proyecta `decisorId` y `decididaEn` para compatibilidad con el contrato. |
| Autoría repetida o clase abstracta | Se reutiliza un mixin de autoría en código; sus columnas se materializan en elementos y relaciones. Una clase abstracta sin identidad propia no crea una tabla vacía. |
| Estado de elemento activo/baja o enum alternativo | `activo` / `baja`; la identidad y referencias se conservan. Relaciones usan `vigente` / `retirada`. |
| Token completo, hash de token o solo identificador | Se guarda SHA-256 del JWT y sus metadatos de sesión; el JWT completo no se guarda. Firma, expiración, identificadores y hash deben coincidir. |
| Identidad de la carga de muestra no explícita | Se añade `cargas_demostracion`, necesaria para garantizar que el PUT no duplica la muestra. |

`diagrama_clases_equipo.puml` representa las 15 clases persistentes y todos los atributos del modelo físico, con nombres camelCase. Los campos internos no se publican automáticamente en los schemas de respuesta; esa separación se detalla en la revisión SQL.

## Arquitectura

Se conserva el monolito modular común a las tres propuestas. FastAPI/PostgreSQL y React/Vite están especificados en los diseños de Gregorio y Jean Paul y concretan los contenedores genéricos de Liciel. Se integran de Liciel la autorización por rol y capa, los módulos explícitos y la configuración por entorno. La vista consolidada distingue contenedores de componentes internos, ya que su PNG mezcla ambos niveles pese a titularse C4 Container Level. El despliegue cloud y la terminación HTTPS se documentan como diseño; estas actividades se verifican localmente.

## Alcance de las dos etapas

S05-S06-A1 valida esquema y CRUD en una instantánea temporal sin seguridad, limitada a loopback. S05-S06-A2 añade registro, login, perfil, verificación JWT y políticas a las rutas del mismo contrato. La versión final solo arranca la API protegida; no incluye un parámetro de entorno para deshabilitar autenticación.
