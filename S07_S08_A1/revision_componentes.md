# Revisión de componentes frontend

Equipo 21 · TC5062 · 3 de noviembre de 2026.

Jean Paul realiza esta semana el trabajo individualmente con asistencia de IA. Este registro describe cambios aplicados durante la construcción; no atribuye revisiones a otros integrantes ni presenta todo el código generado como autoría manual.

## Revisión del scaffolding

La plantilla React/TypeScript de Vite aportó entrada, configuración y dependencias iniciales. Se retiraron logotipos, contador y estilos de ejemplo. Se organizaron componentes, vistas, servicios y autenticación por responsabilidad. La galería `/componentes` permite revisar los cuatro componentes; las pantallas de negocio reutilizan los mismos controles.

| Componente | Configuración y uso real | Cambios aplicados tras la revisión |
| --- | --- | --- |
| `Button.tsx` | `variant`, `loading`, `disabled`, `type` y atributos HTML. Login, búsqueda y reintento. | Tipo button por defecto para evitar envíos accidentales. Carga bloquea acciones duplicadas, conserva el nombre y expone aria-busy. Icono decorativo. |
| `Input.tsx` | `label`, `hint`, `error` y atributos nativos. Correo, contraseña y búsqueda. | Etiqueta visible asociada al campo. useId evita identificadores duplicados; ayuda/error con aria-describedby y aria-invalid. El error incluye texto y color. |
| `Card.tsx` | Título opcional, acción, contenido y atributos de sección. Galería, indicadores e inventario. | Sección vinculada semánticamente a su encabezado. Contenido configurable; no se convierte la tarjeta en botón sin una acción definida. |
| `Navbar.tsx` | Contexto de autenticación, ruta activa y menú móvil. | Estados público/autenticado, nombre para botones de icono, aria-expanded y aria-controls. Escape cierra y devuelve el foco al disparador. |

## Correcciones durante la integración

1. **Contraste:** se oscurecieron bordes de campos y ayuda. Los valores antes/después están en `accesibilidad.md` y en el reporte reproducible.
2. **Foco:** se añadió enlace para saltar al contenido, título por ruta y foco al contenido principal. Un error de login enfoca el campo inválido o el aviso del servidor.
3. **Móvil:** tarjetas en una columna, filtros apilados y menú desplegable. La tabla se desplaza dentro de su contenedor sin ampliar la página a 390 × 844.
4. **Filtros e historial:** el formulario se sincroniza con la URL al volver/avanzar para conservar coherencia con los resultados.
5. **Sesión y red:** un fallo temporal al recuperar el perfil conserva el token y ofrece reintentar. Un 401 sí elimina la sesión local.
6. **Solicitudes antiguas:** un 401 de una sesión anterior no borra una sesión nueva. Las cargas se cancelan al desmontar o cambiar la solicitud.

## Comprobación y límites

Se ejecutaron 14 pruebas de frontend, revisión estática y construcción de producción. La revisión estática termina sin errores y conserva cinco advertencias sobre Fast Refresh y actualizaciones de estado en efectos; reporte en A2/evidencias/frontend_lint.txt. En Chrome se recorrieron validación vacía, rechazo de credenciales, login correcto, panel, listado, vacío, detalle, error con el servicio detenido y recuperación. También se revisaron foco y menú móvil con Escape. Capturas en `evidencias/` y A2.

La evaluación es acotada; no acredita conformidad WCAG completa ni sustituye pruebas con usuarios. El alcance de A2 se concentra en autenticación y consulta de elementos, sin implementar toda la administración de la plataforma.
