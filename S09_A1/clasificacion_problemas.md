# Clasificación de problemas del análisis estático

Equipo 21 · TC5062 · Semana 9 · 13 de noviembre de 2026

Preparado para Jean Paul Lozano Gámiz con asistencia de Codex. Prioridad indicada por el estudiante: mejorar el rendimiento al crecer los datos.

## Alcance y reproducción

Se utilizó **Pylint 4.1.3, Astroid 4.3.4 y Python 3.12.16**. El alcance inicial son los ocho archivos Python de `backend/app/`: 1,168 líneas físicas, incluidos comentarios y líneas vacías. Después de refactorizar son diez archivos y 1,278 líneas. Se revisó el código de producto; scripts auxiliares, pruebas, frontend, archivos generados y dependencias quedan fuera de esta ejecución estática. Las pruebas del backend se ejecutaron por separado.

La base local es el commit `092d11a7008468447304d00c42ede102305ce5ee`. La rama publicada de Semana 8 apunta a `4f2f30130de7af3344bf4736601478221f300088`; ambas bases tienen el árbol `edbc1987679cd9354918fa12b9bb6669736fc0c0`. Los originales examinados, sus líneas y hashes están en `evidencias/antes/`. No se mezclaron cambios con la carpeta de Semana 8.

Desde la raíz de la copia de código:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r backend/requirements-quality.lock.txt
.venv/bin/python backend/scripts/auditar_calidad.py --output S09_A1/evidencias/reproduccion
```

La configuración `backend/pylintrc` fija 100 caracteres por línea, muestra los informes y desactiva la caché persistente. **No añade supresiones de mensajes ni cambia los umbrales de complejidad predeterminados.** El comando y las versiones exactas se registran en cada `ejecucion.json`. `output_linter.txt` es una copia íntegra de la salida inicial; la salida final está en `evidencias/despues/output_linter.txt`. Se conserva también JSON para comprobar los conteos. Pylint admite salidas de texto y JSON en la misma ejecución. [Documentación oficial de salida](https://pylint.pycqa.org/en/stable/user_guide/usage/output.html).

## Criterio de clasificación

- **Crítico:** defecto confirmado que comprometa datos, acceso o funcionamiento. La letra del mensaje del linter por sí sola no demuestra ese impacto.
- **Importante:** complejidad, acoplamiento, diagnóstico insuficiente o trabajo innecesario que encarece cambios o crecimiento.
- **Menor:** legibilidad, documentación y convenciones. Incluye advertencias justificadas que no requieren modificar el diseño.

Cada ocurrencia está clasificada en `evidencias/antes/clasificacion_detallada.csv` y en su equivalente final. La tabla siguiente agrupa por regla; su columna de ubicación muestra un ejemplo, no todas las ocurrencias. Los criterios completos quedan en `evidencias/criterios_clasificacion.json`.

| Prioridad de revisión | Inicial | Final |
| --- | ---: | ---: |
| Crítico confirmado por este análisis | 0 | 0 |
| Importante | 9 | 8 |
| Menor o advertencia justificada | 509 | 484 |
| Total de mensajes | **518** | **492** |

La salida inicial contiene 393 mensajes de convención, 95 advertencias y 30 sugerencias de refactorización; la final contiene 369, 93 y 30, respectivamente. Ambas tienen cero mensajes E/F. El código de salida es **28**, por las categorías C/W/R presentes; no significa que el análisis no se ejecutó ni que el proyecto quedó sin pendientes.

## Inventario y justificación

| Regla | Inicial | Final | Prioridad | Primer ejemplo inicial | Justificación |
| --- | ---: | ---: | --- | --- | --- |
| C0114 / missing-module-docstring | 2 | 1 | Menor | backend/app/config.py:1 | Falta documentar el propósito de un módulo; no demuestra defecto funcional. |
| C0115 / missing-class-docstring | 21 | 21 | Menor | backend/app/config.py:12 | Documentación de clase ausente; revisar prioridad según complejidad. |
| C0116 / missing-function-docstring | 93 | 90 | Menor | backend/app/config.py:21 | Contrato de una función sin documentar; no equivale a fallo de ejecución. |
| C0301 / line-too-long | 142 | 135 | Menor | backend/app/contract.py:44 | Legibilidad; longitud mayor a 100 caracteres. |
| C0321 / multiple-statements | 89 | 76 | Menor | backend/app/contract.py:23 | Varias instrucciones por línea dificultan revisión y depuración. |
| W0707 / raise-missing-from | 2 | 2 | Menor | backend/app/contract.py:70 | Encadenamiento de errores por aclarar, manteniendo mensajes HTTP sin datos sensibles. |
| R0912 / too-many-branches | 2 | 1 | Importante | backend/app/contract.py:52 | Complejidad de flujo: requiere muchas rutas de prueba y dificulta cambios. |
| W0621 / redefined-outer-name | 4 | 4 | Menor | backend/app/main.py:41 | Sombreado de nombres: aquí no se confirmó cambio de comportamiento. |
| W0718 / broad-exception-caught | 1 | 1 | Importante | backend/app/main.py:75 | Contención HTTP válida, pero falta diagnóstico seguro del tipo de error (H06). |
| R0911 / too-many-return-statements | 1 | 1 | Importante | backend/app/main.py:40 | Middleware con varios motivos de salida y responsabilidades; separar después de caracterizar comportamiento. |
| W0613 / unused-argument | 86 | 85 | Menor | backend/app/main.py:82 | Principalmente firma uniforme p/q/b del despacho. El parámetro creating sí era redundante y se retiró. |
| W0611 / unused-import | 2 | 1 | Menor | backend/app/main.py:15 | Importación sin uso; limpieza sin impacto de negocio. |
| R0903 / too-few-public-methods | 18 | 20 | Menor | backend/app/models.py:19 | Heurística no accionable por sí sola en modelos ORM, configuración y protocolos de datos. |
| R0901 / too-many-ancestors | 2 | 2 | Menor | backend/app/models.py:115 | Herencia técnica de SQLAlchemy y mixins; no se observó ruptura de sustitución. |
| R1710 / inconsistent-return-statements | 1 | 0 | Menor | backend/app/security.py:18 | El camino alterno llama invalid, que siempre lanza APIError; se aclara con NoReturn, no era un retorno None real. |
| C0415 / import-outside-toplevel | 1 | 1 | Menor | backend/app/security.py:69 | Importación de UUID dentro de authenticate; oportunidad de organización. |
| R0916 / too-many-boolean-expressions | 1 | 1 | Importante | backend/app/security.py:76 | Nueve condiciones de sesión en un guard; conservar todas al extraer predicados comprobables. |
| C0103 / invalid-name | 45 | 45 | Menor | backend/app/services.py:145 | Nombres camelCase de operationId conservados por compatibilidad. No renombrar sin adaptar dispatch. |
| R0913 / too-many-arguments | 1 | 1 | Importante | backend/app/services.py:456 | validate_endpoints mezcla varios datos y opciones; considerar objeto de parámetros. |
| R0917 / too-many-positional-arguments | 1 | 1 | Importante | backend/app/services.py:456 | La misma firma compleja; no es un defecto adicional independiente. |
| R1735 / use-dict-literal | 1 | 1 | Menor | backend/app/services.py:486 | Preferencia sintáctica por literal de diccionario. |
| R0914 / too-many-locals | 1 | 1 | Importante | backend/app/services.py:601 | La carga de muestra combina preparación de catálogos, elementos y relaciones. |
| R0904 / too-many-public-methods | 1 | 1 | Importante | backend/app/services.py:26 | Service concentra dominios y persistencia (H04). |

## Interpretación de los resultados

La calificación de Pylint pasó de **4.60 a 5.13 sobre 10**. Es un indicador de esta configuración, no una calificación de seguridad ni una medición completa de calidad. Se eliminaron 26 mensajes netos (5.02%); el código creció por la separación de responsabilidades. La densidad pasó de 443.49 a 384.98 mensajes por cada mil líneas físicas. Se cuenta cada aviso, incluidos avisos sobre el mismo problema; no se usa esta cifra como densidad de defectos únicos.

La reducción de complejidad más concreta está en `write_values`: desaparece R0912, que señalaba 18 ramas frente al umbral de 12. R0904 permanece: `Service` tiene 74 métodos públicos antes y después, aunque se extrajo parte de la validación. Los dos avisos nuevos R0903 corresponden a protocolos de datos sin métodos; añadir métodos artificiales para silenciarlos empeoraría su propósito.

R1710 en `correo_normalizado` no probaba un retorno incorrecto: `invalid` siempre lanza una excepción. Declarar ese contrato con `NoReturn` permite al analizador comprenderlo. Los nombres camelCase se conservan donde corresponden a `operationId`; cambiarlos sin adaptar el despacho rompería la integración.

## Revisión manual que complementa al linter

Los problemas de paginación, consultas por campo y serialización repetida **no aparecieron como alertas específicas de Pylint**. Se confirmaron leyendo el flujo y contando consultas. Se registran como H01, H02 y H03 en `code_review.md`, sin sumarlos a los 518 mensajes. El linter sí aporta evidencia estructural para H02, H04 y H06.

No se confirmó una vulnerabilidad crítica en el alcance revisado. Las consultas del servicio usan expresiones parametrizadas de SQLAlchemy; la sentencia SQL de bloqueo del middleware es constante. La revisión y las pruebas observan validación de entradas, permisos, revocación de sesiones y ocultación de contraseñas. Esto no sustituye una evaluación completa de seguridad ni una prueba de carga.
