# Guion de demo — máximo 5 minutos, sin cortes

**Equipo 21 · S11-A1.** Meta: terminar en **4:45**, dejando 15 segundos de margen. Un integrante maneja el teclado y los demás narran por turnos. Asignen nombres reales antes del ensayo; este documento no atribuye intervenciones que aún no se han grabado.

## Preparación

1. Seguir el README para levantar PostgreSQL, backend y frontend. Ejecutar `prepare_frontend_demo.py` antes de grabar.
2. Tener la cuenta ficticia Administrador disponible en un gestor local; no mostrar `.env`, credenciales ni tokens en el video. Cerrar notificaciones y pestañas personales.
3. Abrir `/login`, el README en el diagrama Mermaid y este guion. Mantener la aplicación como pantalla principal.
4. Ensayar con el tipo **Proyecto de mejora**. Para la toma definitiva usar un nombre distinto al del ensayo, por ejemplo **Portal de seguimiento de solicitudes — presentación**.
5. Comprobar que hay datos en el inventario y que el registro del ensayo no confunde la búsqueda. No borrar registros históricos para limpiar la toma.
6. Hacer una grabación corta de audio y escucharla. Verificar también el indicador de micrófono y que la herramienta elegida grabe pantalla y audio juntos.

## Recorrido continuo de 4:45

| Tiempo | Segmento y narrador por asignar | Acción en pantalla y mensaje sugerido |
|---|---|---|
| 0:00–0:25 | Problema y contexto — integrante 1 | Mostrar el acceso: “Cuando objetivos, proyectos y aplicaciones se mantienen en archivos separados, es difícil saber cuál información sigue vigente. Nuestra plataforma ofrece al responsable de arquitectura un inventario común con permisos e historial.” |
| 0:25–0:45 | Demo: login — teclado + integrante 2 | Iniciar sesión con Administrador. Mostrar el panel y el inventario con registros completos. Aclarar que es una organización ficticia y que los datos están persistidos en PostgreSQL. |
| 0:45–1:30 | Demo: crear — integrante 2 | Pulsar **Nuevo elemento**, elegir **Proyecto de mejora** y capturar los valores de la tabla inferior. Guardar y mostrar el identificador asignado. Explicar qué iniciativa se está registrando y para qué área. |
| 1:30–2:00 | Demo: leer — integrante 2 | Volver al inventario, buscar el nombre y abrir su detalle. Mostrar descripción, presupuesto, fecha y etapa. El mismo registro se obtiene desde la API, no de una lista simulada del navegador. |
| 2:00–2:30 | Demo: actualizar y manejar error — integrante 3 | Pulsar **Editar elemento**. Vaciar Nombre e intentar guardar: señalar el error y que no se aplicaron cambios. Restaurar Nombre, cambiar presupuesto a 73000 y Etapa a En curso. Guardar y señalar que el ID se conserva. |
| 2:30–3:15 | Demo: baja y recuperación — integrante 3 | Dar de baja y confirmar. Volver al inventario, buscar el nombre y mostrar que ya no aparece entre activos. Activar **Incluir dados de baja**, abrirlo y reactivarlo. Explicar que se retira sin perder información ni historial. |
| 3:15–3:45 | Decisión técnica clave — integrante 1 | Mostrar brevemente el diagrama del README: “Separamos React, API y base de datos. Las reglas y permisos se validan en el servidor, aunque alguien intente saltarse la interfaz. El proxy de `/api` mantiene un mismo origen en el entorno local.” |
| 3:45–4:15 | Uso del agente de IA — integrante 2 | “Nos ayudó a organizar requisitos, redactar el contrato y revisar pruebas. También generó trabajo extra: la documentación inicial omitió el frontend de otra rama y describió métodos HTTP incorrectos. Fue necesario contrastar sus propuestas con el código y el sistema ejecutándose.” Adaptar la frase a lo que el equipo pueda respaldar. |
| 4:15–4:45 | Qué haríamos diferente — integrante 3 | Volver al inventario: “Priorizaríamos incrementos completos y la integración frecuente. Hoy el CRUD funciona, pero la administración y los mapas todavía no tienen pantallas completas. El siguiente incremento sería la exploración visual de relaciones y su validación con el stakeholder.” |

Los cinco segmentos están cubiertos sin sumar seis minutos: la demo ocupa 2:50 y el total 4:45.

### Datos para capturar durante la toma

| Campo | Valor ficticio sugerido |
|---|---|
| Tipo | Proyecto de mejora |
| Nombre | Portal de seguimiento de solicitudes — presentación |
| Descripción | Permitir a los clientes consultar el estado de sus solicitudes desde el portal de servicios. |
| Presupuesto | 65000; después cambiar a 73000 |
| Fecha objetivo | 2026-12-18 |
| Etapa | Planeado; después cambiar a En curso |

“Datos reales” se interpreta como registros completos que el sistema guarda y recupera, en lugar de una pantalla vacía o un mock. La consigna del SRS exige **datos ficticios**; no se necesita información confidencial de una empresa. Explicar esa distinción en la grabación.

## Revisión y entrega

- Confirmar una sola toma continua, narración inteligible, participación del equipo y duración **≤300 segundos**.
- No afirmar que existe un mapa visual, un despliegue público o una funcionalidad que no se haya mostrado/verificado.
- Guardar como `S11_A1/demo_proyecto.mp4`. Si supera 100 MB, subirlo al almacenamiento elegido y poner su URL real en `S11_A1/demo_link.txt`; verificar que el docente pueda abrirlo sin pedir acceso.
- Ejecutar `python3 scripts/empaquetar_s11.py --final`. Para MP4 local se necesita `ffprobe` en PATH para validar duración y pistas de audio/video.
- Subir el ZIP final a Canvas y los documentos y video/enlace al repo del equipo 24 horas antes de la presentación.

**Pendiente humano:** grabar el video, comprobar el micrófono, revisar la narración y efectuar la entrega en Canvas. Este guion y las capturas no sustituyen el video.
