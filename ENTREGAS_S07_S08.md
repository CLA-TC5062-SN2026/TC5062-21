# Entregas S07–S08 — Equipo 21

Jean Paul Lozano Gámiz · TC5062 · 3 de noviembre de 2026.

Frontend e integración construidos sobre `codex/s05-s06-crud-autenticacion`, commit `348c032729add9591cc481d427c9d5d0fff5625e`. Rama de este trabajo: `codex/s07-s08-frontend-integracion`. El código y contrato previos se conservan; se agrega frontend, documentación y evidencia de las dos actividades.

## Archivos para Canvas

| Actividad | ZIP | Contenido principal |
| --- | --- | --- |
| Generación de componentes frontend | S07_S08_A1.zip | Stack aprobado, revisión de componentes, accesibilidad, código frontend y scaffolding.mp4 |
| Integración frontend–backend | S07_S08_A2.zip | Capa de servicios, frontend, backend de referencia, SQL/contrato, evidencias y los dos videos |

Generar desde la raíz con `python3 scripts/empaquetar_s08.py`. Los archivos se escriben en `entregas/`; el script verifica duración máxima 20/30/30 segundos, integridad ZIP y exclusión de archivos privados. Incluye código reproducible y dependencias declaradas, no dependencias instaladas. Los ZIP requieren revisión y subida del estudiante a la actividad correspondiente en Canvas.

Consignas: [A1](https://experiencia21.tec.mx/courses/708363/assignments/23606103?module_item_id=44839054) y [A2](https://experiencia21.tec.mx/courses/708363/assignments/23606106?module_item_id=44839055). Fecha visible de entrega: 8 de noviembre de 2026, 23:59. Este documento no acredita una entrega a Canvas.

## Ejecución y recorrido

1. Preparar y arrancar la API según `backend/README.md`.
2. Preparar datos mediante `backend/scripts/prepare_frontend_demo.py`.
3. En frontend, ejecutar `npm ci`, copiar .env.example a .env y `npm run dev`.
4. Revisar /componentes; acceder con una cuenta ficticia local en /login y recorrer /panel → /elementos → detalle.

Las cuentas se generan en .local/demo_credentials.json; no se comparten secretos por Git/ZIP. El backend conserva autorización y reglas de negocio. Los datos visibles de demostración son ficticios y persistidos.

## Verificación

- Backend: **50 pruebas aprobadas** contra PostgreSQL real de pruebas.
- Frontend: **14 pruebas aprobadas**; construcción de producción correcta.
- Postman: **6 solicitudes, 22 aserciones, 0 fallos** contra API local.
- Contraste: ocho pares revisados superan sus umbrales.
- Revisión estática: sin errores; cinco advertencias de organización para Fast Refresh y actualizaciones de estado en efectos. No impiden la construcción; se conservan en frontend_lint.txt.
- Navegador: login correcto/rechazado, rutas protegidas, listado/detalle, vacío, error y recuperación; móvil 390 × 844 y foco de menú.

Los reportes se conservan en S07_S08_A2/evidencias y S07_S08_A1/evidencias. La evaluación de accesibilidad es básica, sin declaración de conformidad completa.

Los videos se grabaron en [Google Vids](https://docs.google.com/videos/d/1kWCPZAMd6jfKKABcZQJSEFGtHJjsycs3KbGNl8R2ElM/edit). Se extrajeron tramos a velocidad normal y se retiró el audio. Scaffolding muestra comando y aplicación; autenticación muestra credenciales enmascaradas, acceso y panel protegido; E2E muestra solicitud, indicador de carga, listado, búsqueda y detalle. videos.json registra su procedencia.

Jean Paul realiza el trabajo de esta semana con asistencia de IA. No se atribuyen decisiones o participación inexistentes al resto del equipo.
