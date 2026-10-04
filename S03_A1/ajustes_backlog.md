# Ajustes al backlog — Parte 1 (S02-A2)
Bitácora de la revisión crítica del borrador que el agente propuso a partir de `SRS_equipo.md`, antes de llegar a `backlog.md`.

## Borrador inicial del agente
Generó 5 épicas replicando directamente los 6 grupos de funciones de §2.2 del SRS (Acceso, Configuración, Captura, Validación, Consulta, Conservación), fusionando Captura y Validación en una sola épica. Para cada RF propuso una historia 1 a 1, con 2 criterios de aceptación copiados casi literalmente del SRS y una estimación uniforme de 3 puntos para casi todas las historias, salvo las de inicio de sesión y detalle de vínculo, que puso en 1.

## Problemas encontrados y correcciones

| # | Problema en el borrador | Corrección aplicada |
|---|---|---|
| 1 | Estimaciones casi todas en 3 puntos, sin relación con la complejidad real. "Aprobar o rechazar una propuesta" (US-12) tenía 3 puntos igual que "cerrar una sesión" (US-02). | Reestimé por complejidad real: US-12 subió a 8 porque además de aprobar/rechazar incluye la revalidación de extremos y duplicados al momento de decidir (RF-12-AC-4), que es lógica adicional no trivial. US-02 bajó a 2 por ser una operación simple de invalidar un token. |
| 2 | "Iniciar sesión" y "cerrar sesión" estaban en una sola historia, mezclando dos acciones con dueños y momentos distintos. | Separé en US-01 (inicio) y US-02 (cierre de una sesión individual), cada una con sus propios AC, porque son dos entregables independientes y el cierre de una sesión específica entre varias (RF-01-AC-3) merece su propio criterio. |
| 3 | La historia de "crear cuenta" no mencionaba la asignación de capas editables, que es una regla central del SRS de equipo (§2.3) y no un detalle menor. | Reescribí US-03 para incluir explícitamente la asignación de capas al crear la cuenta, con un AC que prueba que un Editor sin capas asignadas no puede escribir. |
| 4 | El agente redactó "Como usuario, quiero gestionar relaciones, para tener el sistema actualizado" como una sola historia enorme que mezclaba proponer, aprobar, cambiar y retirar — no era accionable ni estimable como una unidad. | Dividí en cuatro historias independientes (US-11 proponer alta, US-12 aprobar/rechazar, US-13 cambiar o retirar, US-14 baja lógica de elementos), cada una con su propio dueño (Editor o Administrador) y sus propios AC, siguiendo la separación propuesta–decisión que el equipo adoptó de Jean Paul. |
| 5 | Ningún AC citaba el ID de criterio del SRS (`RF-XX-AC-Y`), rompiendo la trazabilidad que pide la actividad. | Agregué la referencia entre paréntesis a cada AC, apuntando al criterio exacto de `SRS_equipo.md` del que deriva. |
| 6 | La historia de búsqueda no mencionaba que el SRS exige distinguir nombres repetidos por identificador (aporte de Gregorio, regla 4 de §2.4), un punto que el equipo discutió explícitamente como conflicto resuelto. | Añadí ese comportamiento al AC-2 de US-15, con datos de ejemplo (dos "Proyecto Alfa" con IDs distintos). |
| 7 | Faltaba una historia para cargar los datos de demostración (RF-17), que facilita probar el resto del backlog sin captura manual. | Agregué US-20. Su prioridad inicial era Baja y se revisó a Media durante la integración porque RF-17 forma parte del alcance de la primera entrega. |
| 8 | El agente priorizó todo como "Alta" salvo dos historias, lo que no sirve para planear sprints. | Repriorizé con un criterio explícito: Alta son las historias que forman el recorrido mínimo demostrable (entrar, configurar, capturar, proponer/aprobar un vínculo, explorarlo); Media son necesarias pero no bloquean la primera demo; Baja es solo la carga de datos de ejemplo. |
| 9 | Dos historias usaban "el sistema" como actor ("Como sistema, quiero validar..."), lo que no es una historia de usuario válida (sin valor de negocio para una persona). | Reescribí esas validaciones (p. ej., campos obligatorios, tipo de dato) como criterios de aceptación dentro de las historias de captura (US-09, US-10) en vez de historias independientes. |
| 10 | El borrador no incluía un resumen de puntos por épica ni por prioridad, dificultando ver el tamaño total del backlog. | Agregué la tabla de resumen al final de `backlog.md`. La primera revisión sumaba 74 puntos en 20 historias; tras la integración, el resumen actualizado suma 79 puntos en 21 historias. |

## Revisión de integración del 3 de octubre de 2026

| Hallazgo | Cambio aplicado al backlog de `S03_A1` |
| --- | --- |
| RF-19 aparecía en la descripción de la épica E5, pero ninguna historia comprobaba la persistencia entre sesiones. | Se agregó US-21, Recuperación de datos entre sesiones, con dos criterios tomados de RF-19-AC-1 y RF-19-AC-2, 5 puntos y prioridad Alta. |
| US-11 y US-12 eran de prioridad Alta, pero la definición del tipo de relación de la que dependen (US-08) era Media. | US-08 pasó a Alta para que el recorrido de propuesta y aprobación pueda planearse en orden de dependencia. |
| US-20 implementa RF-17, que forma parte del alcance acordado para la primera entrega, pero figuraba como Baja. | US-20 pasó a Media. Se quitó «con un clic» de la historia porque el SRS no exige esa interacción específica. |
| El AC-2 de US-03 citaba de forma indirecta un RF del SRS individual de Liciel y atribuía la regla de capas a §2.4. | Se trazó al SRS de equipo §2.3 y RF-06-AC-3. |
| El AC-1 de US-15 omitía la segunda página y el desempate por identificador; US-12 contenía la errata «aprubo». | Se completó el criterio de US-15 conforme a RF-08-AC-1 y se corrigió «apruebo». |

## Resultado
`backlog.md`: 5 épicas, 21 historias de usuario (mínimo pedido: 10; recomendado: 15), cada una con al menos 2 criterios de aceptación trazables a `SRS_equipo.md`, estimación en Fibonacci y prioridad. El total es **79 story points**. Las 19 funciones RF del SRS tienen al menos una historia asociada.

## Decisiones de planificación
- US-12 se mantiene como una historia de 8 puntos: la decisión y la revalidación forman una sola operación atómica. Si durante la implementación supera la capacidad de un sprint, se dividirá sin cambiar el resultado exigido por RF-11 y RF-12.
- US-20 queda en prioridad Media y puede implementarse antes de las pruebas integradas para evitar repetir la captura manual. No bloquea la construcción inicial de las funciones de alta y consulta.
