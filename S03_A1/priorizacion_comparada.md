# Priorización comparada del backlog — Parte 3

**Proyecto:** Plataforma de Arquitectura Empresarial · Equipo 21  
**Fecha:** 3 de octubre de 2026  
**Fuentes:** `SRS_equipo.md`, `backlog.md` y `ajustes_backlog.md` de `S03_A1`  
**Alcance:** 21 historias, 79 story points. Este análisis propone un orden; no cambia los Issues ni sus etiquetas en GitHub.

## 1. Priorización desde el rol de Product Owner

**Objetivo de producto.** Permitir que un equipo registre elementos de arquitectura, mantenga sus datos entre sesiones y consulte relaciones confiables para entender el impacto de cambios. El valor principal aparece cuando la información capturada puede recuperarse, encontrarse y conectarse de manera controlada.

**Criterio de orden.** Primero ponderé el resultado visible para los usuarios y la continuidad de la información; después, el riesgo de que el flujo principal quede incompleto. Usé las dependencias para decidir qué construir antes, pero distinguí ese orden técnico del valor de negocio. Los story points ayudan a planear capacidad; no equivalen a valor. La categoría **Alta / Media / Baja** de esta tabla es relativa para planear entregas: que una historia quede al fondo no elimina su alcance del SRS.

| Orden PO | Historia | Puntos | Prioridad PO | Motivo principal |
|---:|---|---:|---|---|
| 1 | US-21 Recuperación entre sesiones | 5 | Alta | Sin conservar datos, el trabajo de captura y configuración pierde utilidad tras cerrar la sesión. |
| 2 | US-09 Registro de elementos | 5 | Alta | Crea el contenido que el resto del producto permite consultar y relacionar. |
| 3 | US-15 Búsqueda de elementos | 3 | Alta | Hace utilizable la información capturada y distingue registros con nombres repetidos. |
| 4 | US-16 Mapa de relaciones | 5 | Alta | Expone el beneficio central de comprender vínculos y dependencias de arquitectura. |
| 5 | US-12 Aprobación o rechazo | 8 | Alta | Garantiza que el mapa muestre relaciones revisadas, no propuestas sin validar. |
| 6 | US-11 Propuesta de relaciones | 5 | Alta | Permite construir vínculos sin publicarlos antes de su revisión. |
| 7 | US-01 Inicio de sesión | 3 | Alta | Habilita un acceso controlado al modelo y a las funciones por rol. |
| 8 | US-03 Alta de cuentas, roles y capas | 5 | Alta | Permite colaborar sin conceder edición indiscriminada. |
| 9 | US-06 Tipos de elemento | 3 | Alta | Da estructura a los registros que se capturarán. |
| 10 | US-07 Campos y obligatoriedad | 5 | Alta | Asegura datos consistentes desde el alta de los elementos. |
| 11 | US-08 Tipos de relación | 3 | Alta | Evita vínculos incompatibles y habilita el flujo de propuestas. |
| 12 | US-10 Modificación de elementos | 3 | Alta | Mantiene vigente la información sin obligar a recrear registros. |
| 13 | US-05 Creación de capas | 3 | Media | Extiende el modelo; las cuatro capas iniciales permiten empezar a capturar antes. |
| 14 | US-19 Trazabilidad de autor y fecha | 3 | Media | Aumenta la confianza en los datos y permite explicar cambios. |
| 15 | US-18 Detalle de un vínculo | 2 | Media | Da contexto a una relación ya visible en el mapa. |
| 16 | US-17 Filtros del mapa | 3 | Media | Mejora la exploración cuando el mapa ya contiene suficientes relaciones. |
| 17 | US-14 Baja y reactivación | 3 | Media | Permite retirar elementos obsoletos sin perder historial. |
| 18 | US-04 Cambio de rol | 3 | Media | Atiende cambios organizativos posteriores al alta inicial de cuentas. |
| 19 | US-13 Cambio o retiro de relación | 5 | Baja | Mantiene relaciones existentes; primero deben poder proponerse y aprobarse. |
| 20 | US-20 Datos de demostración | 2 | Baja | Facilita pruebas y presentación, pero no aporta una función de uso cotidiano al usuario final. |
| 21 | US-02 Cierre de una sesión individual | 2 | Baja | Mejora el control de sesiones múltiples; el primer recorrido de negocio funciona sin esta opción específica. |

**Por qué están arriba.** US-21, US-09, US-15 y US-16 forman la cadena de valor: guardar información, recuperarla, encontrarla y entenderla. US-11 y US-12 completan esa cadena al incorporar relaciones confiables. La autenticación, los permisos y la configuración del modelo sostienen ese resultado y deben entrar temprano en la construcción.

**Por qué están abajo.** US-13, US-20 y US-02 son valiosas y siguen comprometidas en el SRS. Su beneficio se aprovecha después de que el flujo principal está operativo. US-20 puede adelantarse tácticamente para probar o presentar el sistema, aunque su valor de negocio directo sea menor.

### Orden sugerido de implementación

El orden de valor anterior **no es una secuencia técnica literal**. Para que cada incremento funcione, conviene construir primero las bases: US-01 → US-21 → US-06 → US-07 → US-03 → US-09 → US-15 → US-08 → US-11 → US-12 → US-16. US-05 puede adelantarse si el equipo necesita una capa distinta de las cuatro iniciales. US-20 puede programarse antes de una prueba integrada para ahorrar captura manual.

## 2. Comparación con la priorización del backlog creado

Para la comparación solicitada se toma como **priorización propia de referencia** la que quedó documentada en el backlog creado para esta actividad. `backlog.md` clasifica 12 historias como **Alta**, 9 como **Media** y ninguna como **Baja**. Esa clasificación fue revisada en `ajustes_backlog.md` con foco en un recorrido mínimo demostrable y en cubrir el alcance del SRS.

| Historia o grupo | Backlog actual | Propuesta PO | Coincidencia o diferencia y razón |
|---|---|---|---|
| US-01, US-03, US-06–US-09, US-11, US-12, US-15, US-16 y US-21 | Alta | Alta | Coinciden: permiten acceder, configurar, capturar, validar, consultar y conservar información. |
| US-10 Modificación de elementos | Media | Alta | Difieren: corregir información existente es esencial para que el modelo siga siendo útil después de la primera carga. |
| US-05 Creación de capas | Alta | Media | Difieren: el sistema ya dispone de cuatro capas iniciales; crear más puede esperar si el primer caso de uso cabe en ellas. |
| US-04, US-14, US-17–US-19 | Media | Media | Coinciden: mejoran administración, ciclo de vida, consulta y confianza una vez establecido el flujo central. |
| US-02, US-13 y US-20 | Media | Baja relativa | Difieren: aportan sobre todo a casos posteriores o a la preparación de pruebas. Siguen siendo parte del alcance y no se descartan. |

La coincidencia es amplia: 11 de las 12 historias que el backlog actual llama **Alta** permanecen en la franja alta del PO. La diferencia más importante es el intercambio entre US-05 y US-10. Además, el PO crea una franja baja relativa para hacer explícitos los compromisos que podrían planearse en una entrega posterior.

## 3. Conclusión para la planificación

La primera entrega debería demostrar datos persistentes, elementos capturados y localizables, y relaciones aprobadas visibles en el mapa. Las historias de mantenimiento, exploración avanzada y datos de demostración pueden planearse alrededor de ese recorrido según la capacidad del equipo. Antes de modificar prioridades en GitHub Projects, el equipo debe acordar si adopta esta propuesta o conserva las etiquetas actuales.
