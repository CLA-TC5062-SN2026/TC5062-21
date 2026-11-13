# Reflexión sobre deuda técnica y calidad en SCRUM

Equipo 21 · TC5062 · Semana 9 · 13 de noviembre de 2026

Preparado para Jean Paul Lozano Gámiz con asistencia de Codex. Prioridad indicada por el estudiante: mejorar el rendimiento al crecer los datos.

## Mi prioridad de calidad

Mi prioridad para este proyecto es **mejorar el rendimiento al crecer los datos**. En una muestra pequeña, cargar todos los elementos para mostrar una página puede pasar desapercibido. Al medirlo encontré una señal concreta: mostrar 25 resultados necesitaba 122 consultas con 60 elementos y 602 con 300. Esta diferencia justifica atender la forma de consultar antes de ampliar el volumen de uso.

También considero necesario conservar el comportamiento. Reducir consultas pierde valor si cambia los permisos, deja un registro incompleto o genera movimientos de bitácora al repetir la misma operación. Por eso la evaluación combina análisis estático, lectura del código y pruebas sobre PostgreSQL.

## Cuánta deuda se observa y cómo la mediría

La deuda observada es relevante en rendimiento y mantenibilidad, aunque el alcance funcional probado continúa funcionando. No tengo una estimación validada del costo total de corregirla ni evidencia para asignarle una categoría financiera. La línea base contiene siete hallazgos manuales: seis importantes y uno menor. Se implementaron tres mejoras prioritarias; permanecen la separación completa de Service (parcialmente mitigada), la duplicación de proyecciones de propuestas, el diagnóstico de errores y la claridad de nombres internos.

| Indicador y unidad | Antes | Después | Qué permite decidir |
| --- | ---: | ---: | --- |
| SELECT de aplicación por página de 25, con 300 elementos | 602 | 53 | Confirmar que ya no se serializa todo el conjunto y priorizar el N+1 residual |
| SELECT para guardar ocho campos numéricos | 10 | 2 | Verificar que el costo no crece por una consulta de valor anterior por entrada |
| SELECT para cambiar un nombre con nueve campos | 57 | 30 | Medir la reutilización del estado final, junto con la mejora del guardado |
| Mensajes Pylint, código de producto | 518 | 492 | Vigilar tendencias por regla y distinguir alertas justificadas |
| Mensajes por mil líneas físicas | 443.49 | 384.98 | Comparar densidad declarando el denominador: 1,168/1,278 líneas |
| Métodos públicos en Service, según Pylint | 74 | 74 | Mantener visible la concentración de responsabilidades |
| Casos pytest aprobados | 50 de 50 | 84 de 84 | Confirmar regresiones cubiertas; no equivale a cobertura de líneas |

Los conteos de consultas usan datos ficticios controlados. No permiten prometer un tiempo de respuesta con miles de usuarios. El siguiente paso de medición sería observar p50/p95 de latencia con volumen y concurrencia definidos, registrar el costo de conteo y páginas profundas y evaluar el bloqueo global de escrituras. Los criterios de aceptación se fijarían antes de esa prueba.

Los mensajes de Pylint tampoco equivalen a defectos únicos: una firma recibe avisos por número de argumentos y por argumentos posicionales. Los modelos ORM y protocolos pueden activar heurísticas que no justifican modificar su diseño. Mantendría los hallazgos confirmados separados de esos avisos.

## Deuda intencional e involuntaria

| Decisión o problema del proyecto | Clasificación y evidencia | Seguimiento |
| --- | --- | --- |
| Un bloqueo transaccional común para las escrituras | **Intencional y documentada.** `main.py:48–52` explica que evita carreras en último administrador y relaciones, y que se eligió para carga académica. Simplifica integridad a cambio de concurrencia. | Conservar hasta medir; evaluar bloqueos más específicos con pruebas de carreras y sin perder consistencia. |
| Métodos con nombres iguales a operationId y firma uniforme p/q/b | **Decisión de compatibilidad identificable.** `main.py:88–89` y `services.py:134` conectan contrato y despacho. Parte de las advertencias se acepta por ese adaptador. | Aclarar nombres locales y mover firmas específicas a servicios internos, conservando la interfaz HTTP. |
| Serializar todo antes de recortar la página | **Deuda sin justificación documentada; se gestiona como involuntaria.** No hay evidencia de una decisión explícita que aceptara ese costo. H01 y las mediciones muestran el efecto. | R1 limita la carga; medir después el conteo, offsets altos y consultas restantes dentro de la página. |
| Leer el valor anterior por cada campo y repetir el estado final | **Deuda sin justificación documentada.** H02/H03 muestran trabajo repetido y reglas mezcladas. | R2/R3 implementadas y protegidas por pruebas de consultas e historial. |
| Service concentrado y proyección duplicada de propuestas | **Origen no acreditado.** No puedo afirmar que el equipo aceptó deliberadamente este acoplamiento. | Registrar H04/H05, dividir el trabajo por dominio y validar con pruebas antes de sustituir cada parte. |

No atribuyo intenciones al equipo solo por encontrar una solución rápida. Una deuda deliberada debe registrar motivo, costo aceptado, condición de revisión y responsable. Sin ese registro, la clasificación conserva la incertidumbre.

## Cómo incorporaría calidad y SOLID al flujo de SCRUM

| Momento | Acción concreta para este proyecto | Evidencia y criterio |
| --- | --- | --- |
| Refinamiento | Registrar cada deuda con ubicación, efecto, frecuencia y prueba que la evidencia. Vincularla con la historia afectada. | H01–H07 como punto de partida; separar rendimiento, defectos y convenciones. |
| Planeación | Priorizar junto con las funcionalidades. Proponer inicialmente hasta 15% de capacidad para deuda, a negociar según riesgo y tamaño del sprint. | Capacidad acordada y objetivo verificable; el porcentaje es una propuesta, no un acuerdo ya celebrado. |
| Desarrollo | Revisar SRP al añadir una regla; usar dependencias pequeñas para las consultas que requiere; evitar nuevas duplicaciones del estado de propuestas. | Pruebas unitarias de reglas y de integración para persistencia, permisos y transacciones. |
| Revisión del cambio | Evaluar los cinco principios SOLID con ejemplos concretos. Revisar entradas, errores, secretos y número de consultas. | Una revisión de otra persona cuando esté disponible. Si trabajo solo, revisión diferida del diff y anotación de ese límite; no se registra como revisión independiente. |
| Definition of Done propuesta | Ejecutar la suite, conservar las 46 operaciones del recorrido, cumplir los presupuestos de consulta y revisar alertas nuevas. | 84 casos actuales verdes; en la muestra fijada, ≤55 SELECT por página, ≤2 por ocho campos numéricos y ≤30 por modificación. Sin errores E/F nuevos ni alertas importantes nuevas sin disposición documentada. |
| Integración continua futura | Automatizar instalación fijada, Pylint, pytest y comparación contra la línea base. Usar PostgreSQL con el esquema del proyecto. | Configuración revisada antes de activarla. Esta entrega aporta comandos y evidencia local; no afirma que exista un pipeline remoto nuevo. |
| Revisión del sprint | Mostrar el recorrido funcional y la comparación de consultas con las mismas condiciones. | Producto funcionando y resultados reproducibles, además de la puntuación del linter. |
| Retrospectiva | Analizar por qué una página pequeña cargaba todo el conjunto y por qué no se detectó con muestras menores. | Añadir volumen y presupuestos de consultas a futuras pruebas; revisar reincidencia en el siguiente sprint. |

## Backlog propuesto

| Orden | Pendiente | Condición de cierre |
| --- | --- | --- |
| 1 | Reducir consultas por tipo/capa dentro de una página y medir COUNT/OFFSET | Comparación con volumen mayor, mismos filtros y orden; definir presupuesto antes de implementar |
| 2 | Medir concurrencia del bloqueo global | Escenario y carga definidos; ninguna pérdida de unicidad, autorización o versión |
| 3 | H04: separar Service por dominios | Componentes con responsabilidades delimitadas y recorridos existentes aprobados |
| 4 | H05: centralizar la proyección de propuestas | Corrección/aprobación/retirada usan la misma representación, con pruebas de versión y permisos |
| 5 | H06: añadir diagnóstico seguro | Error correlacionable y prueba de no exposición de tokens, contraseñas o parámetros |
| 6 | H07 y convenciones menores | Diff de legibilidad sin alterar operationId ni el contrato; revisar advertencias justificadas |

Este orden prioriza crecimiento, pero un defecto de seguridad o pérdida de datos confirmado tendría prioridad inmediata. Las tareas son propuestas para acordar y estimar; no se inventan responsables ni compromisos de otros integrantes.

## Relación con SWEBOK

La guía de estudio suministrada para la semana vincula calidad con necesidades, mediciones y acciones de mejora (SWEBOK v4.0a, cap. 12, §§2.2–2.4.1). En este trabajo, la necesidad de crecer se conecta con un costo observable, un cambio concreto y evidencia de su efecto. La clasificación distingue alertas del analizador, problemas confirmados y límites de las pruebas.

El capítulo 4, §§3.3–3.6, reúne prácticas de codificación y técnicas de calidad de construcción. Aquí se aplican conjuntamente revisión, análisis estático, pruebas unitarias e integración. La verificación observa que se conserva el contrato probado; la validación del rendimiento en un entorno representativo de uso queda como siguiente actividad, porque contar SELECT no reproduce por sí solo la carga real.

## Referencias

- Canvas, **Aprende | Calidad de Código y Deuda Técnica**, consulta del 13 de noviembre de 2026. [Material del curso](https://experiencia21.tec.mx/courses/708363/pages/aprende-%7C-calidad-de-codigo-y-deuda-tecnica?module_item_id=44839064).
- Canvas, **Construye | Auditoría de Calidad de Código | Colaborativa**, consulta del 13 de noviembre de 2026. [Consigna y rúbrica](https://experiencia21.tec.mx/courses/708363/assignments/23606080?module_item_id=44839066).
- **Guía de estudio SWEBOK v4.0a · Semana 9**, archivo suministrado `guia_swebok_semana_9.md`. Referencia de esa guía: IEEE Computer Society, *Guide to the Software Engineering Body of Knowledge*, v4.0a, Hironori Washizaki (ed.), agosto de 2026. Las secciones se toman de la guía proporcionada; no se presenta como una nueva verificación del PDF original.
- Pylint. [Opciones e informes oficiales](https://pylint.pycqa.org/en/stable/user_guide/usage/output.html). Uso del reporte como señal estática complementaria a pruebas.

**Nota de autoría:** reflexión preparada con asistencia de Codex a partir del código, las ejecuciones y la prioridad expresada por Jean Paul. Antes de entregar, el estudiante debe revisar que las valoraciones representan su criterio, conforme al requisito de explicación propia de la rúbrica.
