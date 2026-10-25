"""Genera la vista de clases a partir del mismo modelo que produce la DDL."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from backend.app.models import Base

names = {mapper.local_table.name: mapper.class_.__name__ for mapper in Base.registry.mappers}


def camel(name):
    head, *tail = name.split("_")
    return head + "".join(part.title() for part in tail)


lines = ["@startuml", "hide methods", "skinparam classAttributeIconSize 0", "skinparam linetype ortho",
         "title Equipo 21 — Modelo consolidado y persistencia PostgreSQL", "left to right direction"]
for table in Base.metadata.sorted_tables:
    lines.append(f'class {names[table.name]} <<{table.name}>> {{')
    for column in table.columns:
        access = "-" if "hash" in column.name else "+"
        kind = str(column.type).split(" COLLATE")[0].replace("VARCHAR", "String").replace("TIMESTAMP", "DateTime").replace("BOOLEAN", "Boolean")
        flags = (" {PK}" if column.primary_key else "") + (" [0..1]" if column.nullable else "")
        lines.append(f'  {access}{camel(column.name)} : {kind}{flags}')
    lines.append("}")
for table in Base.metadata.sorted_tables:
    for fk in table.foreign_keys:
        target = "0..1" if fk.parent.nullable else "1"
        lines.append(f'{names[table.name]} "0..*" --> "{target}" {names[fk.column.table.name]} : {camel(fk.parent.name)}')
lines += [
    "note bottom of Usuario", "  correo único normalizado; hash bcrypt interno.", "  Administrador / Editor / Consulta.", "end note",
    "note bottom of Valor", "  Un único valor tipado por (elemento, campo).", "  ValorTexto/Numero/Fecha/Seleccion de Jean Paul se concretan", "  en una tabla con CHECK de exclusión y trigger de compatibilidad.", "end note",
    "note bottom of Bitacora", "  Solo lectura por API; UPDATE/DELETE rechazados en PostgreSQL.", "  Instantáneas públicas sin contraseñas, hashes ni JWT.", "end note",
    "note bottom of Propuesta", "  Alta: sin relación objetivo. Cambio/retiro: relación y versión obligatorias.", "  Una decisión por propuesta; aprobar revalida extremos y duplicados.", "end note",
    "note bottom of Opcion", "  Reemplazo de opciones conserva las anteriores como inactivas.", "end note", "@enduml"]
(ROOT / "S05_S06_A1/diagrama_clases_equipo.puml").write_text("\n".join(lines)+"\n")
print("Diagrama consolidado: 15 clases persistentes, atributos y asociaciones generados desde el modelo físico.")
