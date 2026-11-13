# Semana 9 · Auditoría de calidad de código

Equipo 21 · TC5062 · Jean Paul Lozano Gámiz · 13 de noviembre de 2026.

La auditoría parte del backend de Semana 8. Se priorizó el rendimiento al crecer los datos, de acuerdo con el criterio expresado por Jean Paul.

## Archivos solicitados

| Archivo | Contenido |
| --- | --- |
| `output_linter.txt` | Salida íntegra inicial de Pylint |
| `clasificacion_problemas.md` | Clasificación y explicación de todos los tipos de mensajes |
| `code_review.md` | Siete hallazgos concretos, correcciones y tabla de los cinco principios SOLID |
| `refactorizacion.md` | Tres mejoras implementadas, código antes/después y resultados |
| `deuda_tecnica.md` | Reflexión, mediciones, deuda intencional/no documentada y propuestas para SCRUM |

## Resultado observado

Las 50 pruebas originales pasan antes y después. La suite final tiene **84 casos aprobados**, con 34 casos nuevos. El recorrido original valida las 46 operaciones del contrato. Pylint pasa de 518 a 492 mensajes; persisten observaciones documentadas.

| Caso medido | SELECT antes | SELECT después |
| --- | ---: | ---: |
| Página de 25 resultados entre 300 elementos | 602 | 53 |
| Guardar ocho campos numéricos | 10 | 2 |
| Modificar nombre en un elemento de nueve campos | 57 | 30 |

Son consultas de aplicación en escenarios controlados, no tiempos de respuesta ni una prueba de carga concurrente. La evidencia completa declara condiciones y límites.

## Material de apoyo incluido

- `evidencias/antes/`: salida original, JSON, clasificación por ocurrencia, pruebas, medición y copia de los archivos iniciales.
- `evidencias/despues/`: resultados finales, métricas, pruebas y copia de los archivos auditados.
- `evidencias/cambios.patch`: cambios de código, configuración y pruebas frente al commit base.
- `evidencias/trazabilidad.json`: procedencia y comprobaciones del paquete.
- `codigo/`: backend refactorizado y recursos necesarios para ejecutar las pruebas en una extracción independiente.
- `REPRODUCCION.md`: instrucciones de ejecución.
- `MANIFIESTO_SHA256.txt`: hashes de los archivos entregados, salvo el propio manifiesto.

La copia completa del repositorio de trabajo está fuera del ZIP, en `Semana 9/TC5062-21`, rama local `codex/s09-auditoria-calidad`. El directorio `codigo/` del paquete contiene el alcance necesario para esta auditoría, no el frontend ni los videos de semanas anteriores.

## Revisión antes de presentar

Los documentos fueron preparados con asistencia de Codex. La prioridad de rendimiento sí fue indicada por Jean Paul; no se inventaron sesiones de equipo ni una revisión independiente. La rúbrica solicita explicaciones propias: leer los hallazgos y ajustar la reflexión para confirmar que representan el criterio del estudiante.

El archivo para subir manualmente a Canvas es **`S09_A1.zip`**, que contiene una carpeta raíz `S09_A1/`. Esta entrega local no implica que se haya enviado a Canvas ni publicado en GitHub.
