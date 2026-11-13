"""Reglas de valores de campo, independientes de SQLAlchemy y de la transacción."""
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import date
from math import isfinite
from typing import Any, Protocol

from .errors import invalid


class FieldDefinition(Protocol):
    """Datos mínimos que necesita una regla; no expone operaciones de persistencia."""
    id: str
    nombre: str
    tipo_dato: str
    obligatorio: bool
    es_base_nombre: bool


class FieldOption(Protocol):
    """Estado consultable de una opción, sin depender de su modelo de almacenamiento."""
    campo_id: str
    activa: bool


OptionLookup = Callable[[str], FieldOption]


@dataclass(frozen=True)
class ValueChange:
    """Cambio validado; attribute=None representa vaciar un campo opcional."""
    field_id: str
    attribute: str | None
    value: Any = None
    is_name: bool = False


def clean(value: str, field: str = "nombre", maximum: int = 120) -> str:
    """Normaliza texto y comprueba longitud después de quitar espacios extremos."""
    value = value.strip()
    if not value or len(value) > maximum:
        invalid(f"{field} debe tener entre 1 y {maximum} caracteres sin espacios extremos.", field)
    return value


def _text_value(field: FieldDefinition, value: str) -> str:
    if field.obligatorio and not value.strip():
        invalid("Un texto obligatorio no puede estar vacío.", "valores")
    return clean(value, "Nombre", 500) if field.es_base_nombre else value


def _number_value(_field: FieldDefinition, value: float) -> float:
    if not isfinite(value):
        invalid("El número debe ser finito.", "valores")
    return value


def _date_value(_field: FieldDefinition, value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError:
        invalid("La fecha no es válida.", "valores")


_SCALAR_RULES = {"texto": _text_value, "numero": _number_value, "fecha": _date_value}


def normalize_change(field: FieldDefinition, entry: Mapping[str, Any],
                     lookup_option: OptionLookup) -> ValueChange:
    """Valida y convierte una entrada cuyo formato JSON ya revisó el contrato."""
    if entry.get("vaciar"):
        if field.obligatorio:
            invalid("No se puede vaciar un campo obligatorio.", "valores")
        return ValueChange(field.id, None)
    key = "opcionId" if field.tipo_dato == "seleccion" else field.tipo_dato
    if key not in entry:
        invalid("El valor no corresponde al tipo de campo.", "valores")
    value = entry[key]
    if key == "opcionId":
        option = lookup_option(value)
        if option.campo_id != field.id or not option.activa:
            invalid("La opción no pertenece al campo.", "valores")
        return ValueChange(field.id, "opcion_id", value)
    return ValueChange(field.id, key, _SCALAR_RULES[key](field, value), field.es_base_nombre)


def validate_changes(fields: Mapping[str, FieldDefinition], entries: Sequence[Mapping[str, Any]],
                     existing_ids: set[str], lookup_option: OptionLookup) -> list[ValueChange]:
    """Comprueba el lote completo y los obligatorios antes de modificar filas."""
    identifiers = [entry["campoId"] for entry in entries]
    if len(set(identifiers)) != len(identifiers):
        invalid("No se permiten campos repetidos.", "valores")
    changes = []
    present = set(existing_ids)
    for entry in entries:
        field = fields.get(entry["campoId"])
        if field is None:
            invalid("El campo no pertenece al tipo.", "valores")
        change = normalize_change(field, entry, lookup_option)
        changes.append(change)
        if change.attribute is None:
            present.discard(change.field_id)
        else:
            present.add(change.field_id)
    for field in fields.values():
        if field.obligatorio and field.id not in present:
            invalid(f"Falta el campo obligatorio {field.nombre}.", "valores")
    return changes
