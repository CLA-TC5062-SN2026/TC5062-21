"""Crea ZIP por actividad; requiere videos reales salvo --borrador."""
import argparse
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--borrador", action="store_true", help="Permite ZIP señalados como pendientes de video.")
args = parser.parse_args()
deliveries = {"S05_S06_A1": "pruebas_postman.mp4", "S05_S06_A2": "pruebas_auth.mp4"}
missing = [name + "/" + video for name, video in deliveries.items()
           if not (ROOT / name / video).is_file() or not (ROOT / name / video).stat().st_size]
issues = {name: "Falta " + video for name, video in deliveries.items() if name + "/" + video in missing}
if issues and not args.borrador:
    raise SystemExit("No se creó una entrega definitiva: " + "; ".join(name + ": " + reason for name, reason in issues.items()))
out = ROOT / "entregas"
out.mkdir(exist_ok=True)
for name, video in deliveries.items():
    pending = name in issues
    target = out / (name + ("_pendiente_video" if pending else "") + ".zip")
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for file in sorted((ROOT / name).rglob("*")):
            if file.is_file() and file.name != ".DS_Store":
                archive.write(file, file.relative_to(ROOT))
        if pending:
            archive.writestr(name + "/ESTADO_ENTREGA.txt", "BORRADOR: " + issues[name] + "\nIncorporar video corregido continuo de máximo 1 minuto antes de entregar en Canvas.\n")
    print(target.relative_to(ROOT))
print("Revisa duración <=60 s, continuidad y legibilidad de los videos antes de subir a Canvas.")
