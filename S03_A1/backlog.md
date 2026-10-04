# Backlog — Plataforma de Arquitectura Empresarial
**Equipo 21 · Basado en `SRS_equipo.md` v1.0**
Cada historia referencia el/los RF del SRS de equipo de los que deriva, para trazabilidad. Story points en escala Fibonacci (1, 2, 3, 5, 8, 13). Este es el backlog ya revisado (ver `ajustes_backlog.md` para el borrador original y los cambios aplicados).

## Resumen de épicas
| Épica | Descripción | RF del SRS de equipo |
|---|---|---|
| E1. Acceso y administración de cuentas | Autenticación, roles y asignación de capas editables | RF-01, RF-02 |
| E2. Configuración del modelo de arquitectura | Capas, tipos de elemento, campos y tipos de relación | RF-03, RF-04, RF-05, RF-09 |
| E3. Captura y ciclo de vida de elementos y relaciones | Alta/edición/baja de elementos y el flujo de propuesta–aprobación de relaciones | RF-06, RF-07, RF-10, RF-11, RF-12, RF-16 |
| E4. Consulta y exploración visual | Búsqueda, mapa de relaciones, filtros y detalle de vínculos | RF-08, RF-13, RF-14, RF-15 |
| E5. Trazabilidad y continuidad de los datos | Autoría, bitácora, datos de demostración y persistencia | RF-17, RF-18, RF-19 |

---

## Épica 1 — Acceso y administración de cuentas

### US-01 — Inicio de sesión
**Como** usuario con una cuenta activa, **quiero** iniciar sesión con mis credenciales, **para** acceder a las funciones que corresponden a mi rol.
- **AC-1:** Dado que tengo una cuenta activa y credenciales correctas, cuando inicio sesión, entonces se crea mi sesión y el sistema reconoce mi rol (RF-01-AC-1).
- **AC-2:** Dado que escribo una contraseña incorrecta, cuando intento iniciar sesión, entonces no se crea ninguna sesión ni se me muestra información protegida (RF-01-AC-2).
- **Story points:** 3 — **Prioridad:** Alta

### US-02 — Cierre de una sesión individual
**Como** usuario autenticado con varias sesiones abiertas, **quiero** cerrar una de ellas, **para** proteger mi cuenta en un dispositivo compartido sin afectar mis otras sesiones.
- **AC-1:** Dado que tengo dos sesiones válidas A y B, cuando cierro A, entonces A deja de autorizar solicitudes (RF-01-AC-3).
- **AC-2:** Dado que cerré A, cuando uso B para consultar un elemento, entonces la consulta se autoriza normalmente (RF-01-AC-3).
- **Story points:** 2 — **Prioridad:** Media

### US-03 — Alta de cuentas con rol y capas editables
**Como** administrador, **quiero** crear una cuenta, asignarle un rol y, si es Editor, las capas que puede editar, **para** controlar quién puede modificar cada parte del modelo.
- **AC-1:** Dado que existe la capa Aplicaciones, cuando creo una cuenta de Editor y le asigno esa capa, entonces puede crear elementos en Aplicaciones pero no en Negocio (RF-02-AC-1).
- **AC-2:** Dado que una cuenta de Editor no tiene capas asignadas, cuando intenta crear un elemento, entonces la operación se rechaza (SRS de equipo §2.3; RF-06-AC-3).
- **Story points:** 5 — **Prioridad:** Alta

### US-04 — Cambio de rol con protección del último administrador
**Como** administrador, **quiero** cambiar el rol de una cuenta, **para** ajustar sus permisos cuando cambian sus responsabilidades, sin dejar el sistema sin administrador.
- **AC-1:** Dado que un Editor tiene dos sesiones abiertas, cuando le cambio el rol a Consulta, entonces ambas sesiones se invalidan y la cuenta solo puede leer al volver a entrar (RF-02-AC-2).
- **AC-2:** Dado que solo hay un administrador activo, cuando intento quitarle ese rol, entonces la operación se rechaza y sigue habiendo un administrador activo (RF-02-AC-3).
- **Story points:** 3 — **Prioridad:** Media

---

## Épica 2 — Configuración del modelo de arquitectura

### US-05 — Creación de capas
**Como** administrador, **quiero** crear una capa nueva desde la interfaz, **para** organizar información que no cabe en Negocio, Datos, Aplicaciones o Tecnología.
- **AC-1:** Dado que no existe la capa "Seguridad", cuando la creo, entonces queda disponible sin reiniciar la aplicación (RF-03-AC-1).
- **AC-2:** Dado que ya existe "Seguridad", cuando intento crear " seguridad " (mismo nombre normalizado), entonces se rechaza el duplicado (RF-03-AC-2).
- **Story points:** 3 — **Prioridad:** Alta

### US-06 — Definición de tipos de elemento
**Como** administrador, **quiero** crear un tipo de elemento dentro de una capa, **para** modelar los registros que cada área necesita capturar.
- **AC-1:** Dado que existe la capa Negocio, cuando creo el tipo "Proyecto" en ella, entonces queda disponible para registrar elementos (RF-04-AC-1).
- **AC-2:** Dado que un tipo ya tiene elementos, cuando lo renombro, entonces conserva su identificador, sus campos y sus elementos asociados (RF-04-AC-2).
- **Story points:** 3 — **Prioridad:** Alta

### US-07 — Configuración de campos de un tipo
**Como** administrador, **quiero** definir los campos de un tipo de elemento (texto, número, fecha o selección) y marcar cuáles son obligatorios, **para** asegurar que la captura tenga la información mínima necesaria.
- **AC-1:** Dado que un tipo no tiene elementos, cuando guardo campos de los cuatro tipos con su obligatoriedad, entonces se recuperan exactamente como los configuré (RF-05-AC-1).
- **AC-2:** Dado que un tipo ya tiene al menos un elemento, cuando intento agregar o cambiar un campo, entonces la operación se rechaza y la definición no cambia (RF-05-AC-2).
- **Story points:** 5 — **Prioridad:** Alta

### US-08 — Definición de tipos de relación
**Como** administrador, **quiero** definir un tipo de relación indicando qué tipo de elemento puede ser origen y cuál destino, **para** limitar los vínculos a combinaciones que tengan sentido de negocio.
- **AC-1:** Dado que existen los tipos Proyecto y Capacidad, cuando creo "mejora" con origen Proyecto y destino Capacidad, entonces queda disponible para esa combinación y no para la inversa (RF-09-AC-1).
- **AC-2:** Dado que el tipo de destino indicado no existe, cuando intento guardar el tipo de relación, entonces se rechaza la definición (RF-09-AC-2).
- **Story points:** 3 — **Prioridad:** Alta

---

## Épica 3 — Captura y ciclo de vida de elementos y relaciones

### US-09 — Registro de un elemento
**Como** editor con permiso sobre una capa, **quiero** registrar un elemento nuevo con los campos de su tipo, **para** mantener actualizada la información de mi área.
- **AC-1:** Dado que tengo permiso sobre Negocio y existe el tipo Proyecto, cuando registro "Proyecto Alfa" con valores válidos, entonces se guarda con un identificador único (RF-06-AC-1).
- **AC-2:** Dado que un campo obligatorio queda vacío, cuando intento guardar, entonces se identifica el campo y no se crea el elemento (RF-07-AC-1).
- **Story points:** 5 — **Prioridad:** Alta

### US-10 — Modificación de un elemento
**Como** editor autorizado, **quiero** modificar los valores de un elemento existente, **para** corregir o actualizar su información sin perder su identificador.
- **AC-1:** Dado que un elemento tiene descripción "Inicial", cuando guardo "Actualizada", entonces el mismo identificador conserva el nuevo valor (RF-06-AC-2).
- **AC-2:** Dado que envío un valor de tipo incorrecto (texto en un campo numérico), cuando intento guardar, entonces se rechaza la operación completa y se conservan los valores originales (RF-07-AC-2).
- **Story points:** 3 — **Prioridad:** Media

### US-11 — Propuesta de una relación
**Como** editor con permiso sobre la capa del elemento origen, **quiero** proponer un vínculo entre dos elementos existentes con una justificación, **para** documentarlo sin publicarlo de inmediato en el mapa.
- **AC-1:** Dado que existen un Proyecto, una Capacidad y el tipo "mejora" (Proyecto → Capacidad), cuando propongo el vínculo con una justificación de 10 a 500 caracteres, entonces queda una propuesta pendiente y el mapa ordinario aún no la muestra (RF-10-AC-1).
- **AC-2:** Dado que ya existe un vínculo validado o una propuesta pendiente con el mismo origen, tipo y destino, cuando intento repetirla, entonces se rechaza (RF-10-AC-3).
- **Story points:** 5 — **Prioridad:** Alta

### US-12 — Aprobación o rechazo de una propuesta
**Como** administrador, **quiero** aprobar o rechazar una propuesta de relación, **para** que solo los vínculos revisados queden visibles en el mapa.
- **AC-1:** Dado que existe una propuesta pendiente y sus dos elementos siguen activos, cuando la apruebo, entonces se crea una relación validada vigente con decisor y fecha (RF-11-AC-1).
- **AC-2:** Dado que la rechazo, cuando se registra la decisión, entonces no se crea una relación validada y la propuesta queda marcada como rechazada (RF-11-AC-2).
- **AC-3:** Dado que el nuevo origen de una propuesta de cambio fue dado de baja antes de mi decisión, cuando intento aprobarla, entonces se rechaza la aprobación y la relación vigente no cambia (RF-12-AC-4).
- **Story points:** 8 — **Prioridad:** Alta

### US-13 — Cambio o retiro de una relación vigente
**Como** editor con permiso sobre la capa correspondiente, **quiero** proponer un cambio o el retiro de una relación ya validada, **para** mantener el modelo correcto sin modificarlo sin revisión.
- **AC-1:** Dado que existe una relación vigente R, cuando propongo cambiar su justificación o sus extremos, entonces la propuesta queda pendiente y R conserva sus valores vigentes hasta la decisión (RF-12-AC-1).
- **AC-2:** Dado que R tiene una propuesta de retiro pendiente y se aprueba, cuando se consulta R, entonces aparece como "retirada", se conserva para historial y desaparece del mapa ordinario (RF-12-AC-3).
- **Story points:** 5 — **Prioridad:** Media

### US-14 — Baja lógica y reactivación de un elemento
**Como** editor con permiso sobre su capa, **quiero** dar de baja un elemento y poder reactivarlo después, **para** ocultarlo de las consultas ordinarias sin borrar su información ni su historial.
- **AC-1:** Dado que un elemento está activo y tiene relaciones, cuando lo doy de baja, entonces conserva sus campos y relaciones, y deja de aparecer en el listado y el mapa ordinarios (RF-16-AC-1).
- **AC-2:** Dado que un elemento está de baja, cuando lo reactivo, entonces vuelve a aparecer en los resultados ordinarios (RF-16-AC-2).
- **Story points:** 3 — **Prioridad:** Media

---

## Épica 4 — Consulta y exploración visual

### US-15 — Búsqueda de elementos
**Como** usuario autenticado, **quiero** buscar elementos por nombre y ver resultados paginados con su identificador, tipo y capa, **para** encontrar rápidamente el registro que necesito, incluso si hay nombres repetidos.
- **AC-1:** Dado que existen 30 elementos activos, cuando abro el listado sin filtros, entonces la primera página muestra 25 ordenados por nombre e identificador y la segunda muestra 5 (RF-08-AC-1).
- **AC-2:** Dado que existen dos elementos llamados "Proyecto Alfa" con identificadores distintos, cuando busco "alfa", entonces aparecen ambos distinguidos por su identificador (RF-08-AC-2).
- **Story points:** 3 — **Prioridad:** Alta

### US-16 — Exploración del mapa de relaciones
**Como** usuario autenticado, **quiero** abrir el mapa de relaciones directas de un elemento, **para** entender con qué otros elementos está vinculado.
- **AC-1:** Dado que E1 tiene vínculos vigentes con E2 y E3, cuando abro su mapa sin filtros, entonces se muestran E1, E2, E3 y esos dos vínculos con su dirección (RF-13-AC-1).
- **AC-2:** Dado que un elemento tiene más de 99 vecinos directos, cuando abro su mapa, entonces se muestran como máximo 100 nodos y se informa que la vista fue truncada (RF-13-AC-3).
- **Story points:** 5 — **Prioridad:** Alta

### US-17 — Filtros del mapa
**Como** usuario autenticado, **quiero** filtrar el mapa por capa, tipo de elemento o tipo de relación, **para** enfocarme solo en la parte del modelo que me interesa.
- **AC-1:** Dado que E1 se relaciona con elementos de Negocio y Aplicaciones, cuando filtro por la capa de destino Aplicaciones, entonces permanecen E1 y sus vecinos de esa capa (RF-14-AC-1).
- **AC-2:** Dado que hay filtros activos y no han cambiado los datos ni el elemento de partida, cuando los quito, entonces reaparece la vista ordinaria anterior al filtrado (RF-14-AC-3).
- **Story points:** 3 — **Prioridad:** Media

### US-18 — Detalle de un vínculo
**Como** usuario autenticado, **quiero** abrir el detalle de una relación desde el mapa o desde un elemento, **para** conocer su justificación, su estado y los datos de ambos extremos.
- **AC-1:** Dado que existe un vínculo validado de A hacia B, cuando lo selecciono, entonces veo origen, tipo, destino, justificación, estado, autor y fechas (RF-15-AC-2).
- **AC-2:** Dado que estoy en el detalle de la relación, cuando abro la información de A o de B, entonces veo sus campos y valores guardados (RF-15-AC-2).
- **Story points:** 2 — **Prioridad:** Media

---

## Épica 5 — Trazabilidad y continuidad de los datos

### US-19 — Trazabilidad de autor y fecha
**Como** usuario autenticado, **quiero** ver quién creó y quién modificó por última vez un elemento o relación, y cuándo, **para** confiar en la vigencia de la información que consulto.
- **AC-1:** Dado que Ana crea un elemento y Luis lo modifica después, cuando consulto su detalle, entonces veo a Ana como creadora con su fecha y a Luis como último modificador con la fecha del cambio (RF-18-AC-1).
- **AC-2:** Dado que se actualiza el campo "Criticidad" de "Media" a "Alta", cuando se guarda, entonces la bitácora registra actor, fecha, valor anterior y valor nuevo (RF-18-AC-2).
- **Story points:** 3 — **Prioridad:** Media

### US-20 — Carga de datos de demostración
**Como** administrador, **quiero** cargar un conjunto de datos ficticios, **para** probar el recorrido completo del sistema sin capturar todo manualmente.
- **AC-1:** Dado que la instalación no contiene la muestra, cuando ejecuto la carga, entonces existen registros ficticios de las cinco categorías, una capa adicional y relaciones entre al menos dos capas (RF-17-AC-1).
- **AC-2:** Dado que la muestra ya fue cargada, cuando ejecuto la carga otra vez, entonces no se duplican registros y se me informa que ya existe (RF-17-AC-2).
- **Story points:** 2 — **Prioridad:** Media

### US-21 — Recuperación de datos entre sesiones
**Como** usuario autorizado, **quiero** recuperar la configuración, los elementos y las relaciones guardadas al iniciar una sesión nueva, **para** continuar el trabajo sin volver a capturar información.
- **AC-1:** Dado que se guardaron una capa, un tipo con campos, dos elementos y un vínculo validado, cuando abro una sesión nueva sin estado local anterior, entonces recupero sus identificadores, valores y asociaciones (RF-19-AC-1).
- **AC-2:** Dado que se guardaron una asignación de capa y una decisión sobre una propuesta, cuando inicio una sesión nueva, entonces se recuperan la asignación, el estado de la propuesta, el decisor y la fecha (RF-19-AC-2).
- **Story points:** 5 — **Prioridad:** Alta

---

## Resumen de estimación
| Épica | Historias | Story points |
|---|---|---|
| E1. Acceso y cuentas | US-01 a US-04 | 13 |
| E2. Configuración del modelo | US-05 a US-08 | 14 |
| E3. Captura y ciclo de vida | US-09 a US-14 | 29 |
| E4. Consulta y exploración | US-15 a US-18 | 13 |
| E5. Trazabilidad y continuidad | US-19 a US-21 | 10 |
| **Total** | **21 historias** | **79 pts** |

**Prioridad Alta:** US-01, US-03, US-05, US-06, US-07, US-08, US-09, US-11, US-12, US-15, US-16, US-21 (12 historias; incluyen el tipo de relación y la persistencia necesarios para el recorrido principal).

**Prioridad Media:** US-02, US-04, US-10, US-13, US-14, US-17, US-18, US-19, US-20 (9 historias).

**Prioridad Baja:** ninguna en esta versión; las 21 historias derivan del alcance comprometido en el SRS de equipo.
