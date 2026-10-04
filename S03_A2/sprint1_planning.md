# Sprint 1 — Planificación

**Proyecto:** Plataforma de Arquitectura Empresarial  
**Equipo:** 21 — Gregorio, Liciel y Jean Paul  
**Actividad:** S03-A2, Parte 1 — Sprint Planning asistido por IA  
**Fecha de elaboración:** 4 de octubre de 2026  
**Duración:** dos semanas  
**Estado:** propuesta aprobada por Jean Paul antes de generar este archivo. Las fechas de ejecución y la disponibilidad efectiva se acordarán con el equipo.

## 1. Base de la planificación

Se utiliza el [Product Backlog de S03_A1](https://github.com/CLA-TC5062-SN2026/TC5062-21/blob/86dbddca2b3e55d62ab775bf2dc57717520b748c/S03_A1/backlog.md), basado en el SRS de equipo v1.0. El backlog contiene cinco épicas, 21 historias y 79 story points. Para este sprint se conservan los identificadores, los puntos y los criterios de aceptación de las historias seleccionadas.

La planificación parte de una aplicación aún sin funcionalidades implementadas. El repositorio consultado contiene los entregables de S03_A1 y el README, sin una aplicación funcional. Se supone que los integrantes tienen preparado su entorno de desarrollo de la Semana 1. La elección concreta de tecnologías y el procedimiento de ejecución deberán quedar documentados durante la preparación del proyecto.

## 2. Sprint Goal

**Al terminar dos semanas, permitir registrar y encontrar al menos tres proyectos ficticios mediante cuentas autorizadas, distinguiendo por identificador los proyectos que tengan el mismo nombre.**

El valor del incremento consiste en disponer de un primer inventario utilizable: los datos se capturan de forma válida y las personas pueden localizar el registro correcto. La configuración de tipos y campos permite adaptar esa captura al modelo de arquitectura, sin exigir todavía el flujo de relaciones ni el mapa visual.

### Comprobación del objetivo

1. Un Administrador autenticado configura el tipo `Proyecto` dentro de la capa inicial `Negocio` y sus campos. El tipo admite texto, número, fecha y selección simple, y distingue campos obligatorios y opcionales.
2. Un Editor autorizado para `Negocio` registra al menos tres proyectos ficticios; dos utilizan el mismo nombre y reciben identificadores distintos.
3. Una captura con un campo obligatorio vacío se rechaza sin guardar un elemento incompleto.
4. Un usuario autenticado busca los proyectos y puede distinguir los resultados por identificador, nombre, tipo y capa.
5. Una muestra separada de 30 elementos activos permite comprobar las páginas de 25 y 5 resultados, ordenadas por nombre y después por identificador.
6. Los diez criterios de aceptación de las cinco historias seleccionadas se verifican. También se comprueban los permisos mediante solicitudes directas al servidor y la conservación de los datos de este incremento en la base de datos.

Estos escenarios son condiciones para la futura demostración; no representan pruebas ejecutadas ni funcionalidades ya construidas.

## 3. Historias seleccionadas

| Historia | Épica | Prioridad del backlog | Story points | Justificación de selección |
| --- | --- | --- | ---: | --- |
| US-01 — Inicio de sesión | E1 | Alta | 3 | Permite acceder con una cuenta activa y reconocer el rol del usuario. |
| US-06 — Definición de tipos de elemento | E2 | Alta | 3 | Permite configurar el tipo `Proyecto` dentro de una capa existente. |
| US-07 — Configuración de campos de un tipo | E2 | Alta | 5 | Define los cuatro tipos de campo y la información obligatoria para una captura válida. |
| US-09 — Registro de un elemento | E3 | Alta | 5 | Permite al Editor autorizado incorporar los proyectos al inventario. |
| US-15 — Búsqueda de elementos | E4 | Alta | 3 | Hace consultable el inventario y evita confundir registros con nombres iguales. |
| **Total** | | | **19** | **Un recorrido completo de captura y consulta.** |

### US-01 — Inicio de sesión

Como usuario con una cuenta activa, quiero iniciar sesión con mis credenciales, para acceder a las funciones que corresponden a mi rol.

- **AC-1:** Dado que tengo una cuenta activa y credenciales correctas, cuando inicio sesión, entonces se crea mi sesión y el sistema reconoce mi rol (`RF-01-AC-1`).
- **AC-2:** Dado que escribo una contraseña incorrecta, cuando intento iniciar sesión, entonces no se crea ninguna sesión ni se me muestra información protegida (`RF-01-AC-2`).

### US-06 — Definición de tipos de elemento

Como administrador, quiero crear un tipo de elemento dentro de una capa, para modelar los registros que cada área necesita capturar.

- **AC-1:** Dado que existe la capa Negocio, cuando creo el tipo `Proyecto` en ella, entonces queda disponible para registrar elementos (`RF-04-AC-1`).
- **AC-2:** Dado que un tipo ya tiene elementos, cuando lo renombro, entonces conserva su identificador, sus campos y sus elementos asociados (`RF-04-AC-2`).

### US-07 — Configuración de campos de un tipo

Como administrador, quiero definir los campos de un tipo de elemento (texto, número, fecha o selección) y marcar cuáles son obligatorios, para asegurar que la captura tenga la información mínima necesaria.

- **AC-1:** Dado que un tipo no tiene elementos, cuando guardo campos de los cuatro tipos con su obligatoriedad, entonces se recuperan exactamente como los configuré (`RF-05-AC-1`).
- **AC-2:** Dado que un tipo ya tiene al menos un elemento, cuando intento agregar o cambiar un campo, entonces la operación se rechaza y la definición no cambia (`RF-05-AC-2`).

### US-09 — Registro de un elemento

Como editor con permiso sobre una capa, quiero registrar un elemento nuevo con los campos de su tipo, para mantener actualizada la información de mi área.

- **AC-1:** Dado que tengo permiso sobre Negocio y existe el tipo Proyecto, cuando registro `Proyecto Alfa` con valores válidos, entonces se guarda con un identificador único (`RF-06-AC-1`).
- **AC-2:** Dado que un campo obligatorio queda vacío, cuando intento guardar, entonces se identifica el campo y no se crea el elemento (`RF-07-AC-1`).

### US-15 — Búsqueda de elementos

Como usuario autenticado, quiero buscar elementos por nombre y ver resultados paginados con su identificador, tipo y capa, para encontrar rápidamente el registro que necesito, incluso si hay nombres repetidos.

- **AC-1:** Dado que existen 30 elementos activos, cuando abro el listado sin filtros, entonces la primera página muestra 25 ordenados por nombre e identificador y la segunda muestra 5 (`RF-08-AC-1`).
- **AC-2:** Dado que existen dos elementos llamados `Proyecto Alfa` con identificadores distintos, cuando busco `alfa`, entonces aparecen ambos distinguidos por su identificador (`RF-08-AC-2`).

## 4. Capacidad estimada

Se utiliza el supuesto aprobado de **tres integrantes, ocho horas semanales por integrante y dos semanas de duración**. Se toma el extremo inferior de las ocho a nueve horas indicadas en la actividad:

**3 integrantes × 8 horas por semana × 2 semanas = 48 horas del equipo.**

| Uso previsto | Horas |
| --- | ---: |
| Preparación de la aplicación, base de datos y cuentas de prueba | 4 |
| Implementación y comprobación de las cinco historias | 27 |
| Integración y pruebas del recorrido completo | 4 |
| Documentación y demostración | 1 |
| Coordinación, aprendizaje e imprevistos | 12 |
| **Total** | **48** |

Las 36 horas de trabajo planificado incluyen backend, frontend, pruebas y documentación. Las 12 horas restantes representan una reserva del 25 %: seis horas para coordinación y seis para aprendizaje e imprevistos. La descomposición de la Parte 2 deberá respetar este presupuesto y comprobar que la carga de cada integrante cabe en sus 16 horas disponibles.

La capacidad propuesta es de **19 story points**. Es una previsión inicial, no una velocidad histórica del equipo: no se cuenta con un sprint anterior completado para calibrarla. Las horas se estiman por el trabajo previsto y los puntos se conservan del backlog; no se define una equivalencia entre un punto y una cantidad de horas. Al terminar el sprint se registrarán los puntos de las historias realmente terminadas y el esfuerzo observado para ajustar la siguiente planificación.

## 5. Dependencias y orden de trabajo

1. Preparar la aplicación, la conexión con la base de datos y las migraciones del incremento.
2. Preparar la autenticación y provisionar cuentas ficticias de Administrador, Editor y Consulta, junto con las capas Negocio, Datos, Aplicaciones y Tecnología. El Editor tendrá `Negocio` como capa editable.
3. Configurar el tipo `Proyecto` mediante US-06 y sus campos mediante US-07.
4. Registrar elementos mediante US-09, con autorización por capa, validación y almacenamiento en el servidor.
5. Consultar y buscar los elementos mediante US-15.
6. Completar la integración, las pruebas y la demostración del recorrido.

El frontend puede prepararse en paralelo con el backend una vez acordados los contratos del incremento. Las comprobaciones de renombrar un tipo con elementos y de bloquear sus campos se realizan después de disponer de elementos registrados; esa dependencia no debe omitirse de las tareas técnicas.

Las cuentas y las capas iniciales se provisionan como preparación técnica reproducible. No se presentan como la implementación de US-03 —administración de cuentas— ni de US-05 —creación de capas adicionales—. Los registros capturados por las historias del sprint se guardan en la base de datos; esa condición tampoco completa por sí sola US-21.

## 6. Historias que permanecen en el Product Backlog

| Historia o grupo | Motivo para no seleccionarlo en este sprint |
| --- | --- |
| US-03 y US-05 | Las cuentas de prueba y las cuatro capas iniciales permiten ejecutar el recorrido. Las pantallas para administrar cuentas y agregar capas se planificarán después. |
| US-08, US-11 y US-12 | El flujo de relaciones necesita tipos de relación, elementos disponibles, propuestas y decisión. Incluirlo ampliaría el alcance antes de comprobar la captura y la consulta. |
| US-16 y US-17 | El mapa y sus filtros necesitan relaciones validadas para entregar su valor completo. |
| US-21 | Sus criterios incluyen recuperar vínculos validados, permisos y decisiones sobre propuestas. Guardar únicamente tipos, campos y elementos sería una implementación parcial; no se contará como historia terminada. |
| US-02, US-04, US-10, US-13, US-14, US-18, US-19 y US-20 | Permanecen dentro del alcance del producto, pero no son necesarios para demostrar el objetivo acotado de este primer sprint. |

La muestra limitada utilizada por QA para probar la paginación no sustituye US-20, que exige una carga administrada más amplia, repetible y con relaciones entre capas.

## 7. Revisión crítica y ajustes a la propuesta

- Se eligió un único recorrido de valor —capturar y encontrar proyectos— en lugar de reunir historias de todas las épicas sin cerrar sus dependencias.
- Se conservan historias completas, incluidos el renombrado de tipos con datos, el bloqueo de cambios de campos y la paginación. No se considera terminada una historia por mostrar solamente una pantalla.
- Se aplazó el mapa porque sus relaciones aún no formarían parte del incremento. También se evitó contar US-21 como terminada por cumplir solo una parte de su persistencia.
- Se incluyeron preparación, integración, pruebas y documentación en la capacidad. El total de 19 puntos no consume las 48 horas como si todas fueran horas de programación.
- Se prevé revisar la estimación al descomponer las tareas. Si aparecen dependencias o esfuerzos que excedan las 36 horas planificadas, el alcance se renegociará antes de asumir un compromiso mayor.

La evaluación del agente es que este alcance puede servir como primera previsión con tres integrantes y el entorno preparado. Su viabilidad deberá contrastarse con las tareas, la disponibilidad real y la Definition of Done que se elaborará en la Parte 3.

## 8. Responsabilidades SCRUM

| Responsabilidad | Aplicación en esta planificación |
| --- | --- |
| Product Owner | Explicar el valor esperado y ordenar el backlog. La selección se enfoca en disponer de un inventario utilizable. |
| Scrum Master | Facilitar la planificación, hacer visibles los impedimentos y comprobar que se respeta el tiempo disponible. |
| Developers | Validar estimaciones y capacidad, descomponer las historias y construir un incremento que cumpla sus criterios y la DoD. Los roles técnicos de backend, frontend y QA forman parte de esta responsabilidad. |
| Agente de IA | Proponer alternativas, detectar dependencias y ayudar a documentar. No sustituye la responsabilidad de las personas del equipo. |

Jean Paul aprobó esta propuesta en la conversación antes de la creación del documento. Esa aprobación no se presenta como una reunión o un acuerdo de los otros integrantes que no haya quedado registrado.

## 9. Referencias

- [Backlog de S03_A1, versión consultada](https://github.com/CLA-TC5062-SN2026/TC5062-21/blob/86dbddca2b3e55d62ab775bf2dc57717520b748c/S03_A1/backlog.md).
- [SRS del equipo v1.0](https://github.com/CLA-TC5062-SN2026/TC5062-21/blob/86dbddca2b3e55d62ab775bf2dc57717520b748c/S03_A1/SRS_equipo.md).
- [Guía Scrum 2020 — Sprint Planning](https://scrumguides.org/scrum-guide.html#sprint-planning).
- [Actividad S03-A2 en Canvas](https://experiencia21.tec.mx/courses/708363/assignments/23606108?module_item_id=44839015).
