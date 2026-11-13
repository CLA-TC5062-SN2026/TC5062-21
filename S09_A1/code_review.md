# Revisión asistida de código y principios SOLID

Equipo 21 · TC5062 · Semana 9 · 13 de noviembre de 2026

Preparado para Jean Paul Lozano Gámiz con asistencia de Codex. Prioridad indicada por el estudiante: mejorar el rendimiento al crecer los datos.

## Archivo seleccionado y criterio

Se seleccionó **`backend/app/services.py`**, el archivo de producto más largo: 629 líneas iniciales y 74 métodos públicos según Pylint. Reúne autenticación, administración de usuarios, catálogos, elementos, relaciones, propuestas, bitácora y carga de demostración. Esta concentración permite revisar DRY, SRP, dependencias y costo de consultas en un mismo flujo.

Las ubicaciones **iniciales** se refieren a los archivos congelados en `evidencias/antes/codigo/`; las **finales**, a `codigo/backend/app/`. Los fragmentos marcados como implementados pertenecen a la entrega. Los marcados como propuesta quedan pendientes y no se presentan como código probado.

| Hallazgo | Prioridad | Resultado |
| --- | --- | --- |
| H01. Paginar después de materializar y serializar todo | Importante, rendimiento | Implementado R1 |
| H02. Consultar por cada campo y mezclar validación con escritura | Importante, rendimiento/SRP/DIP | Implementado R2 |
| H03. Reconstruir varias veces el mismo elemento para auditar y responder | Importante, rendimiento/DRY | Implementado R3 |
| H04. Servicio concentrador de dominios y SQL | Importante, mantenibilidad | Mitigación parcial; separación por dominios pendiente |
| H05. Duplicación de la proyección de una propuesta | Importante, DRY | Propuesta pendiente |
| H06. Contención de errores sin diagnóstico suficiente | Importante, operación | Propuesta pendiente |
| H07. Parámetros abreviados y firma poco expresiva | Menor, legibilidad | Propuesta pendiente |

## H01 · La página se recorta demasiado tarde

**Inicial:** `services.py:126` y `services.py:386`; también listados en 180, 496, 553 y 588. `listing` transforma todos los registros y después conserva 25. El total de trabajo crece con el conjunto completo aunque la respuesta tenga siempre el mismo tamaño. Cada resumen de elemento, además, consulta su tipo y capa.

**Explicación:** al crecer de 60 a 300 elementos, las consultas de una página pasaron de 122 a 602. Es trabajo verificable que el usuario no necesita para ver los primeros 25 resultados. La prioridad es mover el límite a la consulta y conservar filtros, orden y total.

**Corrección implementada:** `pagination.py:7` y `services.py:353`. Se aplica a usuarios, elementos, propuestas, relaciones y bitácora.

```python
"""Paginación SQL compartida: contar y cargar solo los registros solicitados."""
from sqlalchemy import func, select

PAGE_SIZE = 25


def paginate(db, statement, serializer, page=1):
    """Conserva filtros y orden del SELECT, y serializa como máximo una página."""
    total = db.scalar(select(func.count()).select_from(statement.order_by(None).subquery()))
    rows = db.scalars(statement.limit(PAGE_SIZE).offset((page - 1) * PAGE_SIZE))
    return {"items": [serializer(row) for row in rows], "total": total,
            "pagina": page, "tamanoPagina": PAGE_SIZE}
```

**Comprobación:** cuatro casos de página (25, 25, 10 y 0 elementos), filtro y orden sobre PostgreSQL, más las cinco rutas paginadas. Con 60 y 300 registros, el listado de elementos realiza 53 SELECT. Persisten consultas por elemento dentro de la página; ese pendiente está delimitado.

## H02 · Validar y escribir un lote estaban mezclados

**Inicial:** `services.py:339`, consulta por campo en 347, reglas de tipo en 353–365 y escritura en 366–371. Pylint señala 18 ramas. El argumento `creating` no se utilizaba.

**Explicación:** para guardar ocho valores se consultaba repetidamente el mismo conjunto de datos. A la vez, reglas como “un campo obligatorio no se puede vaciar” estaban acopladas a la sesión SQL. Esto dificulta comprobar una regla aislada y mantener el flujo al introducir cambios.

**Corrección implementada:** `services.py:331` carga los valores existentes en lote; `value_rules.py:87` valida el conjunto antes de modificar filas. La consulta de opciones se recibe como una función y los protocolos describen solo los datos requeridos.

```python
def write_values(self, element, entries):
    """Carga valores en lote, valida sin escribir y aplica dentro de la transacción."""
    fields = {field.id: field for field in self.fields(element.tipo_elemento_id)}
    existing = {row.campo_id: row for row in self.all(Valor, Valor.elemento_id == element.id)}
    changes = validate_changes(fields, entries, set(existing),
                               lambda option_id: self.get(Opcion, option_id))
    for change in changes:
        row = existing.get(change.field_id)
        if change.attribute is None:
            if row is not None:
                self.db.delete(row)
            continue
        if row is None:
            row = Valor(elemento_id=element.id, campo_id=change.field_id)
        for attribute in ("texto", "numero", "fecha", "opcion_id"):
            setattr(row, attribute, None)
        setattr(row, change.attribute, change.value)
        if change.is_name:
            element.nombre = change.value
        self.db.add(row)
    self.db.flush()
```

**Comprobación:** las consultas para ocho campos numéricos pasan de 10 a 2. Hay pruebas de texto, número finito, fecha, selección, duplicados, pertenencia, obligatorios y vaciado. Un lote con nombre válido y un valor posterior incorrecto conserva datos, autoría y bitácora. Las selecciones todavía requieren consultar la opción elegida; la cifra de dos SELECT corresponde al escenario numérico declarado.

## H03 · La respuesta final se reconstruía cuatro veces

**Inicial:** `services.py:408`, especialmente 411 y 415–418; patrón relacionado en `darBajaElemento:420`. Cada `elemento_json` consulta resumen, campos, opciones y valores.

**Explicación:** comparar, auditar y responder son necesidades diferentes, pero pueden utilizar el mismo estado final. Repetir su lectura añade costo y dispersa la regla de no crear historial cuando nada cambió.

**Corrección implementada:** `services.py:388`, 396 y 405. El estado final se obtiene una vez; al actualizar autoría se sustituye esa sección del resultado y se reutiliza la misma representación para la bitácora y la respuesta.

```python
def _finish_element_change(self, element, before, action):
    """Reutiliza el estado final en respuesta y bitácora, preservando los no cambios."""
    after = self.elemento_json(element)
    if before != after:
        self.touch(element)
        after["autoria"] = self.autoria(element)
        self.audit(element, action, after, before)
    return after
```

**Comprobación:** la modificación de nombre pasa de 57 a 30 SELECT en el escenario de nueve campos, incluyendo la mejora R2. Las pruebas comprueban un solo registro de modificación, coincidencia de bitácora y respuesta, baja repetida y ausencia de cambios de autoría en operaciones idénticas. Los instantes se comparan considerando su zona horaria; dos offsets distintos pueden representar el mismo momento.

## H04 · Service sigue concentrando demasiadas responsabilidades

**Inicial:** `services.py:26`, ayudantes de persistencia en 30–43 y despacho en 142. **Final:** `services.py:18`, persistencia en 22–35 y despacho en 134. R0904 permanece en ambas versiones.

**Explicación:** un cambio de autenticación, un catálogo y una decisión de relación pueden tocar la misma clase. Recibir `db` en el constructor ayuda a componer el servicio, pero las reglas siguen conociendo modelos y consultas concretas. La extracción de valores reduce ese acoplamiento en una parte; todavía no hay una separación completa por dominios.

**Corrección parcial implementada:** la frontera de reglas de valores usa datos y una dependencia pequeña:

```python
class FieldOption(Protocol):
    campo_id: str
    activa: bool

OptionLookup = Callable[[str], FieldOption]

# En Service, el adaptador concreto se conecta desde fuera de la regla:
changes = validate_changes(fields, entries, set(existing),
                           lambda option_id: self.get(Opcion, option_id))
```

**Propuesta pendiente:** separar servicios de usuarios, catálogos y propuestas por composición, conservando `dispatch` como adaptador del contrato. Definir repositorios pequeños según los casos de uso, no una interfaz con todas las operaciones de la base. Antes de migrar propuestas se requieren pruebas de aprobación, rechazo, versión obsoleta y permisos, además del recorrido actual. No se afirma que la clase concentradora quedó resuelta en esta semana.

## H05 · La misma propuesta se transforma en dos sitios

**Inicial:** `services.py:512` y `services.py:529`. **Final:** 497 y 514. Corregir y aprobar construyen el mismo conjunto de claves, con distinto orden de escritura.

**Explicación:** si se añade una regla o dato a una propuesta, es fácil actualizar una proyección y olvidar la otra. Actualmente no se observó divergencia de resultados; el hallazgo es duplicación que aumenta el costo y riesgo de cambio.

**Código corregido propuesto, pendiente de implementar:**

```python
def proposal_input(proposal, changes=None):
    data = {
        "operacion": proposal.operacion,
        "origenId": proposal.origen_id,
        "tipoRelacionId": proposal.tipo_relacion_id,
        "destinoId": proposal.destino_id,
        "relacionId": proposal.relacion_id,
        "versionBase": proposal.version_base,
        "justificacion": proposal.justificacion,
    }
    return {**data, **(changes or {})}

# En corregirPropuestaPendiente:
data = proposal_input(proposal, b)
# En decidirPropuesta:
data = proposal_input(proposal)
```

**Verificación propuesta:** demostrar que corregir conserva los campos no enviados y que aprobar revalida exactamente los mismos extremos y versión. Mantener la restricción de no cambiar extremos de un retiro.

## H06 · El error 500 protege información, pero dificulta el diagnóstico

**Ubicación inicial y final:** `main.py:75`, llamada desde el flujo que ejecuta `Service`.

**Explicación:** existe una separación útil de errores de dominio, integridad, datos y disponibilidad. La última captura genérica evita exponer detalles al cliente, pero el registro solo incluye método y ruta. Dos causas distintas quedan prácticamente indistinguibles. El problema es de observabilidad; no se confirmó una filtración ni se recomienda registrar el cuerpo o la excepción completa, que puede contener parámetros SQL.

**Código corregido propuesto, pendiente de implementar:** importar `uuid4` y sustituir únicamente la última rama:

```python
except Exception as exc:
    error_id = uuid4().hex
    logger.error(
        "error_id=%s exception_type=%s method=%s operation=%s",
        error_id, type(exc).__name__, request.method, operation["operationId"],
    )
    response = error_response(APIError(
        500, "ERROR_INTERNO", "No fue posible completar la operación."
    ))
    response.headers["X-Error-Id"] = error_id
    return response
```

**Verificación propuesta:** provocar un fallo controlado y comprobar correlación entre cabecera y registro, respuesta genérica, reversión de la transacción y ausencia de contraseña, token, cuerpo y parámetros de SQL en ambos destinos.

## H07 · Los nombres internos no explican el papel de los datos

**Inicial:** `services.py:408` usa `p`, `q`, `b` y `e`. **Final:** `services.py:388` conserva esos nombres en el adaptador. Los ayudantes nuevos sí usan nombres como `element`, `entries` y `change`.

**Explicación:** el lector tiene que recordar qué diccionario contiene la ruta y cuál el cuerpo. La mejora puede hacerse sin cambiar `operationId`; renombrar los métodos camelCase directamente rompería el despacho por contrato.

**Código corregido propuesto, pendiente de aplicar al adaptador:**

```python
def modificarElemento(self, path_params, _query, body):
    element = self.get(Elemento, path_params["elementoId"])
    self.may_edit(self.get(TipoElemento, element.tipo_elemento_id).capa_id)
    before = self.elemento_json(element)
    if "valores" in body:
        self.write_values(element, body["valores"])
    if body.get("estado") == "activo":
        element.estado = "activo"
    return self._finish_element_change(element, before, "modificar")
```

## Sección SOLID

La tabla valora el **estado final** y señala el punto de partida. “Parcialmente” delimita lo mejorado y lo pendiente; LSP no se declara violado solamente por existir herencia técnica.

| Principio | ¿Se respeta? | Ejemplo en código, archivo:línea | Propuesta de corrección o conservación |
| --- | --- | --- | --- |
| SRP — responsabilidad única | Parcialmente | Antes, `services.py:339` validaba y persistía; ahora `value_rules.py:87` valida y `services.py:331` aplica cambios. `Service`, en 18, sigue reuniendo dominios. | Mantener la separación implementada y extraer usuarios, catálogos y propuestas en componentes con motivos de cambio distintos (H04). |
| OCP — abierto a extensión, cerrado a modificación | Parcialmente | `services.py:134` despacha por `operationId` sin una cadena de casos. `value_rules.py:65` reúne reglas escalares, pero un tipo nuevo también exige cambiar contrato, almacenamiento y esa tabla. | Preservar el despacho estable; si se requiere extensibilidad de tipos, introducir un registro de estrategias en la composición y probar cada estrategia. No declarar extensible el esquema actual sin migraciones. |
| LSP — sustitución de Liskov | Sí, en el alcance observado | `models.py:19`, 23 y 115: base ORM y mixins de identidad/trazabilidad no redefinen reglas de negocio incompatibles. `value_rules.py:11` y 20 aceptan atributos que suministran tanto modelos como dobles de prueba. | No se identificó una ruptura concreta que corregir. Mantener los contratos de datos, errores y efectos al sustituir colaboradores; añadir pruebas de contrato si aparecen implementaciones de repositorio alternativas. Esto no es una prueba general de toda posible sustitución. |
| ISP — segregación de interfaces | Parcialmente | `value_rules.py:20` necesita solo `campo_id` y `activa`; el validador no recibe el servicio completo. La clase de `services.py:18` conserva 74 métodos públicos y la firma uniforme de operaciones. | Mantener puertos pequeños por caso de uso. La firma HTTP puede quedarse en el adaptador, mientras los servicios de dominio reciben únicamente sus datos necesarios (H04/H07). |
| DIP — inversión de dependencias | Parcialmente | `value_rules.py:26` y 87 dependen de una función de consulta; `services.py:335` conecta el acceso concreto a opciones. El resto de Service sigue construyendo expresiones de SQLAlchemy. | Ampliar esa inversión por etapas con repositorios específicos, inyectados desde la composición. No trasladar consultas SQL a la capa de reglas. |

## Seguridad y manejo de errores revisados

- El filtro por nombre usa `contains(..., autoescape=True)` (`services.py` inicial 379, final 359). No se observó concatenación del texto del usuario en SQL. Las consultas de esta revisión se construyen con expresiones parametrizadas.
- `security.py:18`, 25, 58 y `main.py:54` centralizan correo, contraseñas, JWT, sesión y rol. Las pruebas existentes cubren ausencia/firma inválida, expiración, inactividad, revocación, permisos, registro y contraseñas.
- `contract.py:44` construye errores de validación sin reutilizar mensajes que puedan incluir secretos. `main.py:69` a 78 entrega errores genéricos de persistencia.
- El despacho recibe `operationId` del contrato cargado por el servidor, no un nombre de método suministrado libremente por el cliente.

No se demostró inyección SQL ni exposición de contraseña en los casos revisados. Los 84 casos aprobados tampoco permiten afirmar ausencia total de vulnerabilidades. El tratamiento de errores inesperados conserva el pendiente H06.

## Evidencia de la revisión

`evidencias/antes/pytest.txt`: 50 casos existentes aprobados. `evidencias/despues/pytest.xml`: 84 casos aprobados, incluidos los 50 originales sin modificar. El recorrido original verifica las 46 operaciones del contrato. Los 34 casos nuevos incluyen 21 pruebas parametrizadas de reglas y 13 de integración/rendimiento. No se midió cobertura de líneas ni se realizó una revisión independiente por otro integrante.

Esta es una revisión asistida. La rúbrica pide explicación propia: Jean Paul debe leer y ajustar las interpretaciones antes de presentar el documento como su valoración final; su prioridad de rendimiento ya está incorporada.
