# Definition of Done — Plataforma de Arquitectura Empresarial

**Equipo:** 21 — Gregorio Escobedo Straffon, Liciel Reyes Ávila y Jean Paul Lozano Gámiz  
**Actividad:** S03-A2, Parte 3  
**Versión:** 1.0  
**Fecha:** 4 de octubre de 2026  
**Estado:** propuesta y ajuste de capacidad aprobados por Jean Paul antes de crear este archivo. La aprobación no acredita una revisión de los otros integrantes ni pruebas del producto ya ejecutadas.

## 1. Regla de terminado

**Una historia estará terminada cuando cumpla todos sus criterios de aceptación y las comprobaciones de calidad aplicables, con evidencia registrada.**

La DoD establece una base común de calidad para las historias del proyecto. Los criterios de aceptación describen el comportamiento específico de cada historia; ambos deben cumplirse. El criterio de done de una tarea técnica permite cerrar esa tarea, pero no basta por sí solo para declarar terminada la historia o el incremento.

Si falta una comprobación, falla un criterio o no hay evidencia suficiente, la historia permanece pendiente o en revisión. Al terminar el sprint, el trabajo que no cumple la DoD vuelve al Product Backlog para su consideración futura; no se presenta como terminado ni se cuentan sus story points como completados. La aprobación del Product Owner no sustituye el cumplimiento de la DoD.

Esta regla sigue el compromiso de calidad del incremento descrito en la [Guía Scrum 2020](https://scrumguides.org/scrum-guide.html#commitment-definition-of-done).

## 2. Lista de comprobación común

| ID | Condición para declarar una historia terminada | Evidencia requerida |
| --- | --- | --- |
| D01 | Todos sus criterios de aceptación se cumplen, incluidos los casos de rechazo. | Resultado por cada AC, vinculado a su identificador y a la versión comprobada. |
| D02 | El código está integrado en main; la aplicación compila o inicia y funciona junto con el incremento existente. | Referencia al commit integrado y comprobación de ejecución desde la configuración documentada. Las verificaciones locales configuradas no presentan errores. |
| D03 | Otro integrante revisó el cambio y se resolvieron sus observaciones que afectan el funcionamiento o la calidad exigida. | Revisión registrada en una issue o pull request, con nombre del revisor, fecha y resolución de observaciones. |
| D04 | Pasan las pruebas de aceptación, negativas y de regresión pertinentes. No quedan defectos que incumplan un AC o requisito de calidad aplicable. | Pasos o comandos, resultados, fecha y entorno. Se admiten pruebas manuales reproducibles y automatizadas locales. Los defectos corregidos tienen una comprobación posterior; las limitaciones restantes se registran en issues y no pueden contradecir un AC o RNF aplicable. |
| D05 | El servidor comprueba sesión, rol y permisos por capa. Las contraseñas usan hash resistente con sal y no se publican secretos. Se verifican los límites de sesión de 8 horas y 30 minutos de inactividad; un entorno desplegado utiliza HTTPS. | Pruebas de acceso directo por rol y capa, inspección de configuración y almacenamiento, y pruebas de expiración con tiempo controlado. La evidencia no expone contraseñas, tokens ni otros secretos. |
| D06 | Los datos guardados se recuperan en una sesión nueva; los rechazos y fallos de escritura no dejan cambios parciales. Configurar tipos y campos no exige cambiar código ni el esquema físico por cada definición. | Pruebas de persistencia e integridad, incluida una falla de escritura controlada. Se comparan datos e identificadores antes y después; la configuración se realiza mediante el flujo construido, sin una migración por definición. |
| D07 | Las pantallas del recorrido están en español, permiten navegación con teclado y tienen contraste de texto mínimo de 4.5:1. Funcionan desde 1280 px en las dos últimas versiones estables de Chrome y Edge. | Lista de comprobación por recorrido y navegador, versiones probadas, ancho de referencia, resultado de navegación con teclado y medición de contraste. |
| D08 | La documentación permite instalar, configurar y ejecutar lo construido. La API está documentada en OpenAPI 3.x y relaciona las operaciones con los criterios correspondientes. | README actualizado, configuración de ejemplo sin secretos, instrucciones de migraciones y datos ficticios, y contrato de API validado con los IDs canónicos del SRS. |
| D09 | La issue enlaza código, revisión y pruebas; las tareas necesarias están terminadas y la comprobación de DoD queda registrada. | Lista de cierre D01–D09 en GitHub Projects o en su issue vinculada, con resultado, evidencia y persona que lo comprobó. Solo después se marca la historia como Done. |

Un punto puede marcarse **No aplica** únicamente con una justificación específica revisada por otro integrante. Por ejemplo, una historia sin escrituras no requiere una prueba propia de persistencia, pero sí debe conservar las comprobaciones comunes del incremento. No aplica no significa pendiente ni sirve para dispensar una prueba fallida. **Los criterios de aceptación de la historia siempre deben cumplirse.**

Los resultados se registrarán como Cumple, No cumple, Pendiente o No aplica justificado. Este documento define comprobaciones futuras: no declara cumplido ninguno de estos puntos.

## 3. Aplicación al Sprint 1

La DoD se aplica a US-01, US-06, US-07, US-09 y US-15, las cinco historias y 19 puntos del [plan aprobado](sprint1_planning.md).

| Historia | Comprobaciones específicas que deben quedar demostradas | Tareas principales que aportan evidencia |
| --- | --- | --- |
| US-01 — Inicio de sesión | Cuenta activa con credenciales correctas obtiene sesión y rol. Una contraseña incorrecta no crea sesión; una solicitud directa sin sesión no entrega datos protegidos. Se prueban los límites de sesión. | T01-01 a T01-03 y TINT-01. |
| US-06 — Tipos de elemento | Proyecto queda disponible en Negocio. Renombrar un tipo con datos conserva su identificador, sus campos y los elementos asociados. | T06-01 a T06-03; T09-04 proporciona los elementos de prueba. |
| US-07 — Campos de un tipo | Se recuperan exactamente texto, número, fecha y selección, sus opciones y obligatoriedad. Cuando existen elementos, agregar o cambiar la estructura se rechaza en servidor y conserva la definición. | T07-01 a T07-03 y TINT-01. |
| US-09 — Registro de elementos | Una captura válida recibe ID único. Un obligatorio vacío o con solo espacios identifica el error y no crea un registro parcial. Se prueban valores inválidos, campos opcionales y autorización por capa. | T09-01 a T09-04 y TINT-01. |
| US-15 — Búsqueda | Dos Proyecto Alfa aparecen distinguidos por ID. Una muestra separada de 30 elementos activos produce páginas de 25 y 5, ordenadas por nombre e identificador y sin duplicaciones entre páginas. | T15-01 a T15-03 y TINT-01. |

La demostración del objetivo utiliza tres proyectos ficticios, incluidos los dos con el mismo nombre, y el recorrido de acceso, configuración, captura y consulta. La muestra de 30 elementos comprueba la paginación. Una demostración satisfactoria se acompaña de los diez AC comprobados y de D01–D09; no reemplaza las pruebas negativas ni la revisión.

Las pruebas comunes de interfaz se registran en TQA-01. OpenAPI se completa y valida en TDOC-02. La revisión y las pruebas de integridad se incorporan al trabajo de cada historia y a TINT-01/TINT-02; TDOC-01 reúne instrucciones y evidencia para la demostración.

## 4. Relación con los requisitos de calidad del SRS

| Requisito | Aplicación en la DoD y en el primer incremento |
| --- | --- |
| RNF-01 — Contraseñas | D05: hash resistente con sal e inspección de almacenamiento y registros, sin secretos legibles. |
| RNF-02 — Autorización | D05: sesión, rol y capa se comprueban en servidor; los rechazos conservan los datos. |
| RNF-03 — Transporte y sesión | D05: límites de sesión comprobados localmente; HTTPS obligatorio cuando la aplicación se despliegue. La ejecución local se identifica como entorno de desarrollo. |
| RNF-04 — Rendimiento del mapa | Su prueba de hasta 3 segundos, con 1,000 elementos, 3,000 relaciones y 10 sesiones simultáneas, se incorporará cuando se implemente el mapa. El mapa no forma parte del Sprint 1 y no se declara este requisito cumplido. |
| RNF-05 — Persistencia e integridad | D06: datos confirmados sobreviven a una sesión nueva y una operación rechazada o fallida no deja cambios parciales. |
| RNF-06 — Navegadores | D07 y TQA-01: recorridos construidos en las dos últimas versiones estables de Chrome y Edge de escritorio, desde 1280 px. Propuestas, aprobación y mapa se comprobarán al construirse. |
| RNF-07 — Idioma | D07 y TQA-01: interfaz, mensajes y ayuda del recorrido en español. |
| RNF-08 — Accesibilidad | D07 y TQA-01: recorrido manual con teclado y contraste de texto de al menos 4.5:1. |
| RNF-09 — Configuración | D06: tipos y campos se configuran sin modificar código o ejecutar una migración por definición. Las capas adicionales y tipos de relación se comprobarán en sus historias futuras. |
| RNF-10 — Contrato de API | D08 y TDOC-02: OpenAPI 3.x validado con trazabilidad a los IDs RF-XX-AC-Y del SRS del equipo. |

La aplicación de estos requisitos al incremento no completa historias fuera del sprint. Las cuentas y capas iniciales son preparación técnica; la muestra acotada de paginación tampoco completa la carga integral de US-20. La persistencia de tipos, campos y elementos no permite marcar US-21 terminada mientras falten sus vínculos, decisiones y permisos previstos.

## 5. Adaptación y justificación

| Decisión adoptada | Justificación para el contexto académico |
| --- | --- |
| Ejecutar y registrar comprobaciones locales | El equipo aún no tiene CI/CD completo. La evidencia reproducible permite verificar calidad sin depender de una infraestructura automática. |
| Admitir pruebas manuales y automatizadas locales | Los AC y casos negativos deben comprobarse desde este incremento. Se puede ampliar la automatización posteriormente sin sustituir las pruebas necesarias por una meta arbitraria de cobertura. |
| Revisar el código entre integrantes | La actividad tiene alcance colaborativo y Jean Paul solicitó el reparto entre Gregorio, Liciel y él. Una revisión registrada por otra persona es viable; el agente ayuda, pero no sustituye al revisor humano. |
| Ejecutar el incremento desde el entorno documentado | La DoD exige un incremento utilizable y reproducible. No exige contratar alojamiento ni efectuar un despliegue público para declarar terminadas las historias del entorno académico. Todo despliegue sí debe respetar HTTPS. |
| Aplicar los RNF a las funcionalidades construidas | Se comprueban acceso, configuración, captura y búsqueda en este sprint. El rendimiento del mapa se conserva como obligación de su implementación futura, sin ampliar el Sprint Goal. |
| Reservar tiempo explícito para interfaz y OpenAPI | La revisión detectó dos comprobaciones que no eran tareas visibles en la Parte 2. El ajuste aprobado evita declarar calidad sin planificar su trabajo. |

La DoD se revisará en la retrospectiva y cuando cambie el contexto técnico. Si su cumplimiento requiere más tiempo del estimado, se revisarán las tareas y el alcance con el Product Owner; no se rebajarán los criterios para declarar terminado un trabajo incompleto.

## 6. Ajuste aprobado de tareas y capacidad

Se añaden dos tareas comunes al incremento, anotadas una sola vez en la issue de US-15:

| ID | Tarea | Responsable y rol | Horas |
| --- | --- | --- | ---: |
| TQA-01 | Comprobar navegadores, teclado, contraste e idioma del recorrido | Liciel — QA | 2 |
| TDOC-02 | Completar y validar OpenAPI con referencias a los AC | Gregorio — backend dev | 1 |

Las dependencias y los criterios de terminado están en [tareas_tecnicas.md](tareas_tecnicas.md). El sprint queda en **24 tareas y 39 horas de trabajo**, con **6 horas de coordinación y 3 de reserva** dentro de las **48 disponibles**. Las cinco historias siguen sumando **19 story points**.

| Integrante | Trabajo planificado | Coordinación | Reserva | Total |
| --- | ---: | ---: | ---: | ---: |
| Gregorio | 13.5 h | 2 h | 0.5 h | 16 h |
| Liciel | 13.5 h | 2 h | 0.5 h | 16 h |
| Jean Paul | 12 h | 2 h | 2 h | 16 h |
| **Equipo** | **39 h** | **6 h** | **3 h** | **48 h** |

## 7. Responsabilidades SCRUM y registro de cierre

- **Developers:** construir, revisar y comprobar el incremento; cumplir la DoD y registrar evidencia. Backend, frontend, QA y documentación son roles técnicos dentro de esta responsabilidad.
- **Product Owner:** ordenar el backlog, aclarar los criterios y revisar el valor del incremento. Participa en la renegociación del alcance; su aprobación no dispensa una comprobación fallida.
- **Scrum Master:** facilitar el proceso, hacer visibles los impedimentos y ayudar a respetar los tiempos y la DoD.
- **Agente de IA:** apoyar propuestas, revisión y documentación, sin declarar pruebas ejecutadas ni reemplazar la responsabilidad del equipo.

Antes de cerrar una historia, su issue debe registrar: commit comprobado; fecha y entorno; resultados de sus dos AC; resultado de D01–D09; enlaces a pruebas y revisión; persona que verificó; y justificación revisada de cualquier No aplica. El [tablero del equipo](https://github.com/orgs/CLA-TC5062-SN2026/projects/20) se actualiza después de la comprobación. La Sprint Review permite inspeccionar el valor conseguido y orientar el trabajo futuro; no constituye un permiso adicional para que un trabajo que ya cumple la DoD sea un incremento.

## 8. Referencias

- [Sprint 1 — Planificación](sprint1_planning.md).
- [Sprint 1 — Tareas técnicas](tareas_tecnicas.md).
- [SRS del equipo v1.0, versión consultada](https://github.com/CLA-TC5062-SN2026/TC5062-21/blob/86dbddca2b3e55d62ab775bf2dc57717520b748c/S03_A1/SRS_equipo.md).
- [Backlog de S03_A1, versión consultada](https://github.com/CLA-TC5062-SN2026/TC5062-21/blob/86dbddca2b3e55d62ab775bf2dc57717520b748c/S03_A1/backlog.md).
- [Guía Scrum 2020 — Definition of Done](https://scrumguides.org/scrum-guide.html#commitment-definition-of-done).
- [Actividad S03-A2 en Canvas](https://experiencia21.tec.mx/courses/708363/assignments/23606108?module_item_id=44839015).
