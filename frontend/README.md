# Frontend — Arquitectura Empresarial, Equipo 21

React, Vite y TypeScript. Actividades S07–S08 A1 y A2. Las pantallas de negocio consumen la API FastAPI existente y PostgreSQL; sus resultados no son arreglos simulados en el navegador.

## Arranque

Verificado con Node 24.17.0 y npm 11.13.0. Desde esta carpeta:

```sh
npm ci
cp .env.example .env
npm run dev
```

Abrir `http://127.0.0.1:5173/componentes` para la galería pública y `/login` para acceder. Preparar el backend en el puerto 8000 siguiendo `../backend/README.md`. Vite reenvía `/api` a `API_PROXY_TARGET` manteniendo el mismo origen del navegador. Si 5173 está ocupado, detener el servidor anterior o ejecutar `npm run dev -- --port 5174`.

`VITE_API_URL` es pública y nunca debe contener secretos. El ejemplo usa `/api`. `API_PROXY_TARGET` solo configura el proxy de desarrollo. En producción se necesita un proxy del servidor para `/api` o un origen permitido explícitamente en el backend.

Las cuentas ficticias se generan en `../.local/demo_credentials.json` mediante `setup_local.py`; no se incluyen en Git ni en los ZIP. Con la API activa, ejecutar desde la raíz `.venv/bin/python backend/scripts/prepare_frontend_demo.py` para preparar cinco elementos ficticios persistidos. Una cuenta Consulta puede recorrer las pantallas implementadas.

## Rutas y estructura

| Ruta | Uso | Acceso |
| --- | --- | --- |
| `/login` | Formulario y autenticación real | Público |
| `/componentes` | Galería de los cuatro componentes | Público |
| `/panel` | Cantidades y primeros elementos del API | Protegido |
| `/elementos` | Búsqueda, filtros y paginación | Protegido |
| `/elementos/:id` | Campos y metadatos del elemento | Protegido |

- `src/components/`: Button, Input, Card, Navbar y estados compartidos.
- `src/pages/`: vistas y estilos.
- `src/services/`: cliente Fetch, sesión, tipos y servicios por recurso.
- `src/context/`: identidad y ciclo de sesión.
- `src/hooks/`: carga cancelable y reintento.
- `src/main.tsx` y `src/App.tsx`: entrada, proveedor, rutas y foco.

## Verificación

```sh
npm test
npm run lint
npm run build
```

Las 14 pruebas cubren HTTP, errores, sesión y componentes. La revisión de navegador está en `../S07_S08_A1/accesibilidad.md` y `../S07_S08_A2/capa_servicios.md`. `../scripts/verificar_contraste.py` reproduce las mediciones.

La galería identifica su carga de ejemplo como simulada. Los indicadores del inventario y login corresponden a solicitudes reales.
