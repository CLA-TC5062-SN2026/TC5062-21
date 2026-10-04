# Reflexión sobre Scrum y el uso de IA

**Proyecto:** Plataforma de Arquitectura Empresarial · Equipo 21  
**Base de la reflexión:** `SRS_equipo.md`, `backlog.md`, `ajustes_backlog.md` y `priorizacion_comparada.md`.

## 1. Ventajas y riesgos de usar IA para generar el Product Backlog

La ventaja más visible es la **rapidez para convertir un SRS extenso en una primera propuesta organizada**. El agente puede identificar grupos funcionales, redactar historias con el formato «Como…, quiero…, para…» y relacionarlas con criterios de aceptación. En este proyecto ayudó a estructurar cinco épicas y a mantener la referencia de cada historia a los IDs `RF-XX-AC-Y` del SRS. Esa trazabilidad facilita comprobar que el backlog cubra los requisitos y detectar huecos: por ejemplo, durante la integración se identificó que faltaba una historia para la recuperación de datos entre sesiones y se añadió US-21.

Otra ventaja es que la IA permite **revisar alternativas con poco costo**. Se pueden comparar agrupaciones, separar historias demasiado grandes y explorar distintos órdenes de prioridad antes de mover tarjetas en GitHub Projects. En la Parte 3, la propuesta de Product Owner destacó el valor de mantener los datos, capturarlos y consultarlos, mientras que el backlog original daba más peso al recorrido mínimo demostrable. Esa diferencia sirve para discutir decisiones, no para aceptar automáticamente la respuesta del agente.

El riesgo principal es que una salida bien redactada parezca correcta aunque no lo sea. El primer borrador registrado en `ajustes_backlog.md` asignaba casi siempre tres puntos, mezclaba acciones distintas en una historia, omitía la asignación de capas en US-03 y no citaba los criterios del SRS. También trataba validaciones como historias cuyo actor era «el sistema», sin expresar el valor para una persona. De haber publicado ese borrador sin revisión, el equipo habría tenido un backlog difícil de estimar y de comprobar. La IA también puede interpretar de forma incorrecta una regla ambigua, introducir funciones que nadie acordó o colocar una historia arriba por sonar importante sin conocer las restricciones reales del equipo.

Por eso, el uso adecuado en este ejercicio fue **generar, contrastar y corregir**. Cada historia debe revisarse contra el SRS; sus criterios deben ser observables; las estimaciones deben discutirse con quienes implementarán el trabajo; y la prioridad debe justificarse con el valor esperado y las dependencias. El agente acelera la preparación, pero la revisión humana determina si el resultado representa el producto que se quiere construir.

## 2. ¿Puede un agente reemplazar al Product Owner?

**No puede reemplazarlo como responsable de las decisiones de producto.** Según la [Guía Scrum oficial](https://scrumguides.org/scrum-guide.html?lang=en), el Product Owner responde por maximizar el valor del producto y por la gestión eficaz del Product Backlog, incluido su orden. Puede delegar trabajo, pero conserva esa responsabilidad. Un agente puede preparar análisis, proponer prioridades y señalar inconsistencias; no posee por sí mismo el mandato del equipo ni la relación directa con quienes usarán o financiarán el producto.

En este proyecto, el agente pudo argumentar que US-21 (recuperar datos entre sesiones) aporta más valor inmediato que US-20 (datos de demostración). Sin embargo, un Product Owner tendría que comprobar si la entrega académica exige mostrar datos ficticios, si hay tiempo para capturarlos manualmente y qué consideran más útil los usuarios. Esas condiciones pueden cambiar el orden de implementación. El agente tampoco puede asumir el compromiso de explicar una decisión al equipo, negociar el alcance ante nueva información o responder por los resultados del producto.

La postura de esta reflexión es usarlo como **apoyo para el Product Owner**: produce borradores y escenarios de priorización que hacen más rápida la conversación. La decisión final debe quedar en una persona responsable, informada por el equipo y por la retroalimentación de los usuarios. La comparación de la Parte 3 muestra precisamente por qué conviene conservar ese juicio: la propuesta de priorización subió US-10 y bajó US-05 respecto del backlog creado, una diferencia razonable que requiere valorar el contexto del proyecto antes de aplicarla.

## 3. ¿Cómo afecta la calidad del SRS a la calidad del backlog?

El SRS define el material del que se derivan las historias. Si especifica **actores, reglas, límites y criterios verificables**, el backlog puede expresar una necesidad concreta y sus condiciones de aceptación. En nuestro SRS, los IDs `RF-XX-AC-Y` permitieron rastrear el origen de los criterios. Reglas precisas, como distinguir elementos con el mismo nombre por identificador o impedir que un Editor modifique capas no asignadas, se trasladaron a US-15 y US-03 sin quedar reducidas a frases genéricas.

Si el SRS es incompleto o contradictorio, la IA puede producir historias aparentemente completas que heredan esos defectos. Un requisito vago como «gestionar relaciones» podría terminar en una sola historia que mezcle proponer, aprobar, cambiar y retirar. Al separar esas acciones en US-11, US-12 y US-13, el backlog ganó actores claros, criterios comprobables y estimaciones más útiles. También se detectó que RF-19 aparecía en el SRS de equipo pero no estaba representado en la primera versión del backlog: de ahí surgió US-21. Ese caso muestra que incluso con un SRS relativamente sólido hace falta verificar la cobertura, no solo confiar en la generación inicial.

En conclusión, **un SRS claro mejora la precisión y la trazabilidad del backlog, pero no sustituye su refinamiento**. El equipo debe comprobar que cada requisito importante aparezca en alguna historia, que ninguna historia contradiga las reglas acordadas y que sus criterios puedan probarse. La IA ayuda a realizar esa comprobación; la calidad final depende de la calidad de la fuente y de la revisión del equipo.
