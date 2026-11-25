# Frontend — Arquitectura Empresarial, Equipo 21

React, Vite y TypeScript. Consume la API FastAPI y PostgreSQL del proyecto. El frontend de S07–S08 se integró con la refactorización backend de S09 y el CRUD de elementos añadido en S11.

## Arranque

Seguir primero el [README raíz](../README.md#instalación-y-ejecución-local) para generar configuración, preparar PostgreSQL y levantar la API en 8000. Desde esta carpeta:

```sh
npm ci
npm run dev
```

Abrir `http://127.0.0.1:5173/login`. El configurador de la raíz copia `.env.example` a `.env` si no existe. Las credenciales ficticias permanecen en `../.local/demo_credentials.json`; no están en Git.

Vite reenvía `/api` a `API_PROXY_TARGET` manteniendo un mismo origen para el navegador. `VITE_API_URL` es pública y debe ser `/api` en esta configuración. No debe contener secretos. El contenedor preparado utiliza Nginx para servir React y reenviar `/api`; no se ejecutó Docker en S11.

## Rutas y alcance

| Ruta | Función | Acceso |
|---|---|---|
| `/login` | Autenticación real y error de credenciales | Público |
| `/componentes` | Galería de componentes | Público |
| `/panel` | Cantidades e inventario inicial desde la API | Autenticado |
| `/elementos` | Búsqueda, filtros, ID, páginas e inclusión de bajas | Autenticado |
| `/elementos/nuevo` | Captura según campos de tipo | Administrador o Editor con capa asignada |
| `/elementos/:id` | Detalle, autoría, baja y reactivación | Lectura autenticada; escritura según capa |
| `/elementos/:id/editar` | Edición conservando el identificador | Administrador o Editor con la capa asignada |

Los formularios admiten texto, número, fecha y selección; identifican obligatorios y conservan la captura cuando el servidor rechaza una operación. El servidor comprueba permisos aunque alguien acceda directamente a una ruta o envíe una solicitud por fuera de la interfaz.

Todavía no hay pantallas completas para administrar cuentas y tipos, proponer/aprobar relaciones, consultar bitácora o explorar mapas. La galería tiene ejemplos identificados como simulados; las pantallas de inventario usan solicitudes reales.

## Verificación

```sh
npm test
npm run lint
npm run build
```

S11: 19 pruebas aprobadas, build correcto y cinco advertencias de lint existentes, sin errores. Ver [reportes](../S11_A1/evidencias/) y [ensayo de navegador](../S11_A1/verificacion_demo.md). Las comprobaciones no sustituyen la prueba de micrófono, narración o compatibilidad completa con Chrome y Edge.
