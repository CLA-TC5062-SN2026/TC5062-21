"""Casos de negocio del validador usando colaboradores sin base de datos."""
from datetime import date
from types import SimpleNamespace

import pytest

from backend.app.errors import APIError
from backend.app.value_rules import validate_changes


def field(kind="texto", required=False, base=False):
    return SimpleNamespace(id="campo", nombre="Dato", tipo_dato=kind,
                           obligatorio=required, es_base_nombre=base)


def option(_ident):
    return SimpleNamespace(campo_id="campo", activa=True)


@pytest.mark.parametrize("definition,entry,attribute,expected", [
    (field(), {"texto": "  conservar  "}, "texto", "  conservar  "),
    (field(required=True, base=True), {"texto": "  Nombre  "}, "texto", "Nombre"),
    (field("numero"), {"numero": 0}, "numero", 0),
    (field("numero"), {"numero": -2.5}, "numero", -2.5),
    (field("fecha"), {"fecha": "2024-02-29"}, "fecha", date(2024, 2, 29)),
    (field("seleccion"), {"opcionId": "opcion"}, "opcion_id", "opcion"),
    (field(), {"vaciar": True}, None, None),
])
def test_valid_field_values(definition, entry, attribute, expected):
    changes = validate_changes({"campo": definition}, [{"campoId": "campo", **entry}],
                               set(), option)
    assert len(changes) == 1
    assert (changes[0].attribute, changes[0].value) == (attribute, expected)
    assert changes[0].is_name == (definition.es_base_nombre and attribute is not None)


@pytest.mark.parametrize("definition,entry,message", [
    (field(), {"numero": 2}, "tipo de campo"),
    (field(required=True), {"texto": "  "}, "vacío"),
    (field(required=True), {"vaciar": True}, "obligatorio"),
    (field("fecha"), {"fecha": "2025-02-29"}, "fecha"),
    (field("numero"), {"numero": float("inf")}, "finito"),
    (field("numero"), {"numero": float("-inf")}, "finito"),
    (field("numero"), {"numero": float("nan")}, "finito"),
])
def test_invalid_values_keep_domain_error(definition, entry, message):
    with pytest.raises(APIError) as caught:
        validate_changes({"campo": definition}, [{"campoId": "campo", **entry}], set(), option)
    assert caught.value.status == 422
    assert message in caught.value.body["mensaje"]


@pytest.mark.parametrize("entries,message", [
    ([{"campoId": "campo", "texto": "A"}] * 2, "repetidos"),
    ([{"campoId": "ajeno", "texto": "A"}], "pertenece"),
    ([], "Falta el campo obligatorio"),
])
def test_batch_rejects_duplicates_foreign_fields_and_missing_required(entries, message):
    with pytest.raises(APIError, match=message):
        validate_changes({"campo": field(required=True)}, entries, set(), option)


@pytest.mark.parametrize("field_id,active", [("ajeno", True), ("campo", False)])
def test_option_must_be_active_and_belong_to_field(field_id, active):
    def lookup(_ident):
        return SimpleNamespace(campo_id=field_id, activa=active)

    with pytest.raises(APIError, match="opción no pertenece"):
        validate_changes({"campo": field("seleccion")},
                         [{"campoId": "campo", "opcionId": "opcion"}], set(), lookup)


def test_partial_update_keeps_existing_required_values():
    assert validate_changes({"campo": field(required=True)}, [], {"campo"}, option) == []


def test_scalar_rule_does_not_need_option_storage():
    def unavailable_lookup(_ident):
        raise AssertionError("Un número no debe consultar opciones ni abrir conexión.")

    change = validate_changes({"campo": field("numero")},
                              [{"campoId": "campo", "numero": 42}], set(), unavailable_lookup)
    assert change[0].value == 42
