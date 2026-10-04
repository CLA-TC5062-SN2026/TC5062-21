# Diferencias y resolución de conflictos — SRS de equipo
**Equipo 21 · Plataforma de Arquitectura Empresarial**
Este documento sustenta la Parte 0 de S02-A2: documenta qué aportó cada integrante al `SRS_equipo.md` y cómo se resolvió cada conflicto. Se basa en `Analisis_comparativo_SRS_equipo.docx` (análisis de diferencias entre los tres SRS individuales) y en las reglas ya fijadas en `SRS_equipo.md` §2.4 y §3.4.

**Documentos de entrada**
| Documento | Autor | Rol en la comparación |
|---|---|---|
| SRS Gregorio (`S02_A1/SRS_final.md`) | Gregorio | SRS individual 1 |
| SRS Liciel (`SRS_final.md` v1.1) | Liciel Reyes Ávila | SRS individual 2 |
| SRS Jean Paul (`SRS_final-2.md` v1.1) | Jean Paul Lozano Gámiz | SRS individual 3 |
| `Analisis_comparativo_SRS_equipo.docx` | — | Análisis de consenso, gaps y conflictos entre los tres |

**Advertencia de identificadores.** Los tres SRS reutilizan IDs como `RF-01` para funciones distintas. La comparación se hizo por comportamiento, no por número de RF. `SRS_equipo.md` define una serie canónica propia (`RF-01` a `RF-19`, 56 AC); ningún ID individual se traslada automáticamente.

---

## 1. Qué aportó cada integrante

### Consenso (los tres SRS lo pedían, aunque con reglas distintas)
Los tres documentos coincidían en la intención general de estos puntos; `SRS_equipo.md` fijó la regla única:
- Aplicación web para registrar y consultar arquitectura empresarial.
- Inicio y cierre de sesión con control de acceso (RF-01 del equipo).
- Configuración de capas/estructura desde la interfaz, sin tocar código (RF-03, RF-04).
- Campos configurables de un tipo de elemento (RF-05).
- Alta y modificación de elementos con validación (RF-06, RF-07).
- Tipos de relación y vínculos dirigidos entre elementos (RF-09 y siguientes).
- Vista visual y consulta de detalles (RF-13 a RF-15).
- Conservación de datos entre sesiones (RF-19).
- Datos ficticios para la demostración, sin integraciones automáticas ni IA en la v1.

### Aportación específica de Gregorio
- Cuatro tipos de campo predefinidos (texto, número, fecha, lista) y el bloqueo de cambios estructurales cuando el tipo ya tiene elementos — adoptado en RF-05 y en la regla 3 de §2.4.
- Búsqueda que permite nombres repetidos, distinguiéndolos por identificador, con reglas explícitas de espacios/mayúsculas/acentos — adoptado en RF-08 y en la regla 4 de §2.4.
- Exclusión de la eliminación física de elementos, capas, tipos y vínculos — adoptado en RD-05 ("no hay eliminación física ni borrados en cascada").
- Perfil de rendimiento con 1,000 elementos, 3,000 relaciones y 10 usuarios simultáneos — base de RNF-04 del equipo (ajustado a 3 s y 1,000/3,000 elementos/relaciones).

### Aportación específica de Liciel
- Permisos de edición del Editor restringidos a las capas que el Administrador le asigne, y lectura abierta a todo usuario autenticado — adoptado en RF-02-AC-1 y en la regla de "edición por capa" de §2.3.
- Estado de vigencia de las relaciones (vigente/retirada) y baja lógica con reactivación de elementos, en vez de borrado — adoptado en RF-12 (retiro) y RF-16 (baja lógica), con RD-05 ("conservación").
- Trazabilidad de creador/modificador y bitácora inmutable con valores anterior y nuevo — adoptado en RF-18.
- Función administrada para cargar un conjunto mínimo de datos de demostración (y que no se duplique al repetirse) — adoptado en RF-17.
- Justificación obligatoria de 10 a 500 caracteres en cada relación — adoptada como regla 5 de §2.4 ("propuesta... justificación de 10 a 500 caracteres").

### Aportación específica de Jean Paul
- Separación entre **proponer** una relación y **aprobar/rechazar** esa propuesta, sin alterar la relación vigente hasta la decisión — adoptado como el núcleo de RF-10 y RF-11, y como regla 6 de §2.4 ("el editor propone; el administrador aprueba o rechaza").
- La separación entre propuesta y decisión motivó una precisión del SRS conjunto: revalidar extremos y duplicados antes de aplicar un cambio (RF-12-AC-4). Esa comprobación adicional es una decisión de integración; no se atribuye como requisito literal al SRS individual de Jean Paul.
- Señalamiento explícito de reglas pendientes de precisar (compatibilidad de extremos, cambios de campos con datos) — tratado como alerta, no como regla; se resolvió con las reglas de Gregorio y Liciel en esos puntos, dejando constancia en la tabla de procedencia (§3.4) de que Jean Paul los dejaba abiertos.

---

## 2. Conflictos y cómo se resolvieron

| # | Conflicto | Gregorio | Liciel | Jean Paul | Decisión del equipo (`SRS_equipo.md`) | Dónde quedó |
|---|---|---|---|---|---|---|
| C-1 | Modelo de roles | 3 roles fijos, sin herencia | 3 roles, Administrador hereda Editor/Consulta | Roles configurables, facultades acumulables | Se mantienen 3 roles fijos, con herencia (Administrador puede todo lo de Editor y Consulta), por simplicidad de implementación en 12 semanas; no se configuran roles nuevos. | §2.3 |
| C-2 | Alcance de permisos | Sin restricción por capa/elemento | Edición por capa asignada | Permisos por elemento | Se adopta la edición por capa de Liciel (contiene el número de combinaciones de acceso); no hay permisos por elemento en la v1. | §2.3, RF-02 y RF-06 |
| C-3 | Autenticación y cuentas | Procedimiento técnico fuera de la interfaz | Gestión de usuarios y contraseñas por el Administrador en la app | Proveedor de identidad corporativo (Google) | Se adopta la gestión por el Administrador desde la plataforma (Liciel); el primer administrador se aprovisiona por instalación (elemento de Gregorio). El SSO corporativo queda como candidato futuro (§3.5). | Regla 1 de §2.4 |
| C-4 | Registro y cambios de relaciones | Editor guarda directo | Editor guarda directo | Requiere propuesta + aprobación | Se adopta el modelo de Jean Paul (propuesta/aprobación) porque distingue un vínculo revisado de uno capturado sin revisión, con menor riesgo para la demostración. | RF-10, RF-11, regla 6 de §2.4 |
| C-5 | Justificación de relaciones | Razón de negocio sin campo obligatorio | Texto obligatorio de 10–500 caracteres | Depende de los campos configurados | Se adopta el campo obligatorio de 10 a 500 caracteres de Liciel: es verificable y evita propuestas sin sustento. | RF-10-AC-3, regla 5 de §2.4 |
| C-6 | Relaciones permitidas | Cualquier tipo/capa con un tipo configurado | Tipo de relación ligado a tipos de elemento origen/destino | Pendiente de precisar | Se adopta la restricción de Liciel (tipo de relación con origen/destino definidos). Es más restrictiva que la regla de Gregorio; Jean Paul dejaba la compatibilidad por precisar. | RF-09, regla 5 de §2.4 |
| C-7 | Eliminación | Sin eliminación de ningún tipo | Eliminación definitiva administrada, con cascada de relaciones | Eliminar solo sin dependencias, sin cascada | Se adopta "sin eliminación física ni cascada" (Gregorio/Jean Paul): se usa baja lógica (Liciel) en su lugar. La eliminación definitiva queda fuera de la v1. | RD-05, RF-16, §3.5 |
| C-8 | Cambios de campos con datos existentes | Bloqueados si el tipo tiene elementos | Se permite agregar obligatorios y desactivar con datos | Pendiente de precisar | Se adopta el bloqueo de Gregorio: ningún cambio de estructura (tipo, obligatoriedad, opciones) se permite si el tipo ya tiene elementos; solo se editan valores. Evita migraciones de datos implícitas en 12 semanas. | Regla 3 de §2.4 |
| C-9 | Nombres de elementos | Permite repetidos, distingue por ID | Exige nombre único por tipo | Sin regla equivalente | Se adopta la postura de Gregorio: se permiten nombres repetidos y la búsqueda siempre distingue por identificador. | RF-08, regla 4 de §2.4 |
| C-10 | Tipos de campo | 4 tipos (texto, número, fecha, lista) | 7 tipos (incluye sí/no y referencia a usuario) | 4 tipos iniciales | Se adoptan los 4 tipos de Gregorio/Jean Paul para la v1; sí/no y referencia a usuario quedan como candidatos futuros. | RF-05, §3.5 |
| C-11 | Rendimiento | 3 s, 1,000 elementos, 3,000 relaciones, 10 usuarios | 3 s, 100 nodos, 20 usuarios | 2 s, 10 elementos visibles, 20 usuarios | Se fija un solo perfil para la v1 (no se promedian las tres pruebas): 3 s por operación, con 1,000 elementos, 3,000 relaciones y 10 sesiones simultáneas, siguiendo el escenario más detallado (Gregorio). | RNF-04 |

### Decisiones aplazadas (quedan fuera de la primera entrega)
Documentadas en `SRS_equipo.md` §3.5: perspectivas y subniveles jerárquicos, roles configurables, permisos por elemento, SSO corporativo, los tres tipos de campo adicionales de Liciel, migración de definiciones con datos existentes, estado "planeada" de relaciones, eliminación física protegida, exportación y análisis automático. Ningún integrante pierde su propuesta: quedan como candidatos para una versión posterior, con su propia validación y estimación.

---

## 3. Resultado
`SRS_equipo.md` v1.0: **19 RF con 56 criterios de aceptación, 10 RNF y 7 RD**, con tabla de procedencia (§3.4) que rastrea cada RF del equipo a los RF de origen de Gregorio, Liciel y Jean Paul. Este documento es ahora la fuente de verdad para el diseño de API (S04-A2), el backlog de esta actividad y las pruebas de S09-A1.
