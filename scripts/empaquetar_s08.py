"""Valida evidencias y construye ZIP de código/documentación sin archivos privados."""
import hashlib
import json
from pathlib import Path
import struct
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "entregas"
BLOCKED = {".git", ".local", ".venv", "node_modules", "dist", "__pycache__", ".pytest_cache", ".vite", "entregas"}

def boxes(data, start, end):
    while start + 8 <= end:
        size, kind = struct.unpack_from(">I4s", data, start)
        header = 8
        if size == 1:
            size = struct.unpack_from(">Q", data, start + 8)[0]
            header = 16
        elif size == 0:
            size = end - start
        if size < header or start + size > end:
            raise ValueError("Contenedor MP4 inválido")
        yield kind, start + header, start + size
        start += size

def duration(path):
    data = path.read_bytes()
    for kind, start, end in boxes(data, 0, len(data)):
        if kind == b"moov":
            for child, a, b in boxes(data, start, end):
                if child == b"mvhd":
                    if data[a] == 0:
                        scale, ticks = struct.unpack_from(">II", data, a + 12)
                    elif data[a] == 1:
                        scale = struct.unpack_from(">I", data, a + 20)[0]
                        ticks = struct.unpack_from(">Q", data, a + 24)[0]
                    else:
                        raise ValueError("Versión mvhd no soportada")
                    if not scale:
                        raise ValueError("Escala de tiempo inválida")
                    return ticks / scale
    raise ValueError(f"Falta duración MP4: {path.name}")

def allowed(path):
    relative = path.relative_to(ROOT)
    return (not path.is_symlink() and not any(p in BLOCKED for p in relative.parts)
            and path.name != ".DS_Store"
            and not (path.name.startswith(".env") and path.name != ".env.example")
            and path.suffix not in {".pyc", ".pyo"})

def selected(entries):
    result = set()
    for entry in entries:
        path = ROOT / entry
        if not path.exists():
            raise FileNotFoundError(entry)
        candidates = path.rglob("*") if path.is_dir() else [path]
        result.update(p for p in candidates if p.is_file() and allowed(p))
    return sorted(result)

def main():
    required = [
        "S07_S08_A1/decision_stack_frontend.md", "S07_S08_A1/revision_componentes.md",
        "S07_S08_A1/accesibilidad.md", "S07_S08_A2/capa_servicios.md",
        "frontend/package-lock.json", "frontend/.env.example", "frontend/src/main.tsx",
        "S07_S08_A2/evidencias/frontend_vitest.xml", "S07_S08_A2/evidencias/backend_pytest.xml",
        "S07_S08_A2/evidencias/postman_auth.txt",
    ]
    for file in required:
        if not (ROOT / file).is_file() or not (ROOT / file).stat().st_size:
            raise ValueError(f"Falta evidencia: {file}")
    videos = []
    for file, limit in [("S07_S08_A1/scaffolding.mp4", 20), ("S07_S08_A2/flujo_auth.mp4", 30), ("S07_S08_A2/flujo_e2e.mp4", 30)]:
        seconds = duration(ROOT / file)
        if not 0 < seconds <= limit:
            raise ValueError(f"{file}: {seconds} segundos; límite {limit}")
        videos.append({"archivo": file, "segundos": seconds, "limite": limit})
    common = ["frontend", "ENTREGAS_S07_S08.md"]
    packages = {
        "S07_S08_A1.zip": common + ["S07_S08_A1", "scripts/verificar_contraste.py"],
        "S07_S08_A2.zip": common + ["S07_S08_A2", "backend", "compose.yaml",
            "S05_S06_A1/openapi_equipo.yaml", "S05_S06_A1/esquema_bd.sql",
            "S05_S06_A1/insumos/comparacion_operaciones.json",
            "S05_S06_A2/evidencias/cobertura_operaciones.json",
            "postman/collections/S05-S06-A2-Autenticacion", "postman/environments/local-ejemplo.environment.yaml",
            "S07_S08_A1/decision_stack_frontend.md", "S07_S08_A1/revision_componentes.md",
            "S07_S08_A1/accesibilidad.md"],
    }
    OUT.mkdir(exist_ok=True)
    report = {"fecha": "2026-11-03", "videos": videos, "paquetes": []}
    for name, entries in packages.items():
        target = OUT / name
        paths = selected(entries)
        with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
            for path in paths:
                archive.write(path, path.relative_to(ROOT).as_posix())
        with zipfile.ZipFile(target) as archive:
            if archive.testzip() is not None:
                raise ValueError("ZIP dañado")
            names = archive.namelist()
            if any(".env" == Path(n).name or any(p in BLOCKED for p in Path(n).parts) for n in names):
                raise ValueError("Archivo privado dentro del ZIP")
        report["paquetes"].append({"archivo": name, "archivos": len(paths),
            "bytes": target.stat().st_size, "sha256": hashlib.sha256(target.read_bytes()).hexdigest()})
    (OUT / "verificacion_entregas.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
