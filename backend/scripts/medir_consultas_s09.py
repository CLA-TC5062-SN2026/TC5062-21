"""Compara SELECT de aplicación con datos sintéticos y revierte toda la muestra."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

from dotenv import dotenv_values
from sqlalchemy import create_engine, event, select
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from backend.app.models import Elemento, Usuario, Valor, uid
from backend.app.services import Service


@contextmanager
def count_selects(engine):
    """Cuenta sentencias enviadas por SQLAlchemy; no incluye SQL interno de triggers."""
    counter = {"selects": 0}

    def capture(_connection, _cursor, statement, _parameters, _context, _many):
        if statement.lstrip().upper().startswith("SELECT"):
            counter["selects"] += 1

    event.listen(engine, "before_cursor_execute", capture)
    try:
        yield counter
    finally:
        event.remove(engine, "before_cursor_execute", capture)


def run_sample(engine, size):
    """Mide tres casos de uso dentro de una transacción que nunca se confirma."""
    with Session(engine, expire_on_commit=False) as db:
        try:
            admin = db.scalar(select(Usuario).where(Usuario.rol == "Administrador"))
            if admin is None:
                raise RuntimeError("Ejecute primero pytest para preparar la base aislada.")
            service = Service(db, admin, None, None)
            layer = service.crearCapa({}, {}, {"nombre": "Medición " + uid()})
            kind = service.crearTipoElemento({}, {}, {"nombre": "Medible", "capaId": layer["id"]})
            base_id = kind["campos"][0]["id"]
            numeric_ids = []
            for index in range(8):
                field = service.crearCampo({"tipoId": kind["id"]}, {}, {
                    "nombre": f"Dato {index}", "tipoDato": "numero",
                    "obligatorio": False, "opciones": []})
                numeric_ids.append(field["id"])
            identifiers = [uid() for _ in range(size)]
            for index, ident in enumerate(identifiers):
                db.add(Elemento(id=ident, tipo_elemento_id=kind["id"],
                                nombre=f"Elemento {index:04d}", estado="activo",
                                creador_id=admin.id, ultimo_modificador_id=admin.id))
            db.flush()
            for index, ident in enumerate(identifiers):
                db.add(Valor(elemento_id=ident, campo_id=base_id, texto=f"Elemento {index:04d}"))
                for field_id in numeric_ids:
                    db.add(Valor(elemento_id=ident, campo_id=field_id, numero=1))
            db.flush()
            db.expunge_all()
            with count_selects(engine) as listing_count:
                page = service.listarElementos({}, {"tipoElementoId": kind["id"], "pagina": 1}, {})
            assert page["total"] == size and len(page["items"]) == 25
            assert page["items"][0]["nombre"] == "Elemento 0000"
            db.expunge_all()
            element = service.get(Elemento, identifiers[0])
            entries = [{"campoId": field_id, "numero": 2} for field_id in numeric_ids]
            with count_selects(engine) as write_count:
                service.write_values(element, entries)
            assert db.scalar(select(Valor.numero).where(
                Valor.elemento_id == element.id, Valor.campo_id == numeric_ids[0])) == 2
            db.expunge_all()
            with count_selects(engine) as modify_count:
                result = service.modificarElemento({"elementoId": identifiers[0]}, {}, {
                    "valores": [{"campoId": base_id, "texto": "Nombre actualizado"}]})
            assert result["nombre"] == "Nombre actualizado"
            return {"elementos": size, "campos_por_elemento": 9,
                    "elementos_devueltos": len(page["items"]),
                    "listar_pagina_1": listing_count["selects"],
                    "guardar_8_campos": write_count["selects"],
                    "modificar_nombre": modify_count["selects"]}
        finally:
            db.rollback()


def main():
    """Usa exclusivamente arquitectura21_test, la misma base aislada de pytest."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    values = dotenv_values(ROOT / "backend/.env")
    url = make_url(values["DATABASE_URL"]).set(database="arquitectura21_test")
    assert url.database == "arquitectura21_test"
    engine = create_engine(url)
    try:
        samples = [run_sample(engine, size) for size in (60, 300)]
        report = {"fecha_utc": datetime.now(timezone.utc).isoformat(),
                  "metrica": "SELECT enviados por SQLAlchemy; sin autenticación HTTP ni SQL de triggers",
                  "aislamiento": "Cada muestra usa rollback; no modifica la base de trabajo.",
                  "muestras": samples}
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n",
                               encoding="utf-8")
        print(json.dumps(samples, ensure_ascii=False))
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
