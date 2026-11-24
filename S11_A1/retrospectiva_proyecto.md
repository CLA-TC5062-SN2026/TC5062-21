# Retrospectiva del proyecto

**Proyecto:** Plataforma de Arquitectura Empresarial · Equipo 21  
**Fuentes revisadas:** SRS, Product Backlog, contrato OpenAPI, backend, suite de pruebas y auditoría de calidad de Semana 9.

# Sección A — Retrospectiva SCRUM

## ¿Qué salió bien?

- **Se definió un problema de información concreto.** El SRS parte de una necesidad organizacional: los objetivos, proyectos, capacidades, procesos y aplicaciones están distribuidos entre archivos y áreas, lo que dificulta consultarlos de manera conjunta y comprender sus relaciones.
- **Se consolidó una especificación común.** El equipo integró un SRS con 19 requerimientos funcionales y 56 criterios de aceptación identificados de forma estable. Esto facilitó que el backlog y el contrato API tuvieran una referencia compartida.
- **El Product Backlog quedó estructurado en cinco épicas y 21 historias.** Las historias relacionan sus criterios de aceptación con los RF del SRS. Durante el refinamiento se detectó la necesidad de representar la recuperación de datos entre sesiones y se incorporó US-21.
- **Se diseñó un contrato API amplio antes de cerrar la implementación.** El contrato OpenAPI contempla 46 operaciones para sesiones, usuarios, capas, tipos, elementos, propuestas, relaciones, mapas, bitácora y datos de demostración.
- **Se construyó y refactorizó un backend funcional.** El backend utiliza FastAPI, SQLAlchemy y PostgreSQL. La auditoría de Semana 9 registra que las 50 pruebas originales continuaron pasando y que la suite final alcanzó 84 casos aprobados.
- **Se mejoró el rendimiento de consultas en escenarios medidos.** Para una página de 25 elementos entre 300 registros, los SELECT enviados por SQLAlchemy bajaron de 602 a 53; para guardar ocho campos numéricos, de 10 a 2; y para modificar el nombre de un elemento de nueve campos, de 57 a 30. Son conteos de consultas, no mediciones de latencia.
- **Se documentó la calidad y la deuda técnica.** La auditoría conserva pruebas, resultados de Pylint, mediciones y pasos de reproducción, lo que facilita repetir y revisar el trabajo.

## ¿Qué no salió bien?

- **La documentación y el código no siempre estuvieron sincronizados.** En distintas etapas fue necesario distinguir entre operaciones especificadas en el contrato y operaciones que ya estaban implementadas. Esa diferencia pudo generar confusión sobre el avance real.
- **La experiencia completa de producto no está cerrada.** El SRS contempla una aplicación web, pero en el repositorio revisado se encuentra el backend y no se localizó una interfaz frontend. Por eso, aunque las operaciones del servicio estén implementadas y probadas, todavía no se puede demostrar el recorrido visual completo de los perfiles.
- **La cobertura automatizada llegó a consolidarse en una etapa posterior.** La evidencia de Semana 9 muestra una suite de 84 pruebas; habría sido conveniente contar con pruebas de integración y persistencia desde los primeros incrementos.
- **El análisis estático conserva observaciones.** La ejecución final de Pylint registra 492 mensajes (369 de convención, 93 advertencias y 30 de refactorización), sin errores ni mensajes fatales. La puntuación registrada fue 5.13/10. Los hallazgos están documentados, pero no se debe presentar como un análisis limpio.
- **El uso inicial de IA requirió revisión humana.** La reflexión previa del equipo identifica estimaciones demasiado uniformes, historias que mezclaban acciones y criterios omitidos o poco claros. El resultado generado no siempre reflejó las reglas de negocio sin correcciones.

## ¿Qué haríamos diferente la próxima vez?

1. **Validar el problema y el alcance con el stakeholder al inicio.** Acordar qué información necesita consultar, quién la mantiene, qué relaciones son importantes y cómo se medirá el valor de la plataforma.
2. **Mantener la trazabilidad desde el primer sprint.** Cada criterio del SRS debe vincularse con una historia, endpoint, prueba y evidencia, actualizando la matriz al terminar cada incremento.
3. **Desarrollar vertical slices.** Completar un flujo de extremo a extremo —persistencia, API, interfaz y prueba— antes de ampliar el número de funcionalidades.
4. **Incluir frontend y backend en la planificación integrada.** Evitar que el contrato API avance mucho más rápido que la experiencia que utilizará el usuario.
5. **Automatizar desde el primer sprint.** Preparar una base de pruebas reproducible, pruebas de integración y validaciones de contrato desde las primeras historias.
6. **Definir una Definition of Done verificable.** Una historia se cierra cuando cumple criterios, persiste los datos, maneja errores, respeta permisos y cuenta con evidencia reproducible.
7. **Reservar tiempo para integración y demo.** Probar desde una máquina limpia, preparar datos ficticios y validar el flujo completo antes de la presentación.

## Análisis del uso de herramientas y agentes de IA

### ¿En qué fases fueron más útiles?

- **Análisis y estructuración de requisitos:** ayudaron a organizar los requerimientos, detectar duplicidades y convertir necesidades en criterios verificables.
- **Construcción y refinamiento del backlog:** aceleraron la redacción inicial de épicas e historias, así como la vinculación de historias con criterios RF.
- **Diseño técnico:** apoyaron la elaboración y revisión del contrato OpenAPI, diagramas, esquema de datos y documentación.
- **Programación y refactorización:** facilitaron explorar alternativas de implementación, revisar código y proponer mejoras; el equipo pudo contrastarlas con las pruebas.
- **Pruebas y auditoría:** fueron útiles para generar casos, revisar resultados y documentar hallazgos de calidad y rendimiento.

### ¿En qué fases generaron trabajo adicional?

- Cuando las historias generadas tenían estimaciones repetitivas o agrupaban varias acciones, fue necesario dividirlas y volver a estimarlas.
- Cuando una propuesta omitía reglas del SRS —por ejemplo, permisos por capa, unicidad, justificación o aprobación— el equipo tuvo que rastrear la fuente y corregir los criterios.
- Cuando el agente describía una ruta del contrato como si ya estuviera implementada, fue necesario revisar el código y las pruebas para separar especificación de evidencia.
- Los borradores técnicos necesitaron validación de comandos, rutas y versiones reales del repositorio; una guía genérica habría dificultado la reproducción.

### ¿Cambió nuestra forma de programar?

Sí. El trabajo con agentes reforzó un enfoque más orientado a especificaciones: primero aclarar el comportamiento, los criterios de aceptación y el contrato; después implementar y probar. También hizo más importante revisar cada salida con el repositorio y con pruebas automatizadas. La IA aceleró el análisis y la producción de borradores, pero no reemplazó las decisiones del equipo, la revisión de código ni la responsabilidad de comprobar que el sistema funciona.

# Sección B — Consistencia problema–solución

## ¿La aplicación construida resuelve el problema planteado en la Semana 2?

**La solución implementada atiende directamente el problema de dispersión de información de arquitectura empresarial descrito en el SRS.** La necesidad identificada es que los objetivos, proyectos, capacidades, procesos y aplicaciones de una organización pueden estar repartidos entre archivos y áreas, lo que dificulta obtener una visión común y entender cómo se relacionan.

La plataforma responde a esa necesidad al ofrecer un modelo común de información con capas, tipos de elemento, elementos y relaciones explícitas. La API permite administrar y consultar esos registros; el flujo de propuestas y decisiones permite controlar qué relaciones quedan validadas; los mapas permiten consultar conexiones; y la bitácora aporta trazabilidad de operaciones relevantes.

La evidencia técnica disponible respalda que el backend implementa el contrato: la prueba `test_all_46_operations_and_persistence` recorre las 46 operaciones, y la ejecución documentada de pytest registra 84 pruebas aprobadas. Por tanto, existe evidencia de que la capa de servicios puede gestionar y recuperar la información centralizada.

**La solución contribuye al problema, pero la entrega no está completa como producto web.** El SRS contempla una interfaz para Administrador, Editor y Consulta; sin embargo, en el repositorio revisado no se encontró código frontend. En consecuencia, podemos demostrar la gestión centralizada mediante la API y sus pruebas, pero no todavía una experiencia visual integral para que los usuarios de negocio exploren los mapas y administren la arquitectura desde una aplicación web.

### Evidencia concreta

| Necesidad del problema | Funcionalidad que responde | Evidencia disponible |
|---|---|---|
| Consultar información en un lugar común | Capas, tipos y elementos persistidos en PostgreSQL | `S09_A1/codigo/backend/app/models.py`, `services.py` y `S05_S06_A1/esquema_bd.sql` |
| Entender cómo se relacionan los componentes | Tipos de relación, relaciones y mapa por elemento | Operaciones `/api/v1/tipos-relacion`, `/api/v1/relaciones` y `/api/v1/mapas/{elementoId}`; prueba de integración de 46 operaciones |
| Mantener consistencia de la información | Validación de campos, reglas de dominio y propuestas de relación | `test_value_rules.py`, `test_integration.py` |
| Controlar cambios y responsabilidades | Roles, sesiones, autoría y bitácora | Operaciones de usuarios/sesiones y `/api/v1/entradas-bitacora`; pruebas de integración |
| Recuperar información y dar continuidad | Persistencia y recuperación entre sesiones | `test_all_46_operations_and_persistence` |
| Verificar que la solución funciona | Suite automatizada | `S09_A1/evidencias/despues/pytest.txt`: 84 passed, 1 warning |

No se incluyen capturas inventadas. La evidencia visual deberá obtenerse ejecutando el backend y, cuando exista, la interfaz de usuario.

## ¿Qué partes del problema original no se lograron resolver? ¿Quedaron fuera del alcance o fueron obstáculos técnicos?

Las principales limitaciones pendientes son:

- **Accesibilidad para usuarios no técnicos:** sin frontend, los usuarios deben interactuar con la API o Swagger, lo cual no sustituye una aplicación visual de negocio.
- **Exploración visual de arquitectura:** el backend expone datos de mapas y filtros, pero falta la representación gráfica interactiva en una interfaz.
- **Validación con usuarios reales:** la evidencia del repositorio demuestra pruebas técnicas; no equivale a una validación de usabilidad o a confirmar que las vistas responden a las necesidades de las áreas.
- **Integración con fuentes corporativas:** la primera entrega contempla captura manual. La sincronización automática con sistemas empresariales e importación masiva están fuera del alcance definido en el SRS.
- **Gobierno y evolución de la arquitectura:** funciones avanzadas como perspectivas y subniveles jerárquicos, permisos por elemento, roles configurables, inicio federado y diagnósticos automáticos se dejaron fuera de la primera versión.

La ausencia del frontend es una brecha técnica/de integración de la entrega revisada. La importación masiva, sincronización automática y otras funciones avanzadas son exclusiones explícitas del alcance inicial, no funcionalidades que deban presentarse como defectos del backend.

## Si tuviéramos que presentarle el proyecto al stakeholder, ¿qué demostraríamos primero y por qué?

Primero demostraríamos un caso de uso que refleje la necesidad central: **consultar un conjunto de arquitectura en un solo lugar y comprender las relaciones entre sus componentes**. Utilizaríamos datos ficticios de una organización, por ejemplo, un objetivo conectado con un proyecto, una capacidad, un proceso y una aplicación.

La demostración seguiría este orden:

1. Mostrar las capas y los tipos de elemento que estructuran la información.
2. Registrar o consultar un elemento y recuperar sus datos por identificador.
3. Consultar una relación y explicar su origen, destino, tipo y justificación.
4. Crear una propuesta de relación y mostrar el flujo de aprobación o rechazo.
5. Consultar el mapa de conexiones y aplicar filtros desde la operación disponible de API.
6. Consultar la bitácora para mostrar quién realizó un cambio y cuándo.
7. Cerrar con la evidencia de pruebas automatizadas y explicar qué parte del producto sigue pendiente de interfaz.

Empezaríamos por la consulta integrada y las relaciones porque es el núcleo del problema: pasar de información fragmentada a una visión común y trazable. Seríamos transparentes al explicar que el backend está implementado y probado, mientras que la interfaz web visual no está incluida en el repositorio revisado.

## Cierre

El proyecto avanzó desde la definición de una necesidad de información común hasta una API de arquitectura empresarial con 46 operaciones y una suite de 84 pruebas aprobadas. La solución backend está alineada con el problema de centralizar y relacionar información de arquitectura. El siguiente paso para completar la experiencia del stakeholder es integrar una interfaz web y validar sus flujos con usuarios de las áreas que consultarán y mantendrán la arquitectura.
