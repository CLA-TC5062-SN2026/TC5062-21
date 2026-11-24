# Matriz de trazabilidad requerimientos–implementación

**Proyecto:** Plataforma de Arquitectura Empresarial · Equipo 21  
**Fuentes:** `S03_A1/SRS_equipo.md` (SRS v1.0), `S03_A1/backlog.md`, `S09_A1/codigo/S05_S06_A1/openapi_equipo.yaml`, `S09_A1/codigo/backend/app/`, `S09_A1/codigo/backend/tests/` y evidencias de `S09_A1/evidencias/despues/`.

## Criterios de lectura

- Los IDs RF y sus criterios de aceptación corresponden a la serie canónica del SRS del equipo.
- Las historias se vinculan según los criterios de aceptación que citan explícitamente los RF.
- Las rutas son endpoints del backend bajo el prefijo `/api`.
- **Completo en backend** significa que la funcionalidad del servicio está implementada y respaldada por pruebas del backend. No implica que exista una interfaz web terminada.
- **Parcialmente implementado** significa que hay lógica de API, pero no se cubre la experiencia visual requerida por el SRS.
- La evidencia de Semana 9 registra 84 pruebas aprobadas y la prueba `test_all_46_operations_and_persistence`, que recorre las 46 operaciones del contrato y valida esquemas de respuesta.

## Matriz

| Requerimiento funcional del SRS | Historia(s) del backlog | Endpoint(s) implementado(s) | Prueba / evidencia | Estado y justificación |
|---|---|---|---|---|
| **RF-01 — Inicio y cierre de sesión** | US-01, US-02 | `POST /api/v1/sesiones; GET y DELETE /api/v1/sesiones/actual; POST /api/auth/login; GET /api/auth/me` | `test_integration.py (flujo de autenticación/sesiones); cobertura de operaciones (46 operaciones)` | **Completo en backend.** Las operaciones de autenticación y sesión forman parte del contrato ejecutado y están cubiertas por el recorrido de integración. No se acredita interfaz web. |
| **RF-02 — Cuentas, roles y capas editables** | US-03, US-04 | `GET/POST /api/v1/usuarios; GET/PATCH /api/v1/usuarios/{usuarioId}; PUT/GET /api/v1/usuarios/{usuarioId}/capas-editables; POST /api/v1/usuarios/{usuarioId}/restablecimientos-contrasena` | `test_integration.py; test_quality_integration.py; cobertura de operaciones` | **Completo en backend.** Se implementan altas, consulta, actualización, asignación de capas y restablecimiento. Las reglas de roles y protección del último administrador se validan en las pruebas de integración. |
| **RF-03 — Gestión de capas** | US-05 | `GET/POST /api/v1/capas; GET/PATCH /api/v1/capas/{capaId}` | `test_integration.py; cobertura de operaciones` | **Completo en backend.** Las operaciones CRUD previstas para capas están incluidas en el recorrido de las 46 operaciones. |
| **RF-04 — Tipos de elemento** | US-06 | `GET/POST /api/v1/tipos-elemento; GET/PATCH /api/v1/tipos-elemento/{tipoId}` | `test_integration.py; cobertura de operaciones` | **Completo en backend.** La API permite crear, consultar, listar y renombrar tipos de elemento; el identificador y sus asociaciones se validan mediante integración. |
| **RF-05 — Configuración de campos** | US-07 | `GET/POST /api/v1/tipos-elemento/{tipoId}/campos; GET/PUT/DELETE /api/v1/tipos-elemento/{tipoId}/campos/{campoId}` | `test_integration.py; test_value_rules.py; cobertura de operaciones` | **Completo en backend.** La API contempla operaciones de campos y pruebas de reglas de valores y restricciones de configuración. |
| **RF-06 — Registro y modificación de elementos** | US-09, US-10 | `GET/POST /api/v1/elementos; GET/PATCH /api/v1/elementos/{elementoId}` | `test_integration.py; cobertura de operaciones` | **Completo en backend.** El recorrido de integración cubre creación, consulta y modificación de elementos con validación de esquemas. |
| **RF-07 — Validación de valores** | US-09, US-10 | `POST /api/v1/elementos; PATCH /api/v1/elementos/{elementoId}; operaciones de campos de tipo` | `test_value_rules.py; test_integration.py` | **Completo en backend.** Existen pruebas específicas para reglas de valores, campos obligatorios y tipos de datos, además de integración con el contrato. |
| **RF-08 — Listado, búsqueda y detalle de elementos** | US-15 | `GET /api/v1/elementos; GET /api/v1/elementos/{elementoId}` | `test_integration.py; test_quality_integration.py; cobertura de operaciones` | **Completo en backend.** La API implementa listado, filtros/búsqueda, paginación y consulta de detalle. La auditoría de calidad incluye mediciones para páginas de 25 resultados. |
| **RF-09 — Configuración de tipos de relación** | US-08 | `GET/POST /api/v1/tipos-relacion; GET/PATCH /api/v1/tipos-relacion/{tipoRelacionId}` | `test_integration.py; cobertura de operaciones` | **Completo en backend.** Las operaciones de tipos de relación se recorren y validan contra el contrato. |
| **RF-10 — Propuestas de alta de relación** | US-11 | `GET/POST /api/v1/propuestas-relacion; GET/PATCH /api/v1/propuestas-relacion/{propuestaId}` | `test_integration.py; cobertura de operaciones` | **Completo en backend.** La API implementa el registro y consulta de propuestas, con validaciones de extremos, justificación y duplicados contempladas en el flujo de pruebas. |
| **RF-11 — Decisión sobre propuestas** | US-12 | `POST/GET /api/v1/propuestas-relacion/{propuestaId}/decisiones` | `test_integration.py; cobertura de operaciones` | **Completo en backend.** El flujo de aprobación/rechazo se ejecuta en integración; se valida la respuesta de la operación y sus efectos. |
| **RF-12 — Cambios y retiro de relaciones** | US-12, US-13 | `PATCH /api/v1/propuestas-relacion/{propuestaId}; POST /api/v1/propuestas-relacion/{propuestaId}/decisiones; GET /api/v1/relaciones; GET /api/v1/relaciones/{relacionId}` | `test_integration.py; test_quality_integration.py; cobertura de operaciones` | **Completo en backend.** Se implementa el ciclo de propuesta y decisión para cambios/retiros y la consulta de relaciones. La suite de integración valida el recorrido. |
| **RF-13 — Exploración visual de conexiones** | US-16 | `GET /api/v1/mapas/{elementoId}` | `test_integration.py; cobertura de operaciones para la respuesta del mapa` | **Parcialmente implementado.** El backend calcula y devuelve los datos del mapa, pero no se encontró frontend web que represente visualmente los nodos, vínculos, recorrido y límite de visualización. |
| **RF-14 — Cruces y filtros del mapa** | US-17 | `GET /api/v1/mapas/{elementoId} (parámetros de filtro)` | `test_integration.py; cobertura de operaciones` | **Parcialmente implementado.** La API recibe filtros y devuelve el conjunto correspondiente. Falta la interfaz visual para que el usuario aplique, combine y quite filtros desde el mapa. |
| **RF-15 — Detalle de elementos y vínculos** | US-18 | `GET /api/v1/elementos/{elementoId}; GET /api/v1/relaciones/{relacionId}` | `test_integration.py; cobertura de operaciones` | **Completo en backend.** Las operaciones de detalle de elemento y relación están incluidas en el recorrido integral y validan los esquemas del contrato. |
| **RF-16 — Baja lógica y reactivación** | US-14 | `PUT /api/v1/elementos/{elementoId}/estado` | `test_integration.py; cobertura de operaciones` | **Completo en backend.** El endpoint de cambio de estado y los escenarios de ciclo de vida están implementados y probados en integración. |
| **RF-17 — Datos de demostración** | US-20 | `GET /api/v1/demostraciones/arquitectura-ficticia-v1; POST /api/v1/demostraciones/arquitectura-ficticia-v1` | `test_integration.py; cobertura de operaciones` | **Completo en backend.** Se dispone de consulta y carga idempotente de la muestra ficticia; la operación está incluida en la cobertura de integración. |
| **RF-18 — Trazabilidad y bitácora** | US-19 | `GET /api/v1/entradas-bitacora; GET /api/v1/entradas-bitacora/{entradaId}; operaciones de escritura de entidades que generan auditoría` | `test_integration.py; test_quality_integration.py; cobertura de operaciones` | **Completo en backend.** Se implementan consultas de bitácora y registro de cambios con autoría/fechas. Las pruebas de integración recorren el flujo y sus reglas. |
| **RF-19 — Almacenamiento y recuperación** | US-21 | `Operaciones persistentes de /api/v1/usuarios, /capas, /tipos-elemento, /elementos, /propuestas-relacion, /relaciones y /entradas-bitacora` | `test_integration.py::test_all_46_operations_and_persistence; test_quality_integration.py` | **Completo en backend.** El test de integración valida persistencia y recuperación a través de sesiones/operaciones. La evidencia de reproducción informa 84 pruebas aprobadas. |

## Resultado global

- **19 requerimientos funcionales trazados** (RF-01 a RF-19).
- **21 historias de usuario relacionadas** (US-01 a US-21).
- El contrato OpenAPI contempla 46 operaciones, recorridas por la prueba de integración de Semana 9.
- La suite final documentada contiene **84 pruebas aprobadas** y una advertencia de deprecación (`httpx` con `starlette.testclient`).
- RF-13 y RF-14 quedan parciales desde la perspectiva de producto porque el backend entrega datos de mapas y filtros, pero no se localizó una interfaz web que los presente y permita interactuar con ellos.

## Evidencia de pruebas en el repositorio

| Evidencia | Ubicación | Qué demuestra |
|---|---|---|
| Suite de integración | `S09_A1/codigo/backend/tests/test_integration.py` | Flujo de operaciones, validación de esquemas y persistencia; incluye `test_all_46_operations_and_persistence`. |
| Pruebas de integración de calidad | `S09_A1/codigo/backend/tests/test_quality_integration.py` | Escenarios adicionales de integridad y comportamiento del backend. |
| Reglas de valores | `S09_A1/codigo/backend/tests/test_value_rules.py` | Validación de tipos y reglas de los campos. |
| Resultado de pytest | `S09_A1/evidencias/despues/pytest.txt` | `84 passed, 1 warning`. |
| Ejecución registrada | `S09_A1/evidencias/despues/pruebas_ejecucion.json` | Código de salida 0 y duración registrada. |
| Cobertura de operaciones | `S09_A1/evidencias/despues/cobertura_operaciones.json` | Operaciones ejecutadas, método, ruta, código HTTP y validación de esquema. |
| Reproducción | `S09_A1/REPRODUCCION.md` | Entorno y pasos para repetir las pruebas y auditoría. |

## Brechas y siguientes pasos

1. Incorporar una interfaz web que consuma la API, especialmente para la exploración visual y los filtros del mapa.
2. Añadir pruebas de aceptación de interfaz cuando exista frontend.
3. Mantener esta matriz sincronizada con cambios en SRS, backlog, contrato y pruebas.
4. No presentar “completo en backend” como sinónimo de “producto web completo”.
