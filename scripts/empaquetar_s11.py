"""Prepara el ZIP de Canvas; --final exige un video válido o un enlace HTTPS real."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--final', action='store_true', help='Rechazar una entrega sin video o enlace.')
args = parser.parse_args()
folder = ROOT / 'S11_A1'
required = [ROOT / 'README.md', folder / 'matriz_trazabilidad.md', folder / 'retrospectiva_proyecto.md']
for path in required:
    if not path.is_file():
        raise SystemExit('Falta ' + str(path.relative_to(ROOT)))
video = folder / 'demo_proyecto.mp4'
link = folder / 'demo_link.txt'
if link.exists() and not link.read_text().strip().startswith('https://'):
    raise SystemExit('demo_link.txt debe contener el enlace HTTPS real del video compartido.')
if video.exists():
    if video.stat().st_size >= 100_000_000:
        raise SystemExit('El video supera el umbral de 100 MB. Compártelo y usa demo_link.txt.')
    probe = shutil.which('ffprobe')
    if not probe:
        raise SystemExit('Se necesita ffprobe para verificar que el video dura como máximo 300 s.')
    result = subprocess.run([probe, '-v', 'error', '-show_entries', 'format=duration:stream=codec_type',
                             '-of', 'json', str(video)], check=True, capture_output=True, text=True)
    info = json.loads(result.stdout)
    duration = float(info['format']['duration'])
    if duration <= 0 or duration > 300:
        raise SystemExit('Duración fuera del límite: ' + str(duration) + ' segundos.')
    if not {'audio', 'video'} <= {stream['codec_type'] for stream in info['streams']}:
        raise SystemExit('El video debe incluir imagen y audio. Revisen además la claridad y la narración.')
if args.final and not video.exists() and not link.exists():
    raise SystemExit('Entrega incompleta: falta demo_proyecto.mp4 o demo_link.txt con el video del equipo.')
label = 'final' if args.final else 'preparacion'
output = ROOT / 'entregas' / ('S11_A1_Equipo21_' + label + '.zip')
output.parent.mkdir(exist_ok=True)
paths = [ROOT / 'README.md', *folder.rglob('*')]
# Fuentes exigidas por la consigna, útiles para contrastar la matriz dentro del ZIP.
paths.extend(ROOT / name for name in ['S03_A1/SRS_equipo.md', 'S03_A1/backlog_completo.md',
                                      'S05_S06_A1/openapi_equipo.yaml', 'S09_A1/code_review.md'])
with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(set(paths)):
        if path.is_file() and '__pycache__' not in path.parts and not path.name.startswith('.'):
            archive.write(path, path.relative_to(ROOT))
with zipfile.ZipFile(output) as archive:
    assert archive.testzip() is None
print(output)
print('SHA256: ' + hashlib.sha256(output.read_bytes()).hexdigest())
if not args.final:
    print('ZIP de preparación: aún no acredita la entrega final. Añadan el video del equipo y ejecuten --final.')
