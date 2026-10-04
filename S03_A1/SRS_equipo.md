# Especificación de Requerimientos de Software

**Plataforma de Arquitectura Empresarial**  
**Versión:** 1.0 definitiva recomendada para la primera entrega  
**Fecha:** 1 de octubre de 2026  
**Estado:** especificación conjunta con alcance y reglas cerrados para la primera entrega. Sustituye las decisiones incompatibles de los tres borradores individuales dentro de esta propuesta de integración.

## 1. Introducción

### 1.1 Propósito del documento

Este documento especifica la primera versión de una plataforma web para registrar y explorar información de arquitectura empresarial. Está dirigido al equipo de desarrollo, al docente y a las personas que validarán el producto. Servirá para diseñar la API y la interfaz, preparar datos de demostración y derivar pruebas observables.

La estructura sigue la organización simplificada de IEEE 830 utilizada en S02-A1: introducción, descripción general y requerimientos específicos. Esta versión integra el núcleo compartido por los SRS de Gregorio, Liciel y Jean Paul y resuelve sus conflictos de manera explícita. Las decisiones de integración son reglas de este SRS, sin atribuirlas retroactivamente al cliente.

**Convención de identificadores.** Los tres documentos originales reutilizan identificadores como `RF-01` y `RF-01-AC-1` para comportamientos diferentes. Por esa colisión, este documento establece una **serie canónica del equipo**: cada `RF-XX-AC-Y` identifica un solo criterio dentro de este SRS. Los IDs originales no se trasladan automáticamente ni se presentan como equivalentes. Los IDs canónicos no se renumerarán ni se reutilizarán; un criterio nuevo recibirá el siguiente número de su RF y uno retirado conservará su ID y su motivo en el registro de cambios. La tabla de procedencia en 3.4 permite rastrear cada RF a las versiones individuales.

### 1.2 Alcance del sistema

La organización necesita consultar, en un lugar común, qué objetivos, proyectos, capacidades, procesos y aplicaciones tiene y cómo se relacionan. Hoy esa información puede estar repartida entre archivos y áreas. La plataforma permitirá configurar capas y tipos de elemento, capturar registros y vínculos explícitos, revisar las propuestas de vínculo y explorar el resultado en un mapa interactivo.

La primera entrega se desarrollará dentro del periodo académico de 12 semanas. Comprende una aplicación web para computadora con cuentas locales, tres roles, edición asignada por capa, cuatro tipos iniciales de campo, persistencia en base de datos, búsqueda, mapas filtrables, aprobación de relaciones, baja lógica de elementos y una bitácora de operaciones relevantes. La demostración utilizará exclusivamente datos ficticios.

Quedan fuera de esta entrega las perspectivas y subniveles jerárquicos, la administración de permisos por elemento, los roles configurables, el inicio de sesión federado, la eliminación física de registros, la edición en tiempo real, la importación masiva, la sincronización automática con sistemas empresariales, los diagnósticos automáticos y la inteligencia artificial. Estas funciones son candidatas para versiones posteriores; su exclusión no implica que carezcan de valor.

### 1.3 Definiciones y acrónimos

| Término | Significado |
| --- | --- |
| SRS | Especificación de Requerimientos de Software. |
| RF, RNF, RD | Requerimiento funcional, no funcional y de dominio, respectivamente. |
| AC | Criterio de aceptación con identificador estable. |
| Capa | Agrupación superior de información; inicialmente Negocio, Datos, Aplicaciones y Tecnología. |
| Tipo de elemento | Definición asociada a una capa que determina qué campos tienen sus registros. |
| Elemento | Registro concreto de un tipo; tiene un identificador único e inmutable. |
| Tipo de relación | Definición de un vínculo dirigido, sus tipos de origen y destino permitidos y su descripción. |
| Propuesta de relación | Solicitud pendiente para crear o modificar un vínculo; no cambia el mapa publicado. |
| Relación validada | Vínculo aprobado, con origen, destino, tipo, justificación y estado. |
| Baja lógica | Cambio de estado que oculta un elemento de las consultas ordinarias sin borrar sus datos ni historial. |
| Bitácora | Registro inmutable de operaciones relevantes, actor, fecha y cambios efectuados. |
| Mapa | Vista visual de un elemento de partida y sus relaciones explícitas autorizadas. |

## 2. Descripción general

### 2.1 Perspectiva del producto

La plataforma será una aplicación web con interfaz, servicio de aplicación y base de datos. Los usuarios capturarán manualmente los datos y sus vínculos. La configuración de capas, tipos, campos y tipos de relación se realizará desde la interfaz, sin modificar el código ni el esquema físico por cada definición nueva. Se utilizarán los componentes tecnológicos acordados por el equipo en su etapa de diseño; esta especificación exige comportamiento y resultados, no un proveedor de alojamiento concreto.

La estructura de la primera versión tiene dos niveles: **capa → tipo de elemento → elementos**. Una relación conecta dos elementos existentes y tiene un tipo dirigido. La pertenencia de dos registros a una misma capa, o la existencia de un recorrido de varios vínculos, no crea automáticamente una relación directa entre ellos.

### 2.2 Funciones del producto

| Grupo | Funciones |
| --- | --- |
| Acceso | Iniciar y cerrar sesión; administrar cuentas, roles y capas editables. |
| Configuración | Crear y mantener capas, tipos de elemento, campos y tipos de relación. |
| Captura | Crear, editar, dar de baja y reactivar elementos; proponer altas y cambios de relaciones. |
| Validación | Aprobar o rechazar propuestas sin alterar una relación vigente antes de la decisión. |
| Consulta | Buscar elementos, consultar detalles, explorar mapas y aplicar filtros. |
| Conservación | Recuperar datos entre sesiones y consultar una bitácora de cambios. |

### 2.3 Características del usuario

| Rol | Facultades en la primera versión |
| --- | --- |
| Administrador | Todas las facultades de consulta y edición; administra cuentas, roles, capas editables, configuración, datos de demostración y propuestas de relación. Puede aprobar o rechazar propuestas. |
| Editor | Consulta todos los elementos activos. Crea, modifica, da de baja y reactiva elementos en las capas asignadas. Propone altas y cambios de relaciones cuando tiene permiso de edición sobre la capa del origen. No aprueba propuestas. |
| Consulta | Busca y consulta elementos, relaciones y mapas. No modifica datos. |

Cada cuenta tiene exactamente un rol. El administrador asigna a los editores las capas editables; un editor sin capas asignadas conserva la consulta y no puede escribir. Los permisos se comprueban en el servidor en cada operación, incluso ante solicitudes directas. La primera versión no restringe la **visibilidad** por elemento ni por capa: una cuenta autenticada puede leer todos los registros activos. Por ello, la demostración y los datos cargados en esta versión no deben contener información reservada. La protección de información confidencial por objeto requiere un diseño posterior de permisos y pruebas de filtrado exhaustivas.

### 2.4 Restricciones, reglas y decisiones de la primera entrega

1. **Cuentas y sesiones.** La autenticación será local, con credenciales individuales. El primer administrador se provisionará mediante un procedimiento técnico de instalación. Después, un administrador podrá crear y desactivar cuentas y restablecer contraseñas desde la plataforma. Las contraseñas no se mostrarán después de su entrega inicial. Nunca podrá quedar el sistema sin un administrador activo. Un cambio de rol, una desactivación o un restablecimiento invalidará todas las sesiones de la cuenta afectada; cerrar sesión invalidará solo la sesión utilizada.
2. **Estructura.** Existirán inicialmente las capas Negocio, Datos, Aplicaciones y Tecnología. El administrador podrá agregar capas y tipos de elemento. Los nombres de capas serán únicos globalmente; los nombres de tipos serán únicos dentro de su capa; los nombres de campos serán únicos dentro de su tipo. Se comparan sin distinguir mayúsculas ni espacios extremos. No se elimina físicamente ninguna definición durante la primera entrega.
3. **Campos.** Todo elemento tendrá un campo base `Nombre`, de texto y obligatorio. Los campos adicionales admitirán texto, número, fecha válida y selección simple de una lista configurada; cada uno podrá ser obligatorio u opcional. Si un tipo ya tiene elementos, no se podrán agregar, retirar ni cambiar campos, tipos de dato, obligatoriedad u opciones en esta versión. Los valores de los elementos sí podrán editarse. Esta regla evita migraciones de datos implícitas.
4. **Identidad y búsqueda.** Cada elemento tendrá un identificador único e inmutable. Se permiten elementos con el mismo nombre, incluso dentro de un tipo; los resultados de búsqueda mostrarán identificador, nombre, tipo y capa. La búsqueda por nombre será parcial, ignorará mayúsculas y espacios extremos y conservará la distinción de acentos. El listado tendrá páginas de 25 elementos ordenados por nombre y luego por identificador.
5. **Relaciones.** Un tipo de relación definirá un tipo de elemento origen y uno destino. Se permiten vínculos entre capas distintas cuando los extremos coinciden con esa definición. No se permite relacionar un elemento consigo mismo ni repetir la combinación de origen, tipo y destino entre relaciones validadas no retiradas o propuestas pendientes. Toda propuesta incluirá una justificación de 10 a 500 caracteres que ayude a la revisión humana; el sistema no decidirá automáticamente si el vínculo es válido para el negocio.
6. **Aprobación.** El editor propone; el administrador aprueba o rechaza. Un administrador también puede registrar una propuesta, pero debe realizar la aprobación como acción separada. Solo las relaciones aprobadas se consideran validadas. Un cambio propuesto sobre una relación existente conserva el identificador y la versión vigente hasta su aprobación. Un editor que proponga cambiar el origen deberá tener permiso de edición tanto en la capa del origen vigente como en la del nuevo origen. No se admite más de una propuesta pendiente sobre la misma relación. Al aprobar se vuelven a comprobar extremos activos, compatibilidad del tipo y ausencia de duplicados; si alguna regla falla, la propuesta permanece pendiente y la relación vigente no cambia. La decisión registra actor y fecha.
7. **Ciclo de vida.** Una relación validada puede estar `vigente` o `retirada`. Retirar un vínculo requiere una propuesta aprobada. Las retiradas siguen consultables en el historial, pero se excluyen del mapa ordinario. Un elemento dado de baja conserva campos, relaciones y bitácora; no puede utilizarse en una nueva propuesta y se oculta por defecto. No habrá borrado físico ni cascadas de eliminación.
8. **Vista visual.** El mapa ordinario muestra al elemento de partida y sus relaciones directas vigentes con otros elementos activos. El usuario puede elegir una capa de destino como cruce, y filtrar por capa, tipo de elemento y tipo de relación. Los filtros se combinan por intersección. El elemento de partida permanece visible para dar contexto, aunque no cumpla un filtro; solo se muestran vínculos cuyos dos extremos están visibles. La vista indicará si se truncó al límite de 100 nodos. El usuario puede seleccionar otro nodo para explorar sus conexiones; el recorrido no crea vínculos nuevos.
9. **Trazabilidad.** Cada elemento y relación conservará creador, fecha de creación, último modificador y fecha de modificación. La bitácora registrará las operaciones de alta, modificación, baja, reactivación, propuestas, decisiones y cambios de acceso con actor, fecha, objeto, acción y valores anteriores y nuevos cuando correspondan. No almacenará contraseñas ni secretos. Ningún usuario podrá editar o borrar entradas de la bitácora.
10. **Datos de demostración.** El conjunto de prueba contendrá objetivos, proyectos, capacidades, procesos y aplicaciones ficticios, al menos un vínculo entre capas y una capa adicional creada desde la interfaz. Su carga no duplicará registros si se ejecuta otra vez.

Estas decisiones ponderan la viabilidad del plazo, la integridad de los datos y la facilidad de verificar cada regla. Se adopta la edición por capa de Liciel para contener el número de combinaciones de acceso de la primera entrega; se adopta la aprobación de Jean Paul porque distingue propuestas de vínculos validados; y se conserva de Gregorio la configuración limitada a cuatro tipos de campo y el bloqueo de estructuras que ya tienen datos. La selección fija la versión recomendada, sin presentarla como un consenso previo de los tres documentos.

## 3. Requerimientos específicos

### 3.1 Requerimientos funcionales

Los criterios siguientes describen escenarios independientes en formato **Dado que / cuando / entonces**. Los datos mencionados son ficticios. Un rechazo conserva el estado anterior y debe comprobarse también mediante una petición directa al servidor; ocultar un botón no basta. Los códigos de respuesta HTTP y los textos exactos de mensajes se definirán en el contrato de API, sin cambiar el resultado funcional de cada criterio.

#### RF-01. Inicio y cierre de sesión

El sistema debe autenticar cuentas activas, proteger las funciones privadas y permitir cerrar una sesión individual.

##### RF-01-AC-1. Acceso válido
**Dado que** existe una cuenta activa con credenciales válidas, **cuando** inicia sesión, **entonces** se crea una sesión vinculada a esa cuenta y se informa su rol.

##### RF-01-AC-2. Acceso inválido o sin sesión
**Dado que** existe un elemento registrado, **cuando** se intenta iniciar sesión con una contraseña incorrecta o solicitar directamente el elemento sin sesión válida, en ejecuciones separadas, **entonces** no se crea una sesión ni se entregan datos protegidos.

##### RF-01-AC-3. Cierre individual
**Dado que** una cuenta tiene dos sesiones válidas A y B, **cuando** cierra A, **entonces** A deja de autorizar solicitudes y B continúa autorizándolas.

#### RF-02. Cuentas, roles y capas editables

El administrador debe administrar cuentas, asignar uno de los tres roles y establecer las capas editables de cada editor.

##### RF-02-AC-1. Alta y asignación
**Dado que** hay un administrador y una capa Aplicaciones, **cuando** crea una cuenta de Editor y le asigna esa capa, **entonces** la cuenta puede iniciar sesión y crear un elemento en Aplicaciones, pero no en Negocio.

##### RF-02-AC-2. Cambio de rol y sesiones
**Dado que** un editor tiene dos sesiones abiertas, **cuando** el administrador cambia su rol a Consulta, **entonces** ambas sesiones anteriores se invalidan; al iniciar una nueva, puede leer pero no modificar datos.

##### RF-02-AC-3. Último administrador
**Dado que** solo existe un administrador activo, **cuando** se intenta desactivarlo o asignarle otro rol, **entonces** se rechaza la operación y permanece un administrador activo.

##### RF-02-AC-4. Restablecimiento y desactivación
**Dado que** una cuenta tiene una sesión abierta, **cuando** un administrador restablece sus credenciales o la desactiva, en ejecuciones separadas, **entonces** su sesión anterior se invalida; las credenciales anteriores no autorizan acceso y la cuenta desactivada no puede iniciar sesión.

#### RF-03. Gestión de capas

El administrador debe consultar, crear y renombrar capas sin cambiar código.

##### RF-03-AC-1. Capas iniciales y nueva capa
**Dado que** la instalación acaba de prepararse, **cuando** el administrador consulta las capas y agrega `Seguridad`, **entonces** encuentra Negocio, Datos, Aplicaciones y Tecnología, y la nueva capa queda disponible sin reiniciar la aplicación.

##### RF-03-AC-2. Nombre repetido
**Dado que** existe la capa `Seguridad`, **cuando** se intenta crear ` seguridad `, **entonces** se rechaza el duplicado y permanece una sola capa con ese nombre normalizado.

##### RF-03-AC-3. Protección por rol
**Dado que** hay una sesión de Editor o Consulta, **cuando** solicita crear o renombrar una capa, **entonces** la operación se rechaza y las capas permanecen sin cambios.

#### RF-04. Tipos de elemento

El administrador debe crear y renombrar tipos de elemento asociados a una capa.

##### RF-04-AC-1. Asociación
**Dado que** existe la capa Negocio, **cuando** el administrador crea el tipo `Proyecto` en ella, **entonces** el tipo aparece asociado a Negocio y puede elegirse al registrar un elemento.

##### RF-04-AC-2. Identidad al renombrar
**Dado que** un tipo tiene elementos, **cuando** el administrador renombra ese tipo, **entonces** conserva su identificador, sus campos y la asociación de los elementos existentes.

##### RF-04-AC-3. Asociación inválida
**Dado que** no existe una capa de destino, **cuando** se intenta crear un tipo en ella, **entonces** se rechaza la operación y no aparece un tipo huérfano.

#### RF-05. Configuración de campos

El administrador debe configurar campos de texto, número, fecha y selección simple por tipo de elemento, con obligatoriedad definida.

##### RF-05-AC-1. Cuatro tipos
**Dado que** existe un tipo sin elementos, **cuando** el administrador guarda campos de texto, número, fecha y selección con opciones A y B, **entonces** se recuperan los cuatro tipos, sus opciones y su obligatoriedad configurada.

##### RF-05-AC-2. Configuración usada
**Dado que** un tipo tiene al menos un elemento, **cuando** se intenta agregar un campo o cambiar el tipo u obligatoriedad de otro, **entonces** se rechaza el cambio y se conservan la definición y los elementos.

##### RF-05-AC-3. Nombres y permisos
**Dado que** un tipo contiene el campo base `Nombre` y un campo `Descripción`, **cuando** el administrador intenta agregar ` nombre ` o `DESCRIPCIÓN`, o un Editor intenta configurar un campo, **entonces** se rechaza cada operación y la definición no cambia.

#### RF-06. Registro y modificación de elementos

El administrador y el editor autorizado por capa deben registrar y actualizar elementos sin cambiar su identificador.

##### RF-06-AC-1. Registro
**Dado que** un Editor puede editar Negocio y existe el tipo Proyecto, **cuando** registra `Proyecto Alfa` con valores válidos, **entonces** el sistema asigna un identificador único y recupera los valores y el tipo guardados.

##### RF-06-AC-2. Modificación
**Dado que** existe un elemento con descripción `Inicial`, **cuando** un editor autorizado guarda `Actualizada`, **entonces** el mismo identificador conserva el nuevo valor y los demás campos no cambian.

##### RF-06-AC-3. Rechazo por permisos
**Dado que** hay un Editor sin permiso sobre Negocio y una cuenta de Consulta, **cuando** cada uno intenta modificar un elemento de esa capa, **entonces** se rechazan ambos intentos y se conservan los valores originales.

#### RF-07. Validación de valores

El sistema debe validar cada escritura de elemento de forma atómica según la definición de sus campos.

##### RF-07-AC-1. Obligatorios
**Dado que** un tipo exige Nombre y Descripción, **cuando** se intenta crear un elemento con cualquiera de esos campos vacío o compuesto solo por espacios, **entonces** se identifica el campo inválido y no se crea el elemento.

##### RF-07-AC-2. Tipos incorrectos
**Dado que** un tipo tiene número, fecha y selección entre A y B, **cuando** se intenta guardar `abc` como número, 30 de febrero como fecha o C como opción, en pruebas separadas, **entonces** se identifica el campo incorrecto y no se guarda ningún cambio de esa operación.

##### RF-07-AC-3. Campo opcional
**Dado que** un campo está configurado como opcional, **cuando** se guarda un elemento sin valor en ese campo y los obligatorios son válidos, **entonces** el elemento se guarda y el campo opcional permanece vacío.

#### RF-08. Listado, búsqueda y detalle de elementos

Todo usuario autenticado debe listar, buscar y consultar elementos activos.

##### RF-08-AC-1. Listado paginado
**Dado que** existen 30 elementos activos, **cuando** se abre el listado sin filtros, **entonces** la primera página contiene 25 y la segunda 5, ordenados por Nombre y luego por identificador.

##### RF-08-AC-2. Búsqueda parcial y duplicados
**Dado que** existen dos elementos llamados `Proyecto Alfa` con IDs distintos y uno llamado `Proyecto Beta`, **cuando** se busca ` alfa `, **entonces** aparecen los dos primeros con identificador, nombre, tipo y capa, y cada selección abre su registro correspondiente.

##### RF-08-AC-3. Sin coincidencias o texto vacío
**Dado que** hay un listado disponible, **cuando** se busca un nombre inexistente o un texto vacío, en pruebas separadas, **entonces** el primer caso informa cero resultados y el segundo pide escribir un nombre sin ejecutar la búsqueda.

#### RF-09. Configuración de tipos de relación

El administrador debe definir el nombre, la descripción y los tipos de elemento origen y destino permitidos para cada tipo de relación.

##### RF-09-AC-1. Definición dirigida
**Dado que** existen los tipos Proyecto y Capacidad, **cuando** el administrador crea `mejora` con origen Proyecto y destino Capacidad, **entonces** esa definición aparece al proponer Proyecto → Capacidad y no se ofrece para Capacidad → Proyecto.

##### RF-09-AC-2. Extremos inválidos
**Dado que** no existe un tipo de elemento destino indicado, **cuando** se intenta guardar un tipo de relación que lo referencia, **entonces** se rechaza la definición y no se guarda una referencia inválida.

##### RF-09-AC-3. Protección por rol
**Dado que** hay una sesión de Editor o Consulta, **cuando** solicita crear o renombrar un tipo de relación, **entonces** se rechaza la operación y el catálogo permanece igual.

#### RF-10. Propuestas de alta de relación

El administrador o un editor con permiso sobre la capa del origen debe poder proponer un vínculo entre elementos existentes, sin publicarlo de inmediato.

##### RF-10-AC-1. Propuesta válida
**Dado que** existen un Proyecto, una Capacidad y el tipo Proyecto → Capacidad `mejora`, **cuando** un editor autorizado propone el vínculo con una justificación válida, **entonces** queda una propuesta pendiente con origen, tipo, destino, justificación y autor, y el mapa ordinario aún no muestra ese vínculo.

##### RF-10-AC-2. Reglas de extremos
**Dado que** existe el tipo Proyecto → Capacidad, **cuando** se propone un destino inexistente, un tipo de destino incompatible o un elemento consigo mismo, en pruebas separadas, **entonces** cada intento se rechaza sin crear propuesta ni vínculo.

##### RF-10-AC-3. Duplicado y justificación
**Dado que** ya existe un vínculo validado no retirado o una propuesta pendiente con la misma combinación de origen, tipo y destino, **cuando** se intenta repetirla, o se envía una justificación fuera de 10 a 500 caracteres, **entonces** se rechaza la nueva propuesta y se conserva el estado previo.

#### RF-11. Decisión sobre propuestas

El administrador debe aprobar o rechazar propuestas de relación y registrar la decisión.

##### RF-11-AC-1. Aprobar alta
**Dado que** existe una propuesta de alta pendiente y sus dos elementos siguen activos, **cuando** el administrador la aprueba, **entonces** se crea una relación validada vigente, se registra decisor y fecha y el mapa ordinario puede mostrarla.

##### RF-11-AC-2. Rechazar alta
**Dado que** existe una propuesta de alta pendiente, **cuando** el administrador la rechaza, **entonces** queda registrada la decisión y no se crea una relación validada.

##### RF-11-AC-3. Aprobación no autorizada
**Dado que** existe una propuesta pendiente, **cuando** un Editor o usuario de Consulta intenta aprobarla mediante una petición directa, **entonces** la decisión se rechaza y la propuesta sigue pendiente.

#### RF-12. Cambios y retiro de relaciones

Los cambios de tipo, extremos, justificación o estado de una relación validada deben pasar por una propuesta y una nueva decisión.

##### RF-12-AC-1. Cambio pendiente
**Dado que** existe una relación vigente R de Proyecto → Capacidad, **cuando** un editor autorizado propone cambiar su justificación o sus extremos a valores válidos, **entonces** la propuesta queda pendiente y R conserva su identificador y valores vigentes en las consultas ordinarias.

##### RF-12-AC-2. Aprobar o rechazar cambio
**Dado que** existe una propuesta de cambio de R, **cuando** el administrador la aprueba, **entonces** R conserva su identificador y adopta los nuevos valores; **cuando** la rechaza en una ejecución independiente, **entonces** R conserva exactamente su versión anterior.

##### RF-12-AC-3. Propuesta simultánea y retiro
**Dado que** R tiene una propuesta de cambio pendiente, **cuando** se intenta registrar otra propuesta para R, **entonces** se rechaza. Si la propuesta pendiente solicita retirar R y se aprueba, R queda `retirada`, se conserva para historial y desaparece del mapa ordinario.

##### RF-12-AC-4. Revalidación antes de aplicar
**Dado que** una propuesta pendiente cambia el origen de R y su nuevo origen fue dado de baja antes de la decisión, **cuando** el administrador intenta aprobarla, **entonces** la aprobación se rechaza, la propuesta sigue pendiente para corrección o rechazo y R conserva sus valores vigentes. Se aplica la misma regla si la propuesta produciría un duplicado o extremos incompatibles.

#### RF-13. Exploración visual

Todo usuario autenticado debe poder explorar relaciones directas vigentes desde un elemento activo.

##### RF-13-AC-1. Vista de conexiones
**Dado que** E1 tiene vínculos validados vigentes con E2 y E3, **cuando** se abre el mapa de E1 sin filtros, **entonces** se muestran E1, E2, E3 y esos dos vínculos con su dirección, sin inventar otros.

##### RF-13-AC-2. Sin conexiones y recorrido
**Dado que** E4 no tiene relaciones vigentes y existe una cadena E1 → E2 → E3, **cuando** se explora E4, **entonces** se muestra E4 sin aristas; **cuando** se explora E1 y después E2, **entonces** se puede ver E2 → E3 sin atribuir una relación directa E1 → E3.

##### RF-13-AC-3. Límite visible
**Dado que** un elemento tiene más de 99 vecinos directos vigentes, **cuando** se abre su mapa, **entonces** se muestran como máximo 100 nodos contando el origen, en orden estable por identificador, y se informa que la vista fue truncada.

#### RF-14. Cruces y filtros del mapa

El usuario debe poder limitar el mapa por capa de destino, tipo de elemento y tipo de relación.

##### RF-14-AC-1. Cruce por capa
**Dado que** E1 se relaciona con elementos de Negocio y Aplicaciones, **cuando** se selecciona Aplicaciones como capa de destino, **entonces** permanecen E1 y los vecinos directos de Aplicaciones con sus vínculos; los demás se ocultan sin borrar datos.

##### RF-14-AC-2. Combinación de filtros
**Dado que** el mapa contiene varios tipos de elemento y relación, **cuando** se aplican simultáneamente filtros de capa, tipo de elemento y tipo de relación, **entonces** se muestran solo vecinos y vínculos que cumplen todos; E1 permanece como contexto aunque no cumpla el filtro.

##### RF-14-AC-3. Quitar filtros
**Dado que** hay filtros activos y no cambiaron los datos ni el elemento de partida, **cuando** se quitan, **entonces** reaparece la vista ordinaria anterior al filtrado con sus vínculos intactos.

#### RF-15. Detalle de elementos y vínculos

El usuario debe poder abrir los campos de un elemento y el detalle de un vínculo desde la consulta o el mapa.

##### RF-15-AC-1. Detalle de elemento
**Dado que** existe un elemento con valores configurados, **cuando** se selecciona su resultado de búsqueda o su nodo, **entonces** se muestran su identificador, capa, tipo, campos y valores guardados.

##### RF-15-AC-2. Detalle de relación
**Dado que** existe un vínculo validado de A hacia B, **cuando** se selecciona su arista o se abre desde el detalle de A, **entonces** se muestran origen, tipo, destino, justificación, estado, autor y fechas, y se puede abrir la información de ambos extremos.

#### RF-16. Baja lógica y reactivación

El administrador o un editor autorizado por capa debe dar de baja y reactivar elementos sin borrar sus datos.

##### RF-16-AC-1. Baja conservadora
**Dado que** E está activo y tiene relaciones, **cuando** un editor autorizado lo da de baja, **entonces** E conserva campos, relaciones e historial, y deja de aparecer en el listado y mapa ordinarios.

##### RF-16-AC-2. Consulta histórica y reactivación
**Dado que** E está de baja, **cuando** un usuario activa `Incluir dados de baja`, **entonces** puede consultarlo con esa etiqueta; **cuando** un editor autorizado lo reactiva, **entonces** E vuelve a los resultados ordinarios.

##### RF-16-AC-3. Extremo dado de baja
**Dado que** E está de baja, **cuando** se intenta usarlo como origen o destino de una nueva propuesta, **entonces** se rechaza la propuesta y no se modifica ninguna relación existente.

#### RF-17. Datos de demostración

El administrador debe poder cargar una muestra identificada como ficticia para comprobar el recorrido principal.

##### RF-17-AC-1. Carga completa
**Dado que** la instalación no contiene la muestra, **cuando** el administrador ejecuta la carga, **entonces** existen registros ficticios de objetivos, proyectos, capacidades, procesos y aplicaciones, una capa adicional y relaciones entre al menos dos capas.

##### RF-17-AC-2. Carga repetida
**Dado que** la muestra ya fue cargada, **cuando** se ejecuta otra vez, **entonces** no se duplican capas, elementos ni relaciones y se informa que la muestra ya existe.

#### RF-18. Trazabilidad y bitácora

El sistema debe conservar responsables y fechas de los registros y una bitácora no editable de las operaciones relevantes.

##### RF-18-AC-1. Autoría
**Dado que** Ana crea un elemento y Luis lo modifica después, **cuando** se consulta el detalle, **entonces** Ana permanece como creadora con su fecha y Luis aparece como último modificador con la fecha del cambio.

##### RF-18-AC-2. Cambio auditable
**Dado que** un elemento tiene `Criticidad = Media`, **cuando** se actualiza a `Alta`, **entonces** la bitácora registra actor, fecha, objeto, acción, valor anterior `Media` y valor nuevo `Alta`.

##### RF-18-AC-3. Protección y secretos
**Dado que** existe una entrada y ocurre un restablecimiento de contraseña, **cuando** cualquier usuario intenta editar la entrada o consulta el evento de restablecimiento, **entonces** no puede alterar la bitácora y esta no revela la contraseña anterior ni la nueva.

#### RF-19. Almacenamiento y recuperación

El sistema debe conservar configuraciones, cuentas, permisos, elementos, propuestas, relaciones y bitácora entre sesiones.

##### RF-19-AC-1. Configuración y registros
**Dado que** se guardaron una capa, un tipo con campos, dos elementos y un vínculo validado, **cuando** se abre una sesión nueva sin estado local anterior, **entonces** se recuperan sus identificadores, valores y asociaciones sin volver a capturarlos.

##### RF-19-AC-2. Decisiones y permisos
**Dado que** se guardaron una asignación de capa y una decisión sobre propuesta, **cuando** se inicia una sesión nueva, **entonces** se recuperan la asignación, el estado de la propuesta, el decisor y la fecha.

### 3.2 Requerimientos no funcionales

| ID | Requerimiento | Verificación |
| --- | --- | --- |
| RNF-01 | Las contraseñas se almacenarán con hash resistente y sal; no aparecerán en texto legible ni en registros de aplicación. | Inspección de la base y de los registros después de crear, autenticar y restablecer una cuenta. |
| RNF-02 | Toda operación protegida verificará en el servidor sesión, rol y, para escrituras del Editor, capa asignada. Un rechazo no alterará datos. | Matriz de pruebas por rol y operación, incluidas peticiones directas. |
| RNF-03 | Toda comunicación con el sistema desplegado utilizará HTTPS. Las sesiones expirarán después de 8 horas o 30 minutos de inactividad. | Inspección de transporte y prueba con reloj controlado. |
| RNF-04 | Abrir un mapa de hasta 100 nodos, explorar otro nodo y aplicar o quitar filtros tardará como máximo 3 segundos por operación, medidos en el navegador con 1,000 elementos, 3,000 relaciones y 10 sesiones simultáneas. | Conjunto fijo ficticio y 10 sesiones; 10 recorridos por sesión; medir desde la acción hasta una vista completa e interactiva y registrar entorno, red y resultados. Ninguna operación medida debe superar el límite. |
| RNF-05 | Una operación confirmada como guardada conservará sus datos después de cerrar y abrir una sesión nueva; una operación rechazada no dejará cambios parciales ni relaciones huérfanas. | Pruebas de persistencia, falla durante escritura e inspección de integridad referencial. |
| RNF-06 | Los recorridos principales funcionarán en las dos últimas versiones estables de Chrome y Edge de escritorio, desde 1280 px de ancho. | Ejecutar registro, propuesta, aprobación y consulta en ambos navegadores de referencia. |
| RNF-07 | La interfaz, los mensajes y la ayuda de los recorridos principales estarán en español. | Revisión de pantallas y escenarios de aceptación. |
| RNF-08 | Los recorridos principales permitirán navegación con teclado y textos con contraste mínimo 4.5:1. | Recorrido manual con teclado y verificador de contraste. |
| RNF-09 | Crear capas, tipos, campos y tipos de relación no requerirá cambiar código ni ejecutar una migración de esquema por cada definición nueva. | Configurar las cuatro definiciones en una instalación desplegada. |
| RNF-10 | La API se documentará en OpenAPI 3.x y vinculará cada operación con los IDs de los criterios que comprueba. | Validación del archivo OpenAPI y revisión de trazabilidad con pruebas. |

### 3.3 Requerimientos de dominio

- **RD-01. Capas base.** El modelo inicial contiene Negocio, Datos, Aplicaciones y Tecnología; una organización puede agregar otras capas desde la plataforma.
- **RD-02. Capacidad y proceso.** Una capacidad expresa lo que la organización puede o necesita hacer; un proceso describe actividades orientadas a un resultado. No son conceptos intercambiables.
- **RD-03. Relaciones explícitas.** Una relación representa una afirmación dirigida entre dos elementos. Solo una relación validada establece ese vínculo en la vista ordinaria; compartir capa o formar parte de un recorrido no implica una relación adicional.
- **RD-04. Juicio humano.** La justificación y la aprobación apoyan la revisión de una relación proyecto–capacidad o proceso–aplicación. La plataforma no infiere automáticamente su contribución, prioridad o validez de negocio.
- **RD-05. Conservación.** Dar de baja un elemento o retirar un vínculo no borra su información ni la bitácora. La primera entrega no realiza eliminación física ni borrados en cascada.
- **RD-06. Datos ficticios.** La demostración académica utilizará datos ficticios claramente identificables como tales; no requiere inventarios reales ni información reservada.
- **RD-07. Límites.** La primera versión excluye integraciones automáticas con sistemas empresariales, reglas programables por usuarios, diagnósticos automáticos e inteligencia artificial.

### 3.4 Procedencia y continuidad de identificadores

Los identificadores de las tres columnas de origen son **locales a cada documento**. Una celda vacía significa que no hay un requerimiento equivalente directo; no niega que exista una mención general. Esta tabla facilita la revisión de la propuesta, pero no convierte automáticamente todos los criterios individuales en compromisos del equipo.

| RF del equipo | Gregorio | Liciel | Jean Paul |
| --- | --- | --- | --- |
| RF-01 Sesión | RF-01, RF-17 | RF-01 | RF-13 |
| RF-02 Cuentas y roles | RF-02 | RF-02, RF-16, RF-19 | RF-14 |
| RF-03 Capas | RF-03 | RF-03 | RF-02 |
| RF-04 Tipos de elemento | RF-04, RF-06 | RF-04 | RF-05 (estructura de captura) |
| RF-05 Campos | RF-05 | RF-05 | RF-03, RF-08 |
| RF-06 Elementos | RF-07, RF-08 | RF-06 | RF-05 |
| RF-07 Validación | RF-07, RF-08 | RF-06 | RF-08 |
| RF-08 Búsqueda | RF-11 | RF-07 | RF-09 (elemento de partida) |
| RF-09 Tipos de relación | RF-16 | RF-08 | RF-06 |
| RF-10 Propuestas | RF-09 (registro directo) | RF-09 (registro directo) | RF-11 |
| RF-11 Decisiones | — | — | RF-12 |
| RF-12 Cambios y retiro | RF-10 | RF-09, RF-17 | RF-07, RF-15 |
| RF-13 Mapa | RF-12 | RF-11 | RF-09 |
| RF-14 Filtros | RF-13 | RF-12 | RF-09 (cruce) |
| RF-15 Detalles | RF-11, RF-14 | RF-07, RF-10 | RF-10 |
| RF-16 Baja lógica | — | RF-18 | — |
| RF-17 Demo | RD-06 | RF-14 | §1.3 |
| RF-18 Trazabilidad | — | RF-15, RF-20 | RF-12 (decisión) |
| RF-19 Persistencia | RF-15 | §2.1, RNF-09 | RNF-03 |

**Continuidad de pruebas.** El contrato de API y las pruebas nuevas usarán únicamente los 56 IDs `RF-XX-AC-Y` definidos aquí. Por ejemplo, `RF-01-AC-1` de este documento significa *Acceso válido* y no hereda el texto homónimo de otro SRS. Cualquier cambio futuro de una regla deberá actualizar el RF, sus criterios y el registro de cambios antes de modificar la API o las pruebas.

### 3.5 Decisiones aplazadas para una versión posterior

Se registran como candidatos, sin convertirlos en requerimientos de la primera entrega: perspectivas y subniveles jerárquicos con campos propios; roles configurables; permisos de lectura o edición por elemento; SSO; siete tipos de campo; cambios de definiciones con datos y su migración; estado `planeada` de relaciones; eliminación física protegida; exportación; y análisis automático. Cada candidato necesitará su propia validación, estimación y criterios antes de entrar en una línea base futura.
