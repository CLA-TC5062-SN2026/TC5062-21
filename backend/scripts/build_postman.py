"""Flujos ejecutables en v3 y exportaciones v2.1 para importar en Postman Desktop."""
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
POSTMAN = ROOT / "postman"


class BlockDumper(yaml.SafeDumper):
    pass


def string(dumper, value):
    return dumper.represent_scalar('tag:yaml.org,2002:str', value, style='|' if '\n' in value else None)


BlockDumper.add_representer(str, string)


def dump(value, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(yaml.dump(value, Dumper=BlockDumper, sort_keys=False, allow_unicode=True, width=110))


def request(name, method, path, body=None, expected=200, token=None, script=""):
    code = f'pm.test("HTTP {expected}", () => pm.response.to.have.status({expected}));\n'
    code += 'pm.test("Respuesta JSON", () => pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json"));\n'
    code += 'pm.test("Sin secretos de almacenamiento", () => { const text = pm.response.text(); pm.expect(text).not.to.include("hashContrasena"); pm.expect(text).not.to.include("hash_contrasena"); });\n'
    code += script
    headers = []
    if token: headers.append({"key":"Authorization", "value":"Bearer {{"+token+"}}"})
    item = {"$kind":"http-request", "name":name, "method":method, "url":"{{baseUrl}}"+path,
        "headers":headers, "auth":{"type":"noauth"},
        "scripts":[{"type":"afterResponse", "language":"text/javascript", "code":code}]}
    if body is not None:
        item["headers"].append({"key":"Content-Type", "value":"application/json"})
        item["body"] = {"type":"json", "content":json.dumps(body,ensure_ascii=False,indent=2)}
    return item


def save(name, items, target, base_url):
    folder = POSTMAN / "collections" / name
    vars = [{"key":"baseUrl", "value":base_url}, {"key":"runId", "value":"{{$timestamp}}"}]
    dump({"$kind":"collection", "name":name, "variables":vars}, folder/".resources/definition.yaml")
    exported = {"info":{"name":name,"schema":"https://schema.getpostman.com/json/collection/v2.1.0/collection.json"},
        "variable":vars, "item":[]}
    for i,item in enumerate(items,1):
        item["order"] = i*1000
        dump(item,folder/f"{i:02d}-{item['name'].split(' ',1)[-1].replace(' ','-')}.request.yaml")
        request_v2 = {"method":item["method"],"url":item["url"],"header":item["headers"],"auth":{"type":"noauth"}}
        if "body" in item:
            request_v2["body"]={"mode":"raw","raw":item["body"]["content"],"options":{"raw":{"language":"json"}}}
        exported["item"].append({"name":item["name"],"request":request_v2,
            "event":[{"listen":"test","script":{"type":"text/javascript","exec":item["scripts"][0]["code"].splitlines()}}]})
    target.write_text(json.dumps(exported,ensure_ascii=False,indent=2)+"\n")


def build():
    crud = [
        request("01 Crear capa", "POST", "/v1/capas", {"nombre":"Capa Postman {{runId}}"}, 201,
                script='pm.collectionVariables.set("capaId", pm.response.json().id);\n'),
        request("02 Recuperar capa persistida", "GET", "/v1/capas/{{capaId}}", script='pm.test("Persistencia de capa", () => pm.expect(pm.response.json().id).to.eql(pm.collectionVariables.get("capaId")));\n'),
        request("03 Crear tipo con campo Nombre", "POST", "/v1/tipos-elemento", {"nombre":"Proyecto de video", "capaId":"{{capaId}}"}, 201,
                script='const t = pm.response.json(); pm.collectionVariables.set("tipoId",t.id); pm.collectionVariables.set("campoNombreId",t.campos.find(c => c.esBaseNombre).id);\n'),
        request("04 Crear elemento", "POST", "/v1/elementos", {"tipoElementoId":"{{tipoId}}","valores":[{"campoId":"{{campoNombreId}}","texto":"Proyecto ficticio"}]}, 201,
                script='pm.collectionVariables.set("elementoId",pm.response.json().id);\n'),
        request("05 Recuperar elemento persistido", "GET", "/v1/elementos/{{elementoId}}", script='pm.test("Persistencia de valores", () => pm.expect(pm.response.json().nombre).to.eql("Proyecto ficticio"));\n'),
        request("06 Baja lógica del elemento", "DELETE", "/v1/elementos/{{elementoId}}", script='pm.test("Baja conservadora", () => pm.expect(pm.response.json().estado).to.eql("baja"));\n'),
    ]
    save("S05-S06-A1-CRUD",crud,ROOT/"S05_S06_A1/coleccion_crud.postman_collection.json","http://127.0.0.1:8001/api")
    auth = [
        request("01 Registro Consulta", "POST", "/auth/register", {"correo":"registro{{runId}}@equipo21.test","nombre":"Registro ficticio","contrasena":"{{demoPassword}}"},201,
            script='pm.test("Sin contraseña", () => { pm.expect(pm.response.json()).not.to.have.property("contrasena"); pm.expect(pm.response.json().rol).to.eql("Consulta"); });\n'),
        request("02 Login Administrador ficticio", "POST", "/auth/login", {"correo":"{{adminEmail}}","contrasena":"{{demoPassword}}"},200,
            script='pm.test("JWT presente", () => pm.expect(pm.response.json().accessToken.split(".")).to.have.lengthOf(3)); pm.collectionVariables.set("adminToken",pm.response.json().accessToken);\n'),
        request("03 Perfil del token anterior", "GET", "/auth/me", token="adminToken",
            script='pm.test("Identidad y rol", () => { pm.expect(pm.response.json().correo).to.eql(pm.variables.get("adminEmail")); pm.expect(pm.response.json().rol).to.eql("Administrador"); });\n'),
        request("04 CRUD con token y rol correctos", "POST", "/v1/capas", {"nombre":"Capa autenticada {{runId}}"},201,token="adminToken"),
        request("05 Misma ruta sin token", "POST", "/v1/capas", {"nombre":"Rechazo sin token"},401,
            script='pm.test("Desafío Bearer", () => pm.expect(pm.response.headers.get("WWW-Authenticate")).to.eql("Bearer"));\n'),
        request("06 Misma ruta con rol incorrecto", "POST", "/v1/capas", {"nombre":"Rechazo por rol"},403,token="consultaToken"),
    ]
    save("S05-S06-A2-Autenticacion",auth,ROOT/"S05_S06_A2/coleccion_auth.postman_collection.json","http://127.0.0.1:8000/api")
    # Una colección adicional ejercita el caso de firma alterada exigido en terminal.
    negative = [request("Firma invalida", "GET", "/v1/capas", expected=401, token="invalidToken")]
    save("S05-S06-A2-Firma",negative,ROOT/"S05_S06_A2/coleccion_firma.postman_collection.json","http://127.0.0.1:8000/api")
    env = {"name":"Equipo21-local-ejemplo","values":[
        {"key":"adminEmail","value":"admin@equipo21.test","enabled":True,"type":"default"},
        *[{"key":key,"value":"","enabled":True,"type":"secret"} for key in ("demoPassword","consultaToken","invalidToken")]]}
    dump(env, POSTMAN/"environments/local-ejemplo.environment.yaml")
    (ROOT/"S05_S06_A2/entorno_ejemplo.postman_environment.json").write_text(json.dumps(env,ensure_ascii=False,indent=2)+"\n")
    print("Colecciones v3 y exportaciones Desktop preparadas sin credenciales.")


if __name__ == "__main__": build()
