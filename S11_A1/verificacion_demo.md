# Verificación de demo y estado de entrega

**Fecha:** 25 de noviembre de 2026, zona America/Mexico_City.
**Entorno comprobado:** macOS ARM64, Python 3.12.14, PostgreSQL 17.11, Node 24.21.0, navegador integrado de Codex. Frontend en `127.0.0.1:5173`, API en `127.0.0.1:8000` y PostgreSQL temporal en `127.0.0.1:55432`. Vista de escritorio de 1280 × 900 px para el ensayo. No equivale a verificar las dos últimas versiones de Chrome y Edge.

## Resultados automatizados

| Verificación | Resultado | Evidencia |
|---|---|---|
| Backend, suite histórica de S09 y aceptación S11 | **88 passed, 1 warning**, salida 0 | [Resumen](evidencias/backend_pytest.txt), [JUnit](evidencias/backend_pytest.xml) |
| Frontend | **19 passed**, salida 0 | [Vitest](evidencias/frontend_tests.txt) |
| Compilación frontend | Correcta, salida 0 | [Build](evidencias/frontend_build.txt) |
| Lint frontend | Sin errores; cinco advertencias existentes | [Lint](evidencias/frontend_lint.txt) |
| OpenAPI y colecciones CRUD/autenticación | Lint sin errores | [Resumen de lint](evidencias/contrato_lint.json); la verificación no modificó la interfaz |
| Postman, autenticación y roles contra API local | **6 requests / 22 assertions / 0 failed**, salida 0 | [Salida completa](evidencias/postman_auth.txt) |

La advertencia pytest corresponde a la deprecación Starlette/httpx. Las advertencias frontend se refieren a Fast Refresh y actualizaciones de estado en efectos. El recorrido de 46 operaciones comprueba contrato e integración; no acredita por sí solo los 56 criterios del SRS.

## Casos manuales ejecutados en S11

| ID | Procedimiento y resultado observado | Evidencia |
|---|---|---|
| **M-01** | Contraseña incorrecta: aparece un mensaje de error y no se ingresa. Con credenciales correctas se abre el panel. | [Login](capturas/01_login.png), [error](capturas/02_error_login.png), [panel](capturas/03_panel.png) |
| **M-02** | Seleccionar Proyecto de mejora; intentar guardar sin obligatorios: se señalan campos sin crear un elemento. Completar texto, número, fecha y selección: se crea el registro. | [Validación](capturas/05_validacion.png), [formulario](capturas/06_formulario.png) |
| **M-03** | Abrir el registro creado y modificar presupuesto y etapa. Se conservan ID y demás valores; fecha `2026-12-18` recuperada tras guardar. | [Detalle](capturas/07_detalle.png) |
| **M-04** | Buscar el nombre del registro: se obtiene su resultado. Buscar sin nombre ni filtros muestra una indicación sin cambiar el listado. La tabla distingue ID, tipo y capa; una búsqueda del registro dado de baja obtiene cero resultados en la vista ordinaria. | [Inventario](capturas/04_inventario.png); M-05/M-06 |
| **M-05** | Confirmar baja lógica: cambia a Baja, conserva campos y desaparece de la búsqueda ordinaria. | [Baja](capturas/08_baja.png) |
| **M-06** | Activar Incluir dados de baja, recuperar el mismo registro y reactivarlo. Regresa a Activo con el mismo ID y valores. | [Consulta histórica](capturas/09_historico.png) |
| **M-07** | Cerrar sesión, acceder después con una sesión nueva y abrir el mismo registro. Se recuperan descripción, presupuesto 73000, etapa En curso, fecha e identificador. | Comprobación visual del detalle; almacenamiento PostgreSQL; captura de referencia del mismo objeto |
| **M-08** | Acceder con Consulta: no aparece Nuevo elemento. Navegar directamente a `/elementos/nuevo` muestra la falta de permisos. La API conserva sus controles de servidor, comprobados también con pytest/Postman. | [Vista de Consulta](capturas/10_consulta.png), pruebas de permisos |
| **M-09** | Ejecutar la carga idempotente y repetirla. Se conserva el conjunto previamente cargado y no se duplican los registros de la muestra. | Script de preparación; prueba backend de carga repetida; [repetición local](evidencias/carga_repetida.json) |

Durante el ensayo el frontend consumió el backend por el proxy `/api`. Las operaciones de login, lectura y escritura terminaron sin bloqueo por CORS. La consulta de errores de consola al finalizar el CRUD devolvió una lista vacía; no es una auditoría de todas las pantallas o todos los navegadores.

Se corrigió un problema observado con el campo fecha antes de aceptar M-03. La captura `06_formulario.png` y el detalle muestran el valor posterior a la corrección. Los identificadores y autores de las capturas pertenecen a cuentas ficticias de esta instalación local.

## Pendientes y alcance de lo verificado

- [x] Backend y frontend integrados y comunicándose en local.
- [x] Cuenta ficticia y datos completos cargados.
- [x] Login, CRUD, error de validación, baja y reactivación comprobados.
- [x] Pruebas, compilación y reportes conservados.
- [x] Video del equipo recibido e incorporado con el nombre solicitado.
- [ ] Revisión manual de continuidad, participación del equipo y cobertura de los cinco segmentos.
- [ ] Prueba de micrófono y revisión de claridad de narración.
- [x] Añadir [`demo_proyecto.mp4`](demo_proyecto.mp4), con pistas de imagen y audio presentes.
- [x] Generar ZIP con documentación y video original.
- [ ] Subir el ZIP a Canvas.
- [ ] Alojamiento público y URL de producción; el equipo indicó que todavía no cuenta con hosting.

Se mantiene el alcance parcial del producto indicado en la [matriz](matriz_trazabilidad.md): faltan pantallas administrativas, propuestas/decisiones, bitácora y mapa interactivo. Docker/Nginx se proporcionan como alternativa preparada; no se ejecutaron sus contenedores en esta revisión. No se midió el escenario completo de carga, la conformidad de accesibilidad ni la compatibilidad en Chrome/Edge.

El ZIP `preparacion` permite revisar los documentos antes de grabar. El modo `--final` del empaquetador exige imagen, audio y duración máxima de 300 segundos. El script verifica presencia y metadatos, pero no puede certificar continuidad, calidad del audio, los cinco segmentos o la participación del equipo.

## Video recibido — 27 de noviembre de 2026

El equipo proporcionó el archivo que se incluye como [`demo_proyecto.mp4`](demo_proyecto.mp4). Se cambió únicamente su nombre: su contenido se conserva íntegro, como indicó el equipo.

- Tamaño: **22,170,821 bytes**, inferior a 100 MB; no se necesita `demo_link.txt`.
- Duración del contenedor MP4: **300.315011 segundos** (**5:00.315**), obtenida de la cabecera `moov/mvhd`. Supera el máximo por 0.315011 segundos; el equipo decidió conservarlo así.
- Pistas de imagen (`vide`) y audio (`soun`) presentes. La herramienta nativa `afinfo` reconoce audio AAC estéreo a 44.1 kHz.
- El ZIP con el original se generó por separado: el modo estricto `--final` rechaza esta duración. No se modificó ese control.

La comprobación de metadatos no certifica claridad de narración, continuidad, participación del equipo ni cobertura de los cinco segmentos. Tampoco acredita una entrega a Canvas.
