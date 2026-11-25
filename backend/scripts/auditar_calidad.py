"""Guarda la salida íntegra de Pylint y datos reproducibles de la auditoría."""
import argparse
import ast
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def main():
    """Analiza únicamente el código de producto en backend/app, sin ocultar mensajes."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=ROOT / "S09_A1/evidencias/reproduccion")
    args = parser.parse_args()
    destination = args.output.resolve()
    destination.mkdir(parents=True, exist_ok=True)
    files = sorted(ROOT.glob("backend/app/*.py"))
    command = [sys.executable, "-m", "pylint", "--rcfile=backend/pylintrc",
               f"--output-format=text,json2:{os.path.relpath(destination / 'pylint.json', ROOT)}",
               *[str(path.relative_to(ROOT)) for path in files]]
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True,
                            check=False)
    (destination / "output_linter.txt").write_text(result.stdout + result.stderr,
                                                 encoding="utf-8")
    report = json.loads((destination / "pylint.json").read_text(encoding="utf-8"))
    source_dir = destination / "codigo"
    source_dir.mkdir(exist_ok=True)
    sizes, hashes, functions = {}, {}, []
    for path in files:
        source = path.read_text(encoding="utf-8")
        relative = str(path.relative_to(ROOT))
        sizes[relative] = len(source.splitlines())
        hashes[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        shutil.copy2(path, source_dir / path.name)
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append({"archivo": relative, "nombre": node.name,
                                  "linea": node.lineno,
                                  "lineas_fisicas": node.end_lineno-node.lineno+1})
    metadata = {
        "fecha_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "pylint": subprocess.check_output(
            [sys.executable, "-m", "pylint", "--version"], text=True).strip(),
        "comando": [".venv/bin/python", *command[1:3], "--rcfile=backend/pylintrc",
                    "--output-format=text,json2:<salida>/pylint.json", *command[5:]],
        "codigo_salida": result.returncode,
        "commit_base_local": (subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
            if (ROOT / ".git").exists() else None),
        "sha256_fuentes": hashes,
        "lineas_fisicas": sizes,
        "total_mensajes": len(report["messages"]),
        "por_simbolo": dict(Counter(item["symbol"] for item in report["messages"])),
        "por_tipo_pylint": dict(Counter(item["type"] for item in report["messages"])),
        "estadisticas_pylint": report["statistics"],
        "funciones": functions,
    }
    (destination / "ejecucion.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(f"Pylint: {metadata['total_mensajes']} mensajes; salida {result.returncode}.")
    print(f"Evidencia: {destination}")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
