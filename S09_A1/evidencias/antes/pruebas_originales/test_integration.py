import copy
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from uuid import uuid4

import jwt
import pytest
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from backend.app.contract import METHODS, SPEC, validate
from backend.app.models import Bitacora, Sesion, Usuario, now


def headers(token):
    return {"Authorization": "Bearer " + token}


def login(api, email, password=None):
    r = api.post("/api/auth/login", json={"correo": email, "contrasena": password or api.test_password})
    assert r.status_code == 200, r.text
    return r.json()["accessToken"]


def test_all_46_operations_and_persistence(api, admin_token):
    """Todo éxito se valida contra su schema; el flujo cubre las 46 operaciones."""
    covered, records = set(), []
    token = admin_token
    def call(operation_id, params=None, body=None, query=None, expected=None):
        nonlocal token
        params = params or {}
        for path, item in SPEC["paths"].items():
            for method, op in item.items():
                if method in METHODS and op["operationId"] == operation_id:
                    route = "/api" + path
                    for key, value in params.items(): route = route.replace("{"+key+"}", value)
                    r = api.request(method.upper(), route, json=body, params=query, headers=headers(token))
                    code = expected or next(int(c) for c in op["responses"] if c.startswith("2"))
                    assert r.status_code == code, (operation_id, r.status_code, r.text)
                    schema = op["responses"][str(code)].get("content", {}).get("application/json", {}).get("schema")
                    if schema: validate(r.json(), schema)
                    if code == 201: assert "location" in r.headers
                    covered.add(operation_id)
                    records.append({"operacion": operation_id, "metodo": method.upper(), "ruta": route, "estado": code, "schema": "correcto"})
                    return r.json()
        raise AssertionError(operation_id)

    call("consultarSalud")
    registered = call("registrarUsuario", body={"correo": "alta@prueba.test", "nombre": "Alta ficticia", "contrasena": api.test_password})
    assert registered["rol"] == "Consulta"
    auth = call("autenticarUsuario", body={"correo": "administrador@prueba.test", "contrasena": api.test_password})
    token = auth["accessToken"]
    call("consultarPerfil")
    another = call("iniciarSesion", body={"correo": "administrador@prueba.test", "contrasena": api.test_password})
    call("consultarSesionActual")
    # Cierre de otra sesión no invalida la utilizada para el resto de la prueba.
    old = token; token = another["accessToken"]
    call("cerrarSesionActual"); token = old
    assert api.get("/api/auth/me", headers=headers(another["accessToken"])).status_code == 401
    call("listarUsuarios")
    layer = call("crearCapa", body={"nombre": " Capa de integración "})
    lid = layer["id"]
    call("listarCapas"); call("consultarCapa", {"capaId": lid})
    call("renombrarCapa", {"capaId": lid}, {"nombre": "Capa integrada"})
    user = call("crearUsuario", body={"correo": "editor-flujo@prueba.test", "nombre": "Editor de prueba", "contrasenaInicial": api.test_password, "rol": "Editor", "capasEditables": [lid]})
    up = {"usuarioId": user["id"]}
    call("consultarUsuario", up)
    call("consultarCapasEditables", up)
    call("reemplazarCapasEditables", up, {"capaIds": [lid]})
    call("actualizarUsuario", up, {"rol": "Editor"})
    call("restablecerContrasena", up, {"nuevaContrasena": "NuevaPassword21!"})
    tipo = call("crearTipoElemento", body={"nombre": "Proyecto", "capaId": lid})
    tid, base = tipo["id"], tipo["campos"][0]["id"]
    tp = {"tipoId": tid}
    call("listarTiposElemento", query={"capaId": lid})
    call("consultarTipoElemento", tp)
    call("renombrarTipoElemento", tp, {"nombre": "Proyecto integrado"})
    field = call("crearCampo", tp, {"nombre": "Estado", "tipoDato": "seleccion", "obligatorio": True, "opciones": [{"etiqueta": "Planeado", "orden": 0}]})
    fp = {**tp, "campoId": field["id"]}
    call("listarCampos", tp); call("consultarCampo", fp)
    field = call("reemplazarDefinicionCampo", fp, {"nombre": "Estado", "tipoDato": "seleccion", "obligatorio": True, "opciones": [{"etiqueta": "Planeado", "orden": 0}, {"etiqueta": "Activo", "orden": 1}]})
    option = field["opciones"][0]["id"]
    element = call("crearElemento", body={"tipoElementoId": tid, "valores": [{"campoId": base, "texto": "Proyecto Alfa"}, {"campoId": field["id"], "opcionId": option}]})
    ep = {"elementoId": element["id"]}
    call("listarElementos", query={"q": " alfa ", "capaId": lid})
    persisted = call("consultarElemento", ep)
    assert persisted["nombre"] == "Proyecto Alfa"
    call("modificarElemento", ep, {"valores": [{"campoId": base, "texto": "Proyecto Beta"}]})
    call("darBajaElemento", ep)
    assert api.get("/api/v1/elementos/"+element["id"], headers=headers(token)).status_code == 404
    call("modificarElemento", ep, {"estado": "activo"})
    dest_tipo = call("crearTipoElemento", body={"nombre": "Capacidad", "capaId": lid})
    dest = call("crearElemento", body={"tipoElementoId": dest_tipo["id"], "valores": [{"campoId": dest_tipo["campos"][0]["id"], "texto": "Capacidad ficticia"}]})
    kind = call("crearTipoRelacion", body={"nombre": "mejora", "descripcion": "Mejora una capacidad", "tipoOrigenId": tid, "tipoDestinoId": dest_tipo["id"]})
    kp = {"tipoRelacionId": kind["id"]}
    call("listarTiposRelacion"); call("consultarTipoRelacion", kp)
    call("modificarTipoRelacion", kp, {"descripcion": "Mejora una capacidad empresarial"})
    proposal = call("crearPropuesta", body={"operacion": "alta", "origenId": element["id"], "tipoRelacionId": kind["id"], "destinoId": dest["id"], "justificacion": "Justificación ficticia válida para mejorar la capacidad."})
    pp = {"propuestaId": proposal["id"]}
    call("listarPropuestas"); call("consultarPropuesta", pp)
    call("corregirPropuestaPendiente", pp, {"justificacion": "Justificación corregida para la capacidad ficticia."})
    decision = call("decidirPropuesta", pp, {"decision": "aprobar"})
    rid = decision["relacion"]["id"]
    call("listarRelaciones"); call("consultarRelacion", {"relacionId": rid})
    map_result = call("consultarMapa", ep)
    assert map_result["aristas"][0]["relacionId"] == rid
    call("listarBitacora")
    call("consultarEntradaBitacora", {"entradaId": decision["entradaBitacoraId"]})
    demo = {"muestraId": "arquitectura-ficticia-v1", "ficticia": True}
    first = call("cargarDemostracion", body=demo)
    second = call("cargarDemostracion", body=demo, expected=200)
    assert first["elementoIds"] == second["elementoIds"]
    expected_ops = {o["operationId"] for i in SPEC["paths"].values() for m,o in i.items() if m in METHODS}
    assert covered == expected_ops, expected_ops - covered
    from backend.tests.conftest import ROOT
    (ROOT/"S05_S06_A2/evidencias/cobertura_operaciones.json").write_text(json.dumps(records,ensure_ascii=False,indent=2)+"\n")


@pytest.mark.parametrize("path,method", [("/api"+p,m) for p,i in SPEC["paths"].items() for m,o in i.items()
    if m in METHODS and o.get("security", SPEC["security"])])
def test_every_protected_operation_rejects_absent_and_invalid_token(api, path, method):
    import re
    path = re.sub(r"\{[^}]+\}", str(uuid4()), path)
    for token in (None, "firma-invalida"):
        r = api.request(method.upper(), path, headers=headers(token) if token else {}, json={})
        assert r.status_code == 401, (path, method, r.text)
        assert r.headers["WWW-Authenticate"] == "Bearer"


def test_registration_security_and_bcrypt(api):
    email = "registro-" + uuid4().hex + "@prueba.test"
    payload = {"correo": email, "nombre": "Registro", "contrasena": api.test_password}
    r = api.post("/api/auth/register", json={**payload, "rol": "Administrador"})
    assert r.status_code == 422
    assert api.test_password not in r.text
    r = api.post("/api/auth/register", json=payload)
    assert r.status_code == 201
    assert r.json()["rol"] == "Consulta"
    assert not any(k in r.text.lower() for k in ("contrasena", "password", "hash"))
    assert api.post("/api/auth/register", json={**payload,"correo":email.upper()}).status_code == 409
    with Session(api.test_engine) as db:
        u = db.get(Usuario, r.json()["id"])
        assert u.hash_contrasena.startswith("$2b$12$")
        assert api.test_password != u.hash_contrasena
    assert api.post("/api/auth/register", json={**payload,"correo":"unicode@prueba.test","contrasena":"á"*40}).status_code == 422
    assert api.post("/api/auth/login", json={"correo":email,"contrasena":"incorrecta"}).status_code == 401


def test_roles_scope_and_input_errors(api, admin_token):
    consultation = login(api, "consulta@prueba.test")
    editor = login(api, "editor@prueba.test")
    assert api.post("/api/v1/capas", json={"nombre":"Prohibida"},headers=headers(consultation)).status_code == 403
    assert api.post("/api/v1/capas", json={"nombre":"Prohibida"},headers=headers(editor)).status_code == 403
    layer = api.get("/api/v1/capas",headers=headers(admin_token)).json()["items"][0]
    tipo = api.post("/api/v1/tipos-elemento",json={"nombre":"Restringido","capaId":layer["id"]},headers=headers(admin_token)).json()
    assert api.post("/api/v1/elementos",json={"tipoElementoId":tipo["id"],"valores":[{"campoId":tipo["campos"][0]["id"],"texto":"No autorizado"}]},headers=headers(editor)).status_code == 403
    assert api.get("/api/v1/elementos?q=%20%20",headers=headers(admin_token)).status_code == 422
    assert api.get("/api/v1/capas/no-es-uuid",headers=headers(admin_token)).status_code == 422
    assert api.get("/api/v1/capas/"+str(uuid4()),headers=headers(admin_token)).status_code == 404
    assert api.post("/api/v1/capas",content='{"nombre":',headers={**headers(admin_token),"Content-Type":"application/json"}).status_code == 400
    assert api.post("/api/v1/capas",content='nombre=Texto',headers={**headers(admin_token),"Content-Type":"text/plain"}).status_code == 415
    assert api.post("/api/v1/capas",json={"nombre":"Otro","invento":1},headers=headers(admin_token)).status_code == 422


def test_invalid_signed_tokens_expiration_inactivity_and_revocation(api, admin_token):
    from backend.app.main import settings
    claims = jwt.decode(admin_token,settings.jwt_secret,algorithms=["HS256"],audience=settings.jwt_audience)
    altered = admin_token.split(".")
    altered[2] = ("A" if altered[2][0] != "A" else "B")+altered[2][1:]
    variants = [".".join(altered)]
    for change in ({"exp":int(now().timestamp())-1},{"aud":"otro"},{"sub":"no-uuid"}):
        variants.append(jwt.encode({**claims,**change},settings.jwt_secret,algorithm="HS256"))
    no_exp=copy.deepcopy(claims);no_exp.pop("exp")
    variants += [jwt.encode(no_exp,settings.jwt_secret,algorithm="HS256"),jwt.encode(claims,settings.jwt_secret,algorithm="HS384")]
    for value in variants: assert api.get("/api/auth/me",headers=headers(value)).status_code == 401
    idle=login(api,"editor@prueba.test")
    sid=jwt.decode(idle,settings.jwt_secret,algorithms=["HS256"],audience=settings.jwt_audience)["sid"]
    with Session(api.test_engine) as db,db.begin(): db.get(Sesion,sid).ultima_actividad_en=now()-timedelta(minutes=31)
    assert api.get("/api/auth/me",headers=headers(idle)).status_code == 401
    first=login(api,"consulta@prueba.test");second=login(api,"consulta@prueba.test")
    assert api.delete("/api/v1/sesiones/actual",headers=headers(first)).status_code == 200
    assert api.get("/api/auth/me",headers=headers(first)).status_code == 401
    assert api.get("/api/auth/me",headers=headers(second)).status_code == 200


def test_role_change_revokes_every_session(api,admin_token):
    r=api.post("/api/v1/usuarios",headers=headers(admin_token),json={"correo":"revocar@prueba.test","nombre":"Revocar","contrasenaInicial":api.test_password,"rol":"Editor"})
    assert r.status_code==201
    t1=login(api,"revocar@prueba.test");t2=login(api,"revocar@prueba.test")
    assert api.patch('/api/v1/usuarios/'+r.json()['id'],headers=headers(admin_token),json={"rol":"Consulta"}).status_code==200
    for token in (t1,t2): assert api.get('/api/auth/me',headers=headers(token)).status_code==401
    assert api.get('/api/auth/me',headers=headers(login(api,'revocar@prueba.test'))).json()['rol']=='Consulta'


def test_concurrent_duplicate_registration(api):
    email='concurrente-'+uuid4().hex+'@prueba.test'
    def register(_): return api.post('/api/auth/register',json={"correo":email,"nombre":"Concurrente","contrasena":api.test_password}).status_code
    with ThreadPoolExecutor(max_workers=2) as pool: statuses=list(pool.map(register,range(2)))
    assert sorted(statuses)==[201,409]


def test_sql_bitacora_is_immutable(api):
    from sqlalchemy.exc import IntegrityError
    with Session(api.test_engine) as db:
        entry=db.scalar(select(Bitacora))
        assert entry
        with pytest.raises(IntegrityError):
            db.execute(text('UPDATE entradas_bitacora SET accion=:action WHERE id=:id'),{'action':'alterada','id':entry.id})
            db.commit()
        db.rollback()


def test_unicode_case_uniqueness_and_search(api, admin_token):
    r=api.post('/api/v1/capas',json={'nombre':'Árbol'},headers=headers(admin_token))
    assert r.status_code==201
    assert api.post('/api/v1/capas',json={'nombre':' árbol '},headers=headers(admin_token)).status_code==409
    t=api.post('/api/v1/tipos-elemento',json={'nombre':'Ámbito','capaId':r.json()['id']},headers=headers(admin_token)).json()
    e=api.post('/api/v1/elementos',json={'tipoElementoId':t['id'],'valores':[{'campoId':t['campos'][0]['id'],'texto':'ÁRBOL empresarial'}]},headers=headers(admin_token))
    assert e.status_code==201
    found=api.get('/api/v1/elementos',params={'q':'árbol'},headers=headers(admin_token)).json()
    assert e.json()['id'] in [x['id'] for x in found['items']]
    without_accent=api.get('/api/v1/elementos',params={'q':'arbol'},headers=headers(admin_token)).json()
    assert e.json()['id'] not in [x['id'] for x in without_accent['items']]
