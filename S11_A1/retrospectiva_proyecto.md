# Retrospectiva del proyecto

**Proyecto técnico:** Plataforma de Arquitectura Empresarial · Equipo 21  
**Enfoque:** retrospectiva Scrum, uso de agentes de IA y consistencia entre problema y solución.

> Esta retrospectiva se elaboró con la documentación técnica disponible y la reflexión previa del equipo sobre SRS, backlog y priorización. Se distingue entre hechos observables y valoraciones del proceso; no se atribuyen resultados que no estén documentados.

# Sección A — Retrospectiva SCRUM

## ¿Qué salió bien?

- **Se consolidó una línea base técnica común.** El equipo contó con un contrato OpenAPI en español (v1.2.0), diagramas de arquitectura y clases, esquema SQL y colección Postman. Esto permitió que el diseño del dominio y la API tuvieran referencias compartidas.
- **Se relacionaron historias con criterios del SRS.** La reflexión previa registra cinco épicas y el uso de identificadores `RF-XX-AC-Y` para mantener la trazabilidad.
- **Se detectaron omisiones durante el refinamiento.** La reflexión del equipo señala que se identificó la falta de una historia para recuperar información entre sesiones y se añadió US-21 para representar RF-19.
- **Se discutieron prioridades en lugar de aceptar automáticamente una propuesta.** Se comparó el orden original del backlog con una propuesta desde el punto de vista del Product Owner, lo que ayudó a hacer visibles los trade-offs entre el recorrido mínimo demostrable y el valor de capturar, mantener y consultar información.
- **Se produjo una primera implementación ejecutable de API.** `main.py` incluye health check, operaciones básicas de capas, tipos, cuentas y consultas de elementos, relaciones y bitácora.

## ¿Qué no salió bien?

- **La implementación quedó por debajo del alcance del contrato.** El OpenAPI describe un conjunto funcional más amplio que las rutas presentes en `main.py`. Por ejemplo, no se observan las rutas de sesiones, propuestas, decisiones, mapas, detalle de bitácora, alta/edición de elementos ni baja/reactivación.
- **La validación técnica no cerró el ciclo completo.** La colección Postman disponible contiene cuatro solicitudes, enfocadas en health y capas. El propio README técnico del paquete advierte que no se ejecutó integración real contra PostgreSQL durante la generación.
- **No hay suite automatizada identificable.** En el paquete no aparece `backend/tests/`; por ello no podemos afirmar que exista cobertura automatizada de los requerimientos.
- **La solución entregada no contiene la interfaz prevista.** La arquitectura contempla React + TypeScript y Nginx, pero esos componentes no están incluidos en el paquete revisado.
- **La generación inicial con IA necesitó correcciones sustanciales.** La reflexión previa registra estimaciones repetitivas, historias que mezclaban acciones, omisiones en criterios y una historia sin asignación clara de capas. Una redacción convincente no garantizó precisión funcional.
- **Persistió una brecha entre documentación y ejecución.** El contrato debe leerse como especificación objetivo, no como inventario de funcionalidades terminadas. No mantener esta distinción puede generar expectativas incorrectas durante la demo.

## ¿Qué haríamos diferente la próxima vez?

1. **Cerrar el alcance antes de implementar.** Acordar un MVP con criterios de aceptación verificables y separar explícitamente lo comprometido para el sprint de lo que queda como evolución.
2. **Mantener una matriz viva desde el primer sprint.** Cada RF debe tener historia, endpoint, responsable, prueba y estado; actualizarla en cada revisión, no al final.
3. **Implementar vertical slices.** Completar una funcionalidad de extremo a extremo (persistencia, API, interfaz y prueba) antes de ampliar el contrato con más operaciones.
4. **Definir una Definition of Done más estricta.** Una historia no se cierra solo porque existe una ruta: debe compilar, validar reglas, persistir, manejar errores y contar con prueba reproducible.
5. **Automatizar temprano.** Configurar pruebas de API y de integración desde el primer incremento, con base de datos de prueba y ejecución repetible.
6. **Revisar los artefactos generados por IA contra las fuentes.** Validar cada historia con el SRS, estimar en equipo, detectar duplicados y comprobar que el actor/beneficio estén bien definidos.
7. **Proteger tiempo para integración y demo.** Reservar tiempo para desplegar, probar desde una máquina limpia y capturar evidencia real; no asumir que una arquitectura dibujada ya está operativa.

## Análisis del uso de herramientas/agentes de IA

### ¿En qué fases fueron más útiles?

- **Análisis y estructuración del SRS:** ayudaron a organizar los requisitos y criterios en grupos manejables.
- **Construcción del Product Backlog:** permitieron proponer épicas, historias con formato consistente y relaciones entre historias y criterios `RF-XX-AC-Y`.
- **Refinamiento y priorización:** facilitaron comparar opciones, identificar huecos (como US-21) y discutir el orden de trabajo.
- **Documentación técnica:** son útiles para generar primeros borradores de diagramas, explicaciones, matrices y guías a partir de archivos fuente.

### ¿En qué fases generaron trabajo adicional?

- Cuando el agente asignó estimaciones demasiado uniformes o mezcló varias acciones en una historia, el equipo tuvo que dividir, reestimar y reescribir.
- Cuando omitió reglas o referencias explícitas al SRS, fue necesario rastrear cada criterio y corregir la historia.
- Cuando produjo documentación con tono definitivo sin evidencia de ejecución, hizo falta verificar qué estaba realmente implementado y qué solo estaba descrito en el contrato.

### ¿Cambió nuestra forma de programar?

Sí. El uso de agentes impulsó una forma de trabajo más orientada a especificaciones: primero describir el comportamiento, criterios y contrato; después derivar estructura y código. También hizo más importante revisar las salidas, porque el código o documentación generados pueden parecer correctos aunque omitan reglas del dominio. La conclusión es que la IA acelera la exploración y la producción de borradores, pero no reemplaza la revisión técnica, las pruebas ni la responsabilidad de priorización del equipo.

# Sección B — Consistencia problema–solución

## ¿La aplicación construida resuelve el problema planteado en la Semana 2?

**No de manera directa, con la evidencia disponible.** En la Semana 2 se identificó como problema la desigualdad de acceso a educación STEM en Coacalco, México, particularmente en robótica, programación, inteligencia artificial e ingeniería. Se señalaron como causas la falta de recursos educativos, equipo, instructores especializados, infraestructura y colaboración entre escuelas, universidades e industria.

La aplicación descrita por los artefactos técnicos actuales es una **Plataforma de Arquitectura Empresarial**. Su dominio incluye capas, tipos de elementos, elementos, relaciones, propuestas, decisiones y bitácora. La implementación observada permite gestionar parcialmente esos datos mediante una API. No se encontró evidencia de módulos para impartir cursos STEM, registrar estudiantes, administrar talleres, conectar mentores con escuelas, prestar equipo o medir el acceso y progreso educativo.

Por tanto, no sería correcto afirmar que la plataforma actual resuelve el problema de acceso a STEM. La solución técnica puede demostrar capacidades de modelado y gestión de información, pero falta una relación funcional explícita entre esas capacidades y las necesidades de estudiantes, familias, escuelas y organizaciones STEM de Coacalco.

### Evidencia concreta disponible

- `arquitectura_equipo.md` describe una plataforma con frontend web previsto, API REST y PostgreSQL, organizada alrededor de capas, tipos, elementos, propuestas, relaciones, mapas y bitácora.
- `openapi_equipo.yaml` especifica operaciones para cuentas, capas, elementos, relaciones, propuestas y auditoría.
- `main.py` implementa una parte de las operaciones de capas, tipos, cuentas y consultas.
- `postman_collection.json` ofrece un recorrido manual mínimo de health y CRUD básico de capas.

Estas evidencias demuestran el tipo de sistema construido, pero no demuestran resultados educativos ni atención al problema de Semana 2. Tampoco se recibieron capturas reales, por lo que no se citan imágenes como evidencia visual.

## ¿Qué partes del problema original no se lograron resolver? ¿Quedaron fuera del alcance o fueron obstáculos técnicos?

La solución revisada no aborda directamente:

- La disponibilidad y distribución de kits, laboratorios, computadoras o conectividad.
- La formación y disponibilidad de docentes o mentores especializados.
- El diseño e impartición de experiencias de robótica, programación, IA e ingeniería para estudiantes de 8 a 18 años.
- La vinculación efectiva entre escuelas, universidades, empresas, profesionales STEM y familias.
- La medición de participación, permanencia, aprendizaje y progreso de estudiantes.
- Las barreras de costo, transporte, horarios y acceso para comunidades con menos recursos.

La principal brecha no parece ser solamente un obstáculo técnico puntual: es una **desalineación de alcance y de dominio de producto** entre el problema original y el sistema documentado. La implementación parcial (sin frontend, seguridad ni pruebas completas) constituye además una limitación técnica del entregable, pero incluso una versión completa de la plataforma de arquitectura empresarial no resolvería automáticamente la desigualdad de acceso a STEM.

## Si tuviéramos que presentar el proyecto al stakeholder de la Semana 2, ¿qué demostraríamos primero y por qué?

Primero presentaríamos el problema original y validaríamos con el stakeholder si la necesidad sigue siendo mejorar el acceso a oportunidades STEM en Coacalco. Después mostraríamos un prototipo de flujo que conecte directamente con esa necesidad: por ejemplo, un catálogo de talleres de robótica/programación, registro de estudiantes, disponibilidad de mentores y equipo, y seguimiento del progreso de cada estudiante. Ese flujo permitiría comprobar valor para los beneficiarios y no solo enseñar una API.

Con el sistema técnico actualmente disponible, la demo debe presentarse con transparencia como una **plataforma parcial de gestión de arquitectura empresarial**, no como la solución STEM. Si el objetivo académico exige conservar el problema de Semana 2, sería necesario redefinir el producto y adaptar el dominio, las historias y los criterios de aceptación antes de sostener que existe consistencia problema–solución.

## Cierre

El equipo logró consolidar una especificación técnica y una primera API, además de aprender a utilizar agentes para analizar requisitos, construir backlog y revisar prioridades. Sin embargo, la calidad de la documentación no debe ocultar dos brechas: la diferencia entre contrato e implementación, y la diferencia entre el problema de Semana 2 y el dominio del producto actual. Reconocerlas permite presentar el resultado con credibilidad y definir el siguiente incremento con una dirección clara.
