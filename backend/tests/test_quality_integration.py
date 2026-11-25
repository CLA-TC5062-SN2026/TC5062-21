"""Regresión de paginación, transacciones, autoría y costo de consultas de Semana 9."""
from datetime import datetime, timezone
from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models import Bitacora, Capa
from backend.app.pagination import paginate
from backend.scripts.medir_consultas_s09 import count_selects, run_sample


def normalized_timestamps(value):
    """Compara instantes, porque PostgreSQL puede devolver un offset distinto a UTC."""
    if isinstance(value, list):
        return [normalized_timestamps(item) for item in value]
    if isinstance(value, dict):
        return {key: (datetime.fromisoformat(item).astimezone(timezone.utc).isoformat()
                      if key in {"creadoEn", "modificadoEn"} else normalized_timestamps(item))
                for key, item in value.items()}
    return value


@pytest.mark.parametrize("page,expected", [(1, 25), (2, 25), (3, 10), (4, 0)])
def test_pagination_keeps_filters_total_order_and_boundaries(api, page, expected):
    prefix = "Página-" + uuid4().hex
    with Session(api.test_engine) as db:
        try:
            db.add_all([Capa(nombre=f"{prefix}-{index:03d}") for index in range(60)])
            db.add(Capa(nombre="Excluida-" + uuid4().hex))
            db.flush()
            serialized = []

            def serialize(row):
                serialized.append(row.id)
                return row.nombre

            statement = select(Capa).where(Capa.nombre.startswith(prefix)).order_by(Capa.nombre)
            with count_selects(api.test_engine) as count:
                result = paginate(db, statement, serialize, page)
            assert result["total"] == 60
            assert result["pagina"] == page and result["tamanoPagina"] == 25
            assert len(result["items"]) == len(serialized) == expected
            start = (page - 1) * 25
            assert result["items"] == [f"{prefix}-{i:03d}" for i in range(start, start + expected)]
            assert count["selects"] == 2
        finally:
            db.rollback()


@pytest.mark.parametrize("resource", ["usuarios", "elementos", "propuestas-relacion", "relaciones", "entradas-bitacora"])
def test_all_paginated_routes_keep_total_on_empty_page(api, admin_token, resource):
    headers = {"Authorization": "Bearer " + admin_token}
    first = api.get("/api/v1/" + resource, headers=headers)
    empty = api.get("/api/v1/" + resource, params={"pagina": 100000}, headers=headers)
    assert first.status_code == empty.status_code == 200
    assert empty.json()["items"] == []
    assert empty.json()["total"] == first.json()["total"]
    assert empty.json()["pagina"] == 100000


@pytest.fixture
def sample_element(api, admin_token):
    headers = {"Authorization": "Bearer " + admin_token}

    def post(route, body):
        response = api.post("/api/v1/" + route, headers=headers, json=body)
        assert response.status_code == 201, response.text
        return response.json()

    layer = post("capas", {"nombre": "Regresión-" + uuid4().hex})
    kind = post("tipos-elemento", {"nombre": "Entidad", "capaId": layer["id"]})
    base = kind["campos"][0]["id"]
    number = post(f"tipos-elemento/{kind['id']}/campos", {
        "nombre": "Monto", "tipoDato": "numero", "obligatorio": False, "opciones": []})
    element = post("elementos", {"tipoElementoId": kind["id"], "valores": [
        {"campoId": base, "texto": "Nombre inicial"}, {"campoId": number["id"], "numero": 7}]})
    return headers, element, base, number["id"]


def test_invalid_later_value_rolls_back_name_and_history(api, sample_element):
    headers, element, base, number = sample_element
    response = api.patch("/api/v1/elementos/" + element["id"], headers=headers, json={"valores": [
        {"campoId": base, "texto": "No debe persistir"}, {"campoId": number, "texto": "tipo incorrecto"}]})
    assert response.status_code == 422
    current = api.get("/api/v1/elementos/" + element["id"], headers=headers).json()
    assert normalized_timestamps(current) == normalized_timestamps(element)
    with Session(api.test_engine) as db:
        entries = list(db.scalars(select(Bitacora).where(Bitacora.objeto_id == element["id"])))
        assert len(entries) == 1 and entries[0].accion == "alta"


def test_change_response_matches_history_and_noop_keeps_authorship(api, sample_element):
    headers, element, base, _number = sample_element
    payload = {"valores": [{"campoId": base, "texto": "Nombre actualizado"}]}
    route = "/api/v1/elementos/" + element["id"]
    changed = api.patch(route, headers=headers, json=payload)
    assert changed.status_code == 200
    unchanged = api.patch(route, headers=headers, json=payload)
    assert unchanged.status_code == 200
    assert normalized_timestamps(unchanged.json()) == normalized_timestamps(changed.json())
    with Session(api.test_engine) as db:
        entries = list(db.scalars(select(Bitacora).where(
            Bitacora.objeto_id == element["id"], Bitacora.accion == "modificar")))
        assert len(entries) == 1
        assert normalized_timestamps(entries[0].valores_antes) == normalized_timestamps(element)
        assert entries[0].valores_despues == changed.json()
    retired = api.delete(route, headers=headers)
    assert retired.status_code == 200
    assert retired.json()["estado"] == "baja"
    repeated = api.delete(route, headers=headers)
    assert repeated.status_code == 200
    assert normalized_timestamps(repeated.json()) == normalized_timestamps(retired.json())
    with Session(api.test_engine) as db:
        entries = list(db.scalars(select(Bitacora).where(
            Bitacora.objeto_id == element["id"], Bitacora.accion == "baja")))
        assert len(entries) == 1 and entries[0].valores_despues == retired.json()


def test_optional_value_can_be_cleared_without_losing_required_name(api, sample_element):
    headers, element, _base, number = sample_element
    response = api.patch("/api/v1/elementos/" + element["id"], headers=headers,
                         json={"valores": [{"campoId": number, "vaciar": True}]})
    assert response.status_code == 200
    assert response.json()["nombre"] == element["nombre"]
    assert number not in {item["campoId"] for item in response.json()["valores"]}


def test_query_budgets_do_not_return_to_full_scan(api):
    sample = run_sample(api.test_engine, 60)
    assert sample["listar_pagina_1"] <= 55
    assert sample["guardar_8_campos"] <= 2
    assert sample["modificar_nombre"] <= 30
