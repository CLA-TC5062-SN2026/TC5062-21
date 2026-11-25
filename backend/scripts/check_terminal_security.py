"""Ejecuta curl real para los cuatro casos pedidos, sin volcar los tokens."""
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
results=[]
cases=[("sin_token",None,401),("firma_alterada","invalid.headers",401),
       ("rol_Consulta","consulta.headers",403),("rol_Administrador","admin.headers",201)]
for name,header,expected in cases:
    command=["curl","--silent","--show-error","--request","POST","http://127.0.0.1:8000/api/v1/capas",
             "--data-binary","@.local/protected_request.json","--write-out","\n%{http_code}"]
    command += ["--header","@.local/"+header] if header else ["--header","Content-Type: application/json"]
    result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,check=True)
    payload,status=result.stdout.rsplit("\n",1)
    status=int(status)
    assert status==expected,(name,status,payload)
    results.append({"caso":name,"metodo":"POST","ruta":"/api/v1/capas","esperado":expected,"observado":status,"respuesta":json.loads(payload)})
    print(f"{name}: HTTP {status} (esperado {expected})")
(ROOT/"S05_S06_A2/evidencias/pruebas_terminal.json").write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n")
