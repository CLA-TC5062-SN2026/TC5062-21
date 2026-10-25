"""Exportación determinista de tablas e índices ORM para revisión/importación con psql."""
from pathlib import Path
import sys

from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateIndex, CreateTable

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from backend.app.models import Base

dialect = postgresql.dialect()
parts = ["-- Equipo 21 · PostgreSQL 17 · esquema revisado S05-S06-A1\nBEGIN;"]
for table in Base.metadata.sorted_tables:
    parts.append(str(CreateTable(table).compile(dialect=dialect)).strip() + ";")
    for index in sorted(table.indexes, key=lambda i: i.name):
        parts.append(str(CreateIndex(index).compile(dialect=dialect)).strip() + ";")
parts.append("""
-- La bitácora conserva evidencia; tampoco admite escrituras destructivas por SQL.
CREATE FUNCTION impedir_cambio_bitacora() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  RAISE EXCEPTION 'La bitácora es inmutable' USING ERRCODE = '23514';
END;
$$;
CREATE TRIGGER bitacora_inmutable BEFORE UPDATE OR DELETE ON entradas_bitacora
FOR EACH ROW EXECUTE FUNCTION impedir_cambio_bitacora();

-- El permiso de Editor y la compatibilidad de los cuatro valores se validan
-- también en el servicio bajo la misma transacción. Las FKs impiden huérfanos.
CREATE FUNCTION validar_valor_campo() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE campo definiciones_campo%ROWTYPE; tipo UUID; opcion UUID;
BEGIN
  SELECT * INTO campo FROM definiciones_campo WHERE id = NEW.campo_id;
  SELECT tipo_elemento_id INTO tipo FROM elementos WHERE id = NEW.elemento_id;
  IF campo.tipo_elemento_id <> tipo OR
     (campo.tipo_dato = 'texto' AND NEW.texto IS NULL) OR
     (campo.tipo_dato = 'numero' AND NEW.numero IS NULL) OR
     (campo.tipo_dato = 'fecha' AND NEW.fecha IS NULL) OR
     (campo.tipo_dato = 'seleccion' AND NEW.opcion_id IS NULL) OR
     (campo.obligatorio AND NEW.texto IS NOT NULL AND length(btrim(NEW.texto)) = 0)
  THEN RAISE EXCEPTION 'Valor incompatible con definición' USING ERRCODE = '23514'; END IF;
  IF NEW.opcion_id IS NOT NULL THEN
    SELECT campo_id INTO opcion FROM opciones_campo WHERE id = NEW.opcion_id AND activa;
    IF opcion IS NULL OR opcion <> NEW.campo_id THEN
      RAISE EXCEPTION 'Opción ajena al campo' USING ERRCODE = '23514';
    END IF;
  END IF;
  RETURN NEW;
END;
$$;
CREATE TRIGGER valor_compatible BEFORE INSERT OR UPDATE ON valores_campo
FOR EACH ROW EXECUTE FUNCTION validar_valor_campo();
COMMIT;
""".strip())
out = ROOT / "S05_S06_A1/esquema_bd.sql"
out.write_text("\n\n".join(parts) + "\n")
print(f"SQL exportado: {len(Base.metadata.tables)} tablas")
