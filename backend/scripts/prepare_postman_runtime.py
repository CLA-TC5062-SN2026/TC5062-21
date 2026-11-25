"""Prepara variables de cuentas ficticias SOLO en .local; nunca imprime contraseñas/JWT."""
import json
from pathlib import Path
from uuid import uuid4

import httpx
import yaml

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / ".local"
credentials = json.loads((LOCAL / "demo_credentials.json").read_text())
with httpx.Client(base_url="http://127.0.0.1:8000") as client:
    response = client.post("/api/auth/login", json={"correo": credentials["consulta"], "contrasena": credentials["password"]})
    response.raise_for_status()
    consulta = response.json()["accessToken"]
    response = client.post("/api/auth/login", json={"correo": credentials["admin"], "contrasena": credentials["password"]})
    response.raise_for_status()
    admin = response.json()["accessToken"]
parts = consulta.split(".")
parts[2] = ("A" if parts[2][0] != "A" else "B") + parts[2][1:]
invalid = ".".join(parts)
environment = {"name": "Equipo21-local-privado", "values": [
    {"key": key, "value": value, "enabled": True, "type": kind}
    for key, value, kind in (("adminEmail",credentials["admin"],"default"),
        ("demoPassword",credentials["password"],"secret"),("consultaToken",consulta,"secret"),
        ("invalidToken",invalid,"secret"),("runId",uuid4().hex[:12],"default"))]}
for name,content in (("postman.environment.yaml",yaml.safe_dump(environment,sort_keys=False)),
                     ("desktop.postman_environment.json",json.dumps(environment,ensure_ascii=False,indent=2)+"\n"),
                     ("admin.headers","Authorization: Bearer "+admin+"\nContent-Type: application/json\n"),
                     ("consulta.headers","Authorization: Bearer "+consulta+"\nContent-Type: application/json\n"),
                     ("invalid.headers","Authorization: Bearer "+invalid+"\nContent-Type: application/json\n"),
                     ("protected_request.json",json.dumps({"nombre":"Terminal "+uuid4().hex[:10]}))):
    path=LOCAL/name
    path.write_text(content)
    path.chmod(0o600)
print("Variables locales de demostración listas; los archivos compartibles continúan sin credenciales.")
