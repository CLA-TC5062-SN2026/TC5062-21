# Tres refactorizaciones implementadas y verificadas

Equipo 21 · TC5062 · Semana 9 · 13 de noviembre de 2026

Preparado para Jean Paul Lozano Gámiz con asistencia de Codex. Prioridad indicada por el estudiante: mejorar el rendimiento al crecer los datos.

## Objetivo y criterio de selección

Se implementaron **tres refactorizaciones** sobre el backend de Semana 8. La prioridad definida por Jean Paul fue mejorar el rendimiento al crecer los datos. H01, H02 y H03 combinan costo medido, cambios acotados y verificaciones disponibles. La separación completa de Service implica mayor alcance y se registra como deuda posterior.

Se conservan rutas, formatos del contrato, tamaño de página de 25, permisos, transacciones y reglas de autoría. El middleware continúa siendo propietario de la transacción. No se modificaron el contrato OpenAPI, el esquema SQL ni las 50 pruebas existentes.

## R1 · Paginar en PostgreSQL antes de serializar

**Problema H01:** se cargaba todo el resultado y se recortaba después de ejecutar el serializador. Se encontró en `services.py:126` de la base.

**Antes — código real:**

```python
def listing(self, values, serializer, q=None, paginated=False):
    result = {"items": [serializer(v) for v in values], "total": len(values)}
    if paginated:
        page = (q or {}).get("pagina", 1)
        result["items"] = result["items"][(page-1)*25:page*25]
        result.update(pagina=page, tamanoPagina=25)
    return result
```

**Después — código real de `pagination.py:7`:**

```python
def paginate(db, statement, serializer, page=1):
    """Conserva filtros y orden del SELECT, y serializa como máximo una página."""
    total = db.scalar(select(func.count()).select_from(statement.order_by(None).subquery()))
    rows = db.scalars(statement.limit(PAGE_SIZE).offset((page - 1) * PAGE_SIZE))
    return {"items": [serializer(row) for row in rows], "total": total,
            "pagina": page, "tamanoPagina": PAGE_SIZE}
```

Los cinco listados con paginación construyen un SELECT ordenado y llaman a `_paginated`. El total se obtiene sobre el mismo filtro sin orden; LIMIT/OFFSET se aplican antes de cargar y convertir filas. Los catálogos cuyo contrato no contempla páginas conservan su respuesta completa.

**Justificación:** el trabajo de serialización queda limitado a 25 registros por solicitud. El diseño comparte la política de paginación sin mezclarla con cada serializador. Se preserva un orden determinista: correo para usuarios, nombre normalizado e id para elementos, id para propuestas/relaciones y fecha descendente e id para bitácora.

**Evidencia:** pruebas de páginas completas, última página, página fuera de rango, filtro, orden y cinco rutas. Con 300 elementos, el costo observado baja de 602 a 53 SELECT (91.20% menos). El mismo resultado se obtiene con 60 elementos después del cambio.

## R2 · Separar reglas y guardar valores en lote

**Problema H02:** `write_values` combinaba reglas, consultas por entrada y mutaciones; Pylint detectaba 18 ramas. El argumento `creating` no intervenía.

**Antes — código real de `services.py:339`:**

```python
def write_values(self, e, entries, creating=False):
    fields = {c.id: c for c in self.fields(e.tipo_elemento_id)}
    ids = [item["campoId"] for item in entries]
    if len(set(ids)) != len(ids): invalid("No se permiten campos repetidos.", "valores")
    for item in entries:
        c = fields.get(item["campoId"])
        if not c: invalid("El campo no pertenece al tipo.", "valores")
        old = self.db.scalar(select(Valor).where(Valor.elemento_id == e.id, Valor.campo_id == c.id))
        if item.get("vaciar"):
            if c.obligatorio: invalid("No se puede vaciar un campo obligatorio.", "valores")
            if old: self.db.delete(old)
            continue
        key = {"texto": "texto", "numero": "numero", "fecha": "fecha", "seleccion": "opcionId"}[c.tipo_dato]
        if key not in item: invalid("El valor no corresponde al tipo de campo.", "valores")
        value = item[key]
        if key == "texto":
            if c.obligatorio and not value.strip(): invalid("Un texto obligatorio no puede estar vacío.", "valores")
            if c.es_base_nombre: value = clean(value, "Nombre", 500); e.nombre = value
        if key == "numero" and not isfinite(value): invalid("El número debe ser finito.", "valores")
        if key == "fecha":
            try: value = date.fromisoformat(value)
            except ValueError: invalid("La fecha no es válida.", "valores")
        if key == "opcionId":
            option = self.get(Opcion, value)
            if option.campo_id != c.id or not option.activa: invalid("La opción no pertenece al campo.", "valores")
        row = old or Valor(elemento_id=e.id, campo_id=c.id)
        for attr in ("texto", "numero", "fecha", "opcion_id"): setattr(row, attr, None)
        setattr(row, "opcion_id" if key == "opcionId" else key, value)
        self.db.add(row)
    self.db.flush()
    present = set(self.db.scalars(select(Valor.campo_id).where(Valor.elemento_id == e.id)))
    for c in fields.values():
        if c.obligatorio and c.id not in present: invalid(f"Falta el campo obligatorio {c.nombre}.", "valores")
```

**Después — código real de `services.py:331`:**

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

Las reglas se concentran en `value_rules.py`. `validate_changes` recibe el inventario de campos, los valores presentes y una función para consultar opciones. Devuelve cambios validados antes de modificar filas. Los modelos ORM satisfacen los protocolos de atributos; las pruebas también pueden usar objetos sencillos sin base de datos.

**Justificación:** mejora SRP al separar validación y persistencia, y DIP al inyectar la consulta concreta de opciones. Los valores actuales se leen una sola vez; los obligatorios se revisan sobre el conjunto resultante. Se conserva una columna de valor activa por fila. `clean` se mueve al módulo de reglas para compartir la normalización; `invalid` declara `NoReturn` porque siempre lanza un error. Son ajustes de soporte de esta refactorización.

**Evidencia:** escribir ocho campos numéricos baja de 10 a 2 SELECT (80% menos). `write_values` pasa de 33 a 21 líneas físicas y deja de activar R0912. Las pruebas comprueban tipos, fecha inválida, números no finitos, opciones ajenas/inactivas, duplicados, campos ajenos, obligatorios, vaciado y actualización parcial. La prueba HTTP del lote inválido comprueba persistencia y bitácora después del rechazo.

## R3 · Reutilizar el estado final del elemento

**Problema H03:** modificar un elemento podía ejecutar cuatro veces su serialización completa. La baja repetía parte de la misma política de historial.

**Antes — código real de `services.py:408`:**

```python
def modificarElemento(self, p, q, b):
    e = self.get(Elemento, p["elementoId"])
    self.may_edit(self.get(TipoElemento, e.tipo_elemento_id).capa_id)
    before = self.elemento_json(e)
    if "valores" in b: self.write_values(e, b["valores"])
    if b.get("estado") == "activo": e.estado = "activo"
    # No renovar autoría ni bitácora si una asignación no cambia los valores.
    if before != self.elemento_json(e):
        self.touch(e)
        self.audit(e, "modificar", self.elemento_json(e), before)
    return self.elemento_json(e)
```

**Después — código real de `services.py:388` y 405:**

```python
def modificarElemento(self, p, q, b):
    e = self.get(Elemento, p["elementoId"])
    self.may_edit(self.get(TipoElemento, e.tipo_elemento_id).capa_id)
    before = self.elemento_json(e)
    if "valores" in b: self.write_values(e, b["valores"])
    if b.get("estado") == "activo": e.estado = "activo"
    return self._finish_element_change(e, before, "modificar")
```

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

La baja también utiliza este ayudante y devuelve el estado conocido si ya estaba de baja. Cuando existe un cambio se actualiza la autoría en la representación final, sin repetir las consultas de campos y opciones.

**Justificación:** se mantiene una sola política para comparar, actualizar autoría, auditar y responder. El resultado guardado en bitácora coincide con el enviado al cliente. Los cambios idénticos siguen sin generar entradas nuevas.

**Evidencia:** la modificación del nombre pasa de 57 a 30 SELECT (47.37% menos). Esta comparación representa el resultado combinado R2+R3, no atribuye toda la reducción a R3. Las pruebas comprueban exactamente un registro por cambio, igualdad entre respuesta e historial y conservación de autoría al repetir una operación.

## Comparación medida

La medición se ejecuta sobre `arquitectura21_test`, con un tipo de elemento, nueve campos por elemento (Nombre y ocho números) y conjuntos de 60/300 elementos. La preparación queda fuera del conteo. Se vacía el mapa de identidad de la sesión antes de cada caso para no favorecer una caché de la ejecución previa. Cada muestra termina en rollback.

| Caso | Datos | SELECT antes | SELECT después | Reducción |
| --- | --- | ---: | ---: | ---: |
| Listar página 1, 25 resultados | 60 elementos | 122 | 53 | 56.56% |
| Listar página 1, 25 resultados | 300 elementos | 602 | 53 | 91.20% |
| Guardar ocho campos numéricos | 60 y 300 elementos | 10 | 2 | 80.00% |
| Modificar nombre con nueve campos | 60 y 300 elementos | 57 | 30 | 47.37% |

Son **SELECT enviados por SQLAlchemy**, no todas las sentencias internas de PostgreSQL: no incluyen SQL de triggers, preparación de datos ni autenticación HTTP. No se midieron percentiles de latencia, concurrencia, CPU o memoria. Los porcentajes usan `(antes-después)/antes×100`.

## Verificación y trazabilidad

| Evidencia | Resultado |
| --- | --- |
| `evidencias/antes/pytest.xml` | 50 casos originales aprobados |
| `evidencias/despues/pytest.xml` | 84 casos aprobados: 50 originales + 34 nuevos |
| `evidencias/despues/cobertura_operaciones.json` | Recorrido con las 46 operaciones del contrato verificadas por esquema |
| `evidencias/antes/consultas.json` y `despues/consultas.json` | Conteos sobre las mismas condiciones declaradas |
| `evidencias/antes/ejecucion.json` y `despues/ejecucion.json` | Herramientas, hashes, mensajes y tamaños de los archivos |
| `evidencias/cambios.patch` | Diferencia de código y pruebas frente a la base local |

Hay una advertencia de deprecación de Starlette sobre su integración con httpx, presente tanto antes como después. No impide la ejecución y se conserva visible. Las nuevas comprobaciones se añadieron después de implementar las mejoras; no se presenta el proceso como TDD.

## Límites y riesgos pendientes

La paginación limita las filas cargadas, pero `COUNT(*)` aún debe evaluar el conjunto filtrado y los offsets altos pueden ser costosos. También persisten consultas por tipo/capa dentro de una página. Bajo el aislamiento predeterminado READ COMMITTED, conteo y lectura son dos sentencias: escrituras concurrentes pueden cambiar el conjunto entre ambas. Si el producto necesita una fotografía estrictamente consistente, se debe definir y probar aislamiento de lectura o una estrategia equivalente.

La validación en lote lee todos los valores existentes de un elemento; si un elemento llega a tener miles de campos será necesario medir ese costo. Los casos de selección mantienen consultas de opciones. El bloqueo global de escrituras permanece y requiere una evaluación de concurrencia antes de escalar.

La clase Service pasa de 629 a 615 líneas y conserva 74 métodos públicos. El tamaño total del producto crece de 1,168 a 1,278 líneas por las nuevas fronteras explícitas. La mejora se sustenta en consultas reducidas y comportamiento verificado, no en borrar líneas o alcanzar una calificación perfecta del linter.
