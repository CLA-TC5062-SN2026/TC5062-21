# Decisión de stack de frontend del Equipo 21

Fecha: 3 de noviembre de 2026.

Estado: stack aprobado por Jean Paul el 3 de noviembre de 2026 al aprobar el plan de trabajo. Jean Paul realizará el desarrollo de esta semana. No se atribuyen propuestas ni aprobación a otros integrantes.

## Stack elegido

| Responsabilidad | Opción | Motivo para este proyecto |
| --- | --- | --- |
| Interfaz | React con TypeScript | Componentes reutilizables para formularios, tarjetas y navegación. Los tipos permiten describir las respuestas del contrato y detectar usos incorrectos durante el desarrollo. |
| Construcción y desarrollo | Vite | Dispone de plantilla React con TypeScript y separa el frontend del backend FastAPI existente. |
| Estilos | CSS Modules y variables CSS compartidas | Permite controlar contraste, foco y adaptación a pantallas sin incorporar un framework de estilos para cuatro componentes base. |
| Estado | Estado local y Context para autenticación | El alcance requiere compartir identidad y sesión entre navegación y rutas; no se identifica aún una necesidad de un almacén global adicional. |
| Navegación | React Router | Organiza login, dashboard y vista de elementos, con protección de acceso. |
| HTTP | Fetch mediante un cliente común y servicios por recurso | Centraliza la URL base, JWT y errores sin repetir llamadas en las vistas. |

## Alternativas consideradas en esta propuesta

Estas comparaciones son del análisis inicial; no representan intervenciones de otros integrantes.

- **Vue con Vite:** alternativa viable para el mismo alcance. React mantiene continuidad con la propuesta arquitectónica anterior del proyecto. No se atribuye aquí mayor experiencia del equipo a ninguna de las opciones.
- **JavaScript sin framework:** permite resolver pantallas pequeñas, pero exige organizar manualmente la actualización de la interfaz, composición y estado de autenticación que necesitamos reutilizar.
- **Next.js:** incorpora capacidades de servidor que no se requieren para las dos actividades actuales, cuyo backend ya existe separado en FastAPI.
- **Tailwind o Bootstrap:** alternativas de estilos válidas. Para estos cuatro componentes se propone CSS propio para hacer explícitas las decisiones de diseño, estados y correcciones de accesibilidad.
- **Redux o Zustand:** no se justifican aún para compartir únicamente la sesión y mantener formularios y resultados en sus vistas. Revisar esta decisión si crece el estado compartido.
- **Axios:** facilita interceptores. Un cliente común basado en Fetch puede cubrir el requisito equivalente de JWT y errores del alcance actual.

## Integración prevista con el proyecto

La referencia HTTP es `S05_S06_A1/openapi_equipo.yaml` versión 2.0.0, recuperada de la rama de semana 6. Login utiliza `POST /api/auth/login` con `correo` y `contrasena`; devuelve `accessToken`. La identidad se consulta mediante `GET /api/auth/me`.

Se propone separar `components`, `pages`, `services` y el contexto de autenticación. La URL base será configurable mediante `VITE_API_URL`. En desarrollo, un proxy de `/api` hacia el backend permitirá mantener las llamadas del navegador bajo el mismo origen.

La decisión concreta sobre conservación y caducidad del token se documentará en `capa_servicios.md` al implementar autenticación. El frontend deberá reaccionar a respuestas 401 y mostrar errores útiles.

## Primer recorrido propuesto

Login → dashboard protegido → listado de elementos de arquitectura empresarial. El listado deberá utilizar datos persistidos en el backend e incluir carga, resultados, vacío y error. Si el entorno inicial carece de elementos, se prepararán datos ficticios de demostración mediante los mecanismos existentes del backend.

## Alcance de la decisión

La aprobación de Jean Paul cubre las dos actividades de esta semana. El entorno del backend ya se ejecutó con Python 3.12.16 y PostgreSQL 17.11 con ICU; sus 50 pruebas existentes pasaron. Los resultados del frontend se documentan por separado.

## Referencias

- [React: construir una aplicación desde cero](https://react.dev/learn/build-a-react-app-from-scratch).
- [Vite: inicio y plantillas disponibles](https://vite.dev/guide/).
- Contrato y arquitectura del proyecto recuperados en el repositorio, desde el commit `348c032729add9591cc481d427c9d5d0fff5625e`.
