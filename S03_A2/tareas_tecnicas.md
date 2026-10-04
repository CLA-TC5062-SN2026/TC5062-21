# Sprint 1 — Descomposición en tareas técnicas

**Proyecto:** Plataforma de Arquitectura Empresarial  
**Equipo:** 21 — Gregorio Escobedo Straffon, Liciel Reyes Ávila y Jean Paul Lozano Gámiz  
**Actividad:** S03-A2, Parte 2  
**Fecha:** 4 de octubre de 2026  
**Base:** [Sprint 1 aprobado](sprint1_planning.md): US-01, US-06, US-07, US-09 y US-15; 19 story points.

## 1. Alcance y reparto acordado

Se descomponen las cinco historias seleccionadas en **24 tareas, con 39 horas estimadas de trabajo**. Ninguna tarea supera cuatro horas: la mayor es de tres horas. Cada tarea indica persona responsable, rol técnico, dependencia y criterio de terminado. Todas están **pendientes de ejecución**; este documento registra la planificación y su revisión, no la construcción del producto.

Jean Paul indicó repartir las tareas entre Gregorio, Liciel y él, especificando el rol técnico de cada una. Se aplica esa instrucción para mantener la capacidad de tres integrantes del plan aprobado. Las personas pueden trabajar con distintos roles técnicos; el reparto deberá contrastarse con su disponibilidad al iniciar el sprint.

| Integrante | Trabajo planificado | Coordinación | Reserva para aprendizaje e imprevistos | Total disponible en dos semanas |
| --- | ---: | ---: | ---: | ---: |
| Gregorio | 13.5 h | 2 h | 0.5 h | 16 h |
| Liciel | 13.5 h | 2 h | 0.5 h | 16 h |
| Jean Paul | 12 h | 2 h | 2 h | 16 h |
| **Equipo** | **39 h** | **6 h** | **3 h** | **48 h** |

La revisión de la [Definition of Done](definition_of_done.md) añadió TQA-01 (2 h) y TDOC-02 (1 h). Jean Paul aprobó el ajuste de 36 a 39 horas utilizando tres horas de la reserva para imprevistos. El Sprint Goal y los 19 story points no cambian.

Se utilizan componentes existentes del framework elegido para autenticación, formularios y acceso a datos. La preparación debe acordar los contratos de servicios y dejar documentada la tecnología. Si una tarea rebasa su estimación, se divide en unidades de hasta cuatro horas y se revisa capacidad y alcance antes de añadir trabajo. Los story points se conservan a nivel de historia; las horas de las tareas no constituyen una conversión de puntos.

## 2. Preparación común — 4 horas

Estas tareas habilitan las cinco historias. Se registran una sola vez, como notas de preparación en la tarjeta de US-01.

| ID | Tarea concreta | Horas | Responsable y rol | Dependencias | Criterio de terminado |
| --- | --- | ---: | --- | --- | --- |
| T00-01 | Preparar servicio backend, conexión y migraciones del incremento | 2 | Gregorio — backend dev | Entorno de Semana 1 disponible | El servicio inicia con configuración de ejemplo sin secretos; las migraciones se ejecutan en una base vacía y crean cuentas, roles, permisos por capa, capas, tipos, campos y elementos, con identificadores y referencias. Se documentan los contratos usados por el frontend. |
| T00-02 | Preparar frontend y navegación del recorrido | 1 | Liciel — frontend dev | Contratos acordados en T00-01 | La aplicación inicia, conecta con el servicio configurado y permite navegar a acceso, configuración, captura y búsqueda; muestra estados de carga y fallo de conexión. |
| T00-03 | Provisionar cuentas ficticias y capas iniciales | 1 | Jean Paul — backend dev | T00-01, T01-01 | Un procedimiento repetible crea Administrador, Editor y Consulta activos, las capas Negocio, Datos, Aplicaciones y Tecnología y permiso de edición de Negocio para el Editor. Almacena las contraseñas mediante hash y usa valores locales de prueba; no añade secretos al repositorio ni duplica datos al repetirse. |

## 3. US-01 — Inicio de sesión — 4 horas

| ID | Tarea concreta | Horas | Responsable y rol | Dependencias | Criterio de terminado |
| --- | --- | ---: | --- | --- | --- |
| T01-01 | Implementar autenticación y protección de servicios | 2 | Gregorio — backend dev | T00-01 | Una cuenta activa con contraseña válida obtiene sesión y rol; una contraseña inválida no crea sesión. Los servicios protegidos rechazan accesos sin sesión. El componente del framework verifica hashes y aplica los límites de sesión del SRS: ocho horas de duración y treinta minutos de inactividad. |
| T01-02 | Implementar pantalla de acceso y sesión en frontend | 1 | Liciel — frontend dev | T00-02, T01-01 | El formulario permite entrar, conserva la sesión por el mecanismo acordado y presenta el rol reconocido; muestra un error al fallar el acceso sin revelar información protegida. |
| T01-03 | Comprobar acceso correcto, incorrecto y solicitudes sin sesión | 1 | Jean Paul — QA | T00-03, T01-01, T01-02 | Se guarda evidencia de AC-1 con los tres roles y de AC-2 con contraseña incorrecta; se comprueba rechazo de solicitudes directas sin sesión y de cuenta inactiva. Se verifican los límites de sesión mediante pruebas controladas del tiempo. |

## 4. US-06 — Definición de tipos de elemento — 4 horas

| ID | Tarea concreta | Horas | Responsable y rol | Dependencias | Criterio de terminado |
| --- | --- | ---: | --- | --- | --- |
| T06-01 | Implementar creación y renombrado de tipos | 1.5 | Gregorio — backend dev | T01-01, T00-03 | Solo el Administrador crea un tipo en una capa existente y lo renombra. Se rechaza un nombre vacío o una capa inexistente; el renombrado actualiza el nombre manteniendo el identificador y las referencias. |
| T06-02 | Implementar configuración de tipos en frontend | 1.5 | Liciel — frontend dev | T00-02, T06-01 | El Administrador selecciona una capa, crea Proyecto y lo renombra; las validaciones y los errores del servicio se muestran en pantalla. El tipo guardado aparece disponible para la captura. |
| T06-03 | Verificar creación y renombrado con datos existentes | 1 | Jean Paul — QA | T06-01, T06-02, T09-04 | Se demuestra AC-1 en Negocio y AC-2 renombrando un tipo con campos y elementos. Se comparan antes y después su identificador, campos y elementos: todos conservan la asociación. Un Editor no puede modificar tipos mediante una solicitud directa. |

## 5. US-07 — Configuración de campos de un tipo — 7 horas

| ID | Tarea concreta | Horas | Responsable y rol | Dependencias | Criterio de terminado |
| --- | --- | ---: | --- | --- | --- |
| T07-01 | Implementar definición y recuperación de campos | 3 | Gregorio — backend dev | T06-01 | Solo el Administrador configura campos de texto, número, fecha y selección simple, con obligatoriedad y opciones válidas. Un tipo sin elementos recupera exactamente sus definiciones. El nombre base del elemento es texto obligatorio y se rechazan definiciones vacías o incoherentes. |
| T07-02 | Implementar editor de campos y opciones | 2 | Liciel — frontend dev | T00-02, T07-01 | El editor permite configurar los cuatro tipos, obligatoriedad y opciones de selección; al guardar y volver a abrir muestra los valores recuperados del servidor, incluidos campos opcionales. |
| T07-03 | Bloquear cambios de estructura cuando el tipo tiene elementos | 2 | Jean Paul — backend dev | T07-01, T09-01 | El servidor rechaza agregar, eliminar o alterar campos, tipos de dato, obligatoriedad u opciones cuando existe al menos un elemento del tipo. La definición permanece igual; la interfaz informa el bloqueo y las solicitudes directas tampoco lo evitan. Se adjunta evidencia de AC-2. |

## 6. US-09 — Registro de un elemento — 7 horas

| ID | Tarea concreta | Horas | Responsable y rol | Dependencias | Criterio de terminado |
| --- | --- | ---: | --- | --- | --- |
| T09-01 | Implementar registro autorizado y validación en servidor | 2 | Gregorio — backend dev | T01-01, T00-03, T07-01 | Un Editor con permiso sobre la capa guarda valores válidos con identificador único e inmutable. El servidor valida campos obligatorios, los cuatro tipos y opciones permitidas; informa el campo inválido y no deja un registro parcial. Consulta y Editor sin permiso de capa no pueden registrar elementos. |
| T09-02 | Implementar formulario dinámico de captura | 2 | Liciel — frontend dev | T07-02, T09-01 | El formulario se construye a partir del tipo seleccionado, permite texto, número, fecha y selección, distingue campos obligatorios y presenta los errores del servidor junto al campo correspondiente. Una captura válida muestra el identificador generado. |
| T09-03 | Probar validaciones y autorización de captura | 2 | Jean Paul — QA | T09-01, T09-02 | Se comprueba AC-2 con vacío y solo espacios; se prueban número, fecha y selección inválidos, campos opcionales vacíos y acceso directo sin permiso. Cada rechazo identifica el problema y deja sin cambios la cantidad de elementos guardados. |
| T09-04 | Preparar y verificar los tres proyectos del objetivo | 1 | Jean Paul — QA | T09-01, T09-02 | Se registran tres proyectos válidos, incluidos dos llamados Proyecto Alfa con identificadores distintos. Tras abrir una sesión nueva, se recuperan los mismos datos e identificadores desde la base de datos; se guarda evidencia de AC-1. |

## 7. US-15 — Búsqueda de elementos — 5 horas

| ID | Tarea concreta | Horas | Responsable y rol | Dependencias | Criterio de terminado |
| --- | --- | ---: | --- | --- | --- |
| T15-01 | Implementar consulta, búsqueda y paginación | 2 | Gregorio — backend dev | T09-01 | El servicio autenticado devuelve elementos activos con identificador, nombre, tipo y capa. Busca por coincidencia parcial sin distinguir mayúsculas, elimina espacios externos del término y pagina en bloques de 25; aplica orden estable por nombre y después por identificador. Sin filtro devuelve el listado completo paginado. |
| T15-02 | Implementar listado y búsqueda en frontend | 2 | Liciel — frontend dev | T00-02, T15-01 | El usuario puede buscar, limpiar el filtro y cambiar de página. Los resultados muestran identificador, nombre, tipo y capa, junto con carga, error y ausencia de resultados; al cambiar el término vuelve a la primera página. |
| T15-03 | Verificar 30 registros y nombres repetidos | 1 | Jean Paul — QA | T09-04, T15-01, T15-02 | Una muestra separada de 30 elementos activos demuestra 25 y 5 resultados, sin duplicaciones entre páginas y con orden por nombre e identificador (AC-1). Buscar alfa devuelve ambos Proyecto Alfa con sus IDs (AC-2); se comprueban mayúsculas, espacios externos y búsqueda sin coincidencias. |

## 8. Calidad, integración, correcciones y documentación — 8 horas

Se registran una sola vez, como notas de cierre del incremento en US-15. No aumentan los puntos de esa historia.

| ID | Tarea concreta | Horas | Responsable y rol | Dependencias | Criterio de terminado |
| --- | --- | ---: | --- | --- | --- |
| TQA-01 | Comprobar navegadores, teclado, contraste e idioma del recorrido | 2 | Liciel — QA | T01-02, T06-02, T07-02, T07-03, T09-02, T15-02 | Se registra una matriz de acceso, configuración, captura y búsqueda en las dos últimas versiones estables de Chrome y Edge de escritorio desde 1280 px. Se comprueban navegación con teclado, mensajes y ayuda en español y contraste de texto mínimo de 4.5:1 mediante medición. Se anotan versiones, pasos, resultados y defectos para corregir; no se declara D07 cumplido si falta una comprobación o falla una de ellas. |
| TINT-01 | Ejecutar pruebas integradas del objetivo y los diez criterios | 2 | Jean Paul — QA | Todas las tareas de US-01, US-06, US-07, US-09 y US-15; TQA-01 | Se recorre acceso, configuración, captura y búsqueda; se registra resultado y evidencia por cada AC, con permisos en servidor, renombrado con datos y bloqueo de campos. Se verifica persistencia e integridad ante rechazo y una falla de escritura controlada, conforme a D06. Cada defecto queda descrito con pasos de reproducción. |
| TINT-02 | Corregir defectos del recorrido y verificar regresión | 2 | Liciel — fullstack dev | TINT-01 | Los defectos corregibles dentro de este bloque tienen su cambio revisado y su prueba repetida, incluidas las comprobaciones de TQA-01 afectadas. Si no hay defectos, se revisa la integración y se repiten los escenarios críticos. Un defecto que requiera más tiempo se divide y obliga a revisar la reserva o el alcance; no se declara terminado el incremento con un AC o RNF aplicable fallido. |
| TDOC-02 | Completar y validar OpenAPI con referencias a los AC | 1 | Gregorio — backend dev | T01-01, T06-01, T07-01, T07-03, T09-01, T15-01, TINT-02 | El contrato OpenAPI 3.x describe las operaciones construidas, sus entradas, respuestas y autorización; referencia los IDs canónicos RF-XX-AC-Y del SRS aplicables. Se valida sin errores y se compara con el comportamiento del servicio después de las correcciones; se registra versión y resultado. |
| TDOC-01 | Documentar ejecución y preparar demostración | 1 | Jean Paul — documentación técnica / QA | TINT-02, TDOC-02 y todos los AC aprobados | El README del incremento permite instalar y ejecutar aplicación, migraciones y datos ficticios sin secretos. El guion demuestra tres proyectos, nombres repetidos, validación y paginación; enlaza la evidencia de AC y DoD y registra limitaciones conocidas. |

## 9. Cobertura y secuencia

| Historia | Criterio del backlog | Tareas que aportan la comprobación |
| --- | --- | --- |
| US-01 | AC-1: acceso válido y rol | T01-01, T01-02, T01-03 |
| US-01 | AC-2: contraseña incorrecta sin sesión ni datos protegidos | T01-01, T01-03 |
| US-06 | AC-1: Proyecto disponible en Negocio | T06-01, T06-02, T06-03 |
| US-06 | AC-2: renombrado conserva ID, campos y elementos | T06-01, T09-04, T06-03 |
| US-07 | AC-1: recuperar cuatro tipos y obligatoriedad exactos | T07-01, T07-02, TINT-01 |
| US-07 | AC-2: rechazar cambios con elementos existentes | T07-03, TINT-01 |
| US-09 | AC-1: captura válida con ID único | T09-01, T09-02, T09-04 |
| US-09 | AC-2: obligatorio vacío no crea elemento | T09-01, T09-03 |
| US-15 | AC-1: páginas 25/5 y orden por nombre e ID | T15-01, T15-02, T15-03 |
| US-15 | AC-2: ambos Proyecto Alfa distinguibles por ID | T09-04, T15-03 |

La secuencia principal es preparación → acceso y datos iniciales → tipos → campos → captura → búsqueda → pruebas de interfaz → integración y corrección → OpenAPI y demostración. Los formularios y servicios pueden avanzar en paralelo con los contratos acordados. T09-01 depende de la definición de campos T07-01, pero no de su bloqueo T07-03; el bloqueo se termina después de que exista captura. T06-03 también se ejecuta después de T09-04 para verificar renombrado con datos reales de prueba. Así se evita un ciclo entre configuración y captura. Si una corrección modifica la interfaz, TINT-02 repite las comprobaciones de TQA-01 afectadas; TDOC-02 valida el contrato con el servicio corregido.

La revisión de presupuesto mantiene las 4 h de preparación y 27 h de las cinco historias, y asigna 6 h a calidad, integración y corrección y 2 h a documentación y OpenAPI: 39 h en total. Se conservan 6 h de coordinación y 3 h de reserva. La mayor tarea es T07-01 (3 h); ninguna persona supera sus 16 h con coordinación y reserva incluidas.

## 10. Revisión crítica de la descomposición y ajustes

| Hallazgo en la propuesta general | Ajuste documentado | Efecto |
| --- | --- | --- |
| Un bloque como configurar campos o registrar elementos podía exceder cuatro horas y ocultar pruebas. | Se dividieron backend, frontend y comprobaciones; US-07 queda en 3 + 2 + 2 h y US-09 en 2 + 2 + 2 + 1 h. | Cada tarea puede completarse dentro del límite y tiene un resultado verificable. |
| Faltaban tareas visibles para preparar datos, integrar, corregir y demostrar. | Se añadieron T00-01 a T00-03, TINT-01, TINT-02 y TDOC-01 dentro de las 36 h de la propuesta inicial. | La capacidad incluye el trabajo necesario para demostrar el objetivo. |
| Probar el renombrado antes de registrar elementos no cubre US-06 AC-2. | T06-03 depende de T09-04 y compara ID y asociaciones antes y después. | Se verifica el criterio completo con elementos existentes. |
| Bloquear solo la pantalla de campos permitiría modificar la definición por una solicitud directa. | T07-03 aplica el bloqueo en servidor y comprueba que la definición permanece igual. | Se cubre US-07 AC-2 y su autorización. |
| Un formulario válido por sí solo no garantiza una captura válida. | T09-01 y T09-03 incluyen validación atómica, valores inválidos y permisos por capa en servidor. | Se evita guardar registros incompletos o no autorizados. |
| Tres proyectos bastan para el objetivo, pero no prueban la paginación. | T15-03 utiliza una muestra separada de 30 elementos activos y compara páginas y orden. | Se cubre US-15 AC-1, además de la búsqueda con nombres repetidos. |
| La redacción original de la actividad atribuía las tareas a una sola persona. | Se usa el reparto entre los tres integrantes solicitado expresamente por Jean Paul, con carga individual y rol por tarea. | Se conserva el supuesto aprobado de 48 h del equipo. |
| La preparación podría confundirse con historias adicionales terminadas. | Cuentas y capas iniciales se limitan a datos de prueba; la persistencia cubre solo el incremento seleccionado. | No se suman puntos de US-03, US-05, US-20 o US-21 ni se amplía el objetivo. |
| La revisión de la DoD detectó que navegadores, accesibilidad y OpenAPI no estaban como tareas explícitas. | Se añadieron TQA-01 (Liciel — QA, 2 h) y TDOC-02 (Gregorio — backend dev, 1 h), y se explicitaron las pruebas de integridad de D06 y la regresión posterior a correcciones. Jean Paul aprobó el uso de tres horas de reserva. | La propuesta actual contiene 24 tareas y 39 h, con 6 h de coordinación y 3 h de reserva; conserva las 48 h y los 19 puntos. |

Las estimaciones siguen siendo previsiones de un primer sprint sin velocidad histórica. La integración puede descubrir esfuerzo adicional; se utiliza la reserva con visibilidad del equipo y se renegocia alcance si resulta insuficiente. No se reduce un criterio de aceptación para hacer caber una historia.

## 11. Seguimiento en GitHub Projects

Las tareas se agregan como **notas con casillas pendientes en las cinco issues existentes del tablero**, opción permitida por la actividad. Cada nota incluye ID, duración, persona, rol y criterio de terminado; este archivo conserva las dependencias y la revisión completa. Las tareas comunes se anotan solo en US-01 y US-15 para no duplicar estimaciones.

- [Tablero del equipo 21](https://github.com/orgs/CLA-TC5062-SN2026/projects/20).
- [US-01 — Inicio de sesión](https://github.com/CLA-TC5062-SN2026/TC5062-21/issues/1): tres tareas de preparación y tres de la historia (8 h).
- [US-06 — Definición de tipos](https://github.com/CLA-TC5062-SN2026/TC5062-21/issues/6): tres tareas (4 h).
- [US-07 — Configuración de campos](https://github.com/CLA-TC5062-SN2026/TC5062-21/issues/7): tres tareas (7 h).
- [US-09 — Registro de elementos](https://github.com/CLA-TC5062-SN2026/TC5062-21/issues/9): cuatro tareas (7 h).
- [US-15 — Búsqueda](https://github.com/CLA-TC5062-SN2026/TC5062-21/issues/15): tres tareas de la historia y cinco de calidad y cierre (13 h).

Las casillas se marcarán durante la ejecución, al cumplir el criterio de cada tarea. Una historia solo podrá declararse terminada con sus dos criterios de aceptación y la [Definition of Done aprobada](definition_of_done.md) cumplidos. Las notas del tablero reflejan las 24 tareas y las 39 horas de esta versión.

## 12. Referencias

- [Plan del Sprint 1](sprint1_planning.md).
- [Definition of Done aprobada](definition_of_done.md).
- [Backlog de S03_A1, versión consultada](https://github.com/CLA-TC5062-SN2026/TC5062-21/blob/86dbddca2b3e55d62ab775bf2dc57717520b748c/S03_A1/backlog.md).
- [SRS del equipo v1.0](https://github.com/CLA-TC5062-SN2026/TC5062-21/blob/86dbddca2b3e55d62ab775bf2dc57717520b748c/S03_A1/SRS_equipo.md).
- [Actividad S03-A2 en Canvas](https://experiencia21.tec.mx/courses/708363/assignments/23606108?module_item_id=44839015).
