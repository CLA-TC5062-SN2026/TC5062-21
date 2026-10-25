"""Casos de uso. La transacción y el bloqueo de escrituras los provee el middleware."""
from datetime import date
from math import isfinite

from sqlalchemy import delete, func, or_, select, update

from .errors import APIError, invalid
from .models import (Bitacora, Campo, Capa, CargaDemostracion, Decision, Elemento,
    Opcion, Permiso, Propuesta, Relacion, Sesion, TipoElemento, TipoRelacion, Usuario,
    Valor, now, uid)
from .security import (DUMMY_HASH, correo_normalizado, hash_password, issue_token,
                       unauthorized, verify_password)


def clean(value, field="nombre", maximum=120):
    value = value.strip()
    if not value or len(value) > maximum:
        invalid(f"{field} debe tener entre 1 y {maximum} caracteres sin espacios extremos.", field)
    return value


def iso(value):
    return value.isoformat() if value else None


class Service:
    def __init__(self, db, user, session, settings):
        self.db, self.user, self.session, self.settings = db, user, session, settings

    def get(self, model, ident):
        obj = self.db.get(model, ident)
        if obj is None: raise APIError(404, "NO_ENCONTRADO", "El recurso no existe.")
        return obj

    def all(self, model, *conditions, order=None):
        stmt = select(model).where(*conditions)
        return list(self.db.scalars(stmt.order_by(order if order is not None else model.id)))

    def add(self, model, **attrs):
        obj = model(**attrs)
        self.db.add(obj)
        self.db.flush()
        return obj

    def audit(self, obj, action, after=None, before=None):
        entry = self.add(Bitacora, actor_id=self.user.id, tipo_objeto=obj.__class__.__name__,
            objeto_id=obj.id, accion=action, valores_antes=before, valores_despues=after)
        return entry.id

    def layers(self, user):
        return list(self.db.scalars(select(Permiso.capa_id).where(Permiso.usuario_id == user.id).order_by(Permiso.capa_id)))

    def may_edit(self, layer_id):
        if self.user.rol == "Administrador": return
        if self.user.rol != "Editor" or layer_id not in self.layers(self.user):
            raise APIError(403, "SIN_PERMISO", "No tiene permiso de edición sobre esta capa.")

    def user_json(self, u):
        return {"id": u.id, "correo": u.correo, "nombre": u.nombre, "rol": u.rol,
                "activo": u.activo, "capasEditables": self.layers(u)}

    def capa_json(self, c):
        return {"id": c.id, "nombre": c.nombre}

    def campo_json(self, c):
        return {"id": c.id, "tipoElementoId": c.tipo_elemento_id, "nombre": c.nombre,
            "tipoDato": c.tipo_dato, "obligatorio": c.obligatorio, "esBaseNombre": c.es_base_nombre,
            "opciones": [{"id": o.id, "etiqueta": o.etiqueta, "orden": o.orden}
                for o in self.all(Opcion, Opcion.campo_id == c.id, Opcion.activa.is_(True), order=Opcion.orden)]}

    def fields(self, tipo_id):
        return self.all(Campo, Campo.tipo_elemento_id == tipo_id)

    def tipo_json(self, t):
        return {"id": t.id, "nombre": t.nombre, "capaId": t.capa_id,
            "estructuraBloqueada": bool(self.db.scalar(select(Elemento.id).where(Elemento.tipo_elemento_id == t.id).limit(1))),
            "campos": [self.campo_json(c) for c in self.fields(t.id)]}

    def autoria(self, e):
        return {"creadorId": e.creador_id, "creadoEn": iso(e.creado_en),
            "ultimoModificadorId": e.ultimo_modificador_id, "modificadoEn": iso(e.modificado_en)}

    def summary(self, e):
        t = self.get(TipoElemento, e.tipo_elemento_id)
        return {"id": e.id, "nombre": e.nombre, "tipoElemento": {"id": t.id, "nombre": t.nombre},
            "capa": self.capa_json(self.get(Capa, t.capa_id)), "estado": e.estado}

    def values(self, e):
        output = []
        for v in self.all(Valor, Valor.elemento_id == e.id, order=Valor.campo_id):
            item = {"campoId": v.campo_id}
            for attr, key in (("texto", "texto"), ("numero", "numero"), ("fecha", "fecha"), ("opcion_id", "opcionId")):
                value = getattr(v, attr)
                if value is not None: item[key] = iso(value) if attr == "fecha" else value
            output.append(item)
        return output

    def elemento_json(self, e):
        return {**self.summary(e), "campos": [self.campo_json(c) for c in self.fields(e.tipo_elemento_id)],
                "valores": self.values(e), "autoria": self.autoria(e)}

    def tipo_rel_json(self, t):
        return {"id": t.id, "nombre": t.nombre, "descripcion": t.descripcion,
                "tipoOrigenId": t.tipo_origen_id, "tipoDestinoId": t.tipo_destino_id}

    def relacion_json(self, r):
        return {"id": r.id, "origen": self.summary(self.get(Elemento, r.origen_id)),
            "tipoRelacion": self.tipo_rel_json(self.get(TipoRelacion, r.tipo_relacion_id)),
            "destino": self.summary(self.get(Elemento, r.destino_id)), "justificacion": r.justificacion,
            "estado": r.estado, "version": r.version, "autoria": self.autoria(r)}

    def propuesta_json(self, p):
        decision = self.db.scalar(select(Decision).where(Decision.propuesta_id == p.id))
        return {"id": p.id, "operacion": p.operacion, "estado": p.estado, "origenId": p.origen_id,
            "tipoRelacionId": p.tipo_relacion_id, "destinoId": p.destino_id, "justificacion": p.justificacion,
            "estadoSolicitado": p.estado_solicitado, "relacionId": p.relacion_id,
            "relacionResultadoId": p.relacion_resultado_id, "versionBase": p.version_base,
            "autorId": p.autor_id, "creadaEn": iso(p.creada_en),
            "decisorId": decision.decisor_id if decision else None,
            "decididaEn": iso(decision.decidida_en) if decision else None}

    def audit_json(self, b):
        return {"id": b.id, "actorId": b.actor_id, "fecha": iso(b.fecha), "tipoObjeto": b.tipo_objeto,
            "objetoId": b.objeto_id, "accion": b.accion, "valoresAntes": b.valores_antes, "valoresDespues": b.valores_despues}

    def listing(self, values, serializer, q=None, paginated=False):
        result = {"items": [serializer(v) for v in values], "total": len(values)}
        if paginated:
            page = (q or {}).get("pagina", 1)
            result["items"] = result["items"][(page-1)*25:page*25]
            result.update(pagina=page, tamanoPagina=25)
        return result

    def touch(self, obj):
        obj.ultimo_modificador_id = self.user.id
        obj.modificado_en = now()
        self.db.flush()

    def revoke(self, user):
        self.db.execute(update(Sesion).where(Sesion.usuario_id == user.id, Sesion.revocada_en.is_(None)).values(revocada_en=now()))

    def dispatch(self, operation, p, q, b):
        return getattr(self, operation)(p, q, b)

    def consultarSalud(self, p, q, b):
        self.db.execute(select(1))
        return {"estado": "ok"}

    def registrarUsuario(self, p, q, b):
        u = self.add(Usuario, correo=correo_normalizado(b["correo"]), nombre=clean(b["nombre"]),
            hash_contrasena=hash_password(b["contrasena"]), rol="Consulta", activo=True)
        self.user = u
        result = self.user_json(u)
        self.audit(u, "registro", result)
        return result

    def autenticarUsuario(self, p, q, b):
        email = correo_normalizado(b["correo"])
        u = self.db.scalar(select(Usuario).where(Usuario.correo == email))
        correct = verify_password(b["contrasena"], u.hash_contrasena if u else DUMMY_HASH)
        if not u or not correct or not u.activo: unauthorized()
        token, session = issue_token(self.db, u, self.settings)
        return {"accessToken": token, "tokenType": "Bearer", "expiresIn": self.settings.jwt_expiration,
                "expiraEn": iso(session.expira_en), "usuario": self.user_json(u), "sesionId": session.id}

    iniciarSesion = autenticarUsuario

    def consultarPerfil(self, p, q, b):
        return self.user_json(self.user)

    def consultarSesionActual(self, p, q, b):
        s = self.session
        return {"id": s.id, "usuario": self.user_json(self.user), "creadaEn": iso(s.creada_en),
                "ultimaActividadEn": iso(s.ultima_actividad_en), "expiraEn": iso(s.expira_en)}

    def cerrarSesionActual(self, p, q, b):
        self.session.revocada_en = now()
        return {"mensaje": "Sesión cerrada."}

    def listarUsuarios(self, p, q, b):
        return self.listing(self.all(Usuario, order=Usuario.correo), self.user_json, q, True)

    def consultarUsuario(self, p, q, b):
        return self.user_json(self.get(Usuario, p["usuarioId"]))

    def assign_layers(self, u, ids):
        if u.rol != "Editor" and ids: invalid("Solo Editor puede tener capas asignadas.", "capaIds")
        for ident in ids: self.get(Capa, ident)
        # Las asignaciones actuales se reemplazan; su historial permanece en bitácora.
        self.db.execute(delete(Permiso).where(Permiso.usuario_id == u.id))
        for ident in ids:
            self.add(Permiso, usuario_id=u.id, capa_id=ident, asignado_por=self.user.id)

    def crearUsuario(self, p, q, b):
        u = self.add(Usuario, correo=correo_normalizado(b["correo"]), nombre=clean(b["nombre"]),
            hash_contrasena=hash_password(b["contrasenaInicial"]), rol=b["rol"], activo=True)
        self.assign_layers(u, b.get("capasEditables", []))
        result = self.user_json(u)
        self.audit(u, "alta", result)
        return result

    def actualizarUsuario(self, p, q, b):
        u = self.get(Usuario, p["usuarioId"])
        before = self.user_json(u)
        role, active = b.get("rol", u.rol), b.get("activo", u.activo)
        if u.activo and u.rol == "Administrador" and (role != "Administrador" or not active):
            admins = self.db.scalar(select(func.count()).select_from(Usuario).where(Usuario.activo.is_(True), Usuario.rol == "Administrador"))
            if admins <= 1: raise APIError(409, "ULTIMO_ADMINISTRADOR", "Debe conservarse un administrador activo.")
        if role != u.rol or active != u.activo:
            u.rol, u.activo = role, active
            if role != "Editor": self.assign_layers(u, [])
            self.revoke(u)
            self.db.flush()
            self.audit(u, "cambio_acceso", self.user_json(u), before)
        return self.user_json(u)

    def restablecerContrasena(self, p, q, b):
        u = self.get(Usuario, p["usuarioId"])
        u.hash_contrasena = hash_password(b["nuevaContrasena"])
        self.revoke(u)
        entry_id = self.audit(u, "restablecimiento", {"sesionesRevocadas": True})
        return self.audit_json(self.get(Bitacora, entry_id))

    def consultarCapasEditables(self, p, q, b):
        return {"capaIds": self.layers(self.get(Usuario, p["usuarioId"]))}

    def reemplazarCapasEditables(self, p, q, b):
        u = self.get(Usuario, p["usuarioId"])
        before = {"capaIds": self.layers(u)}
        self.assign_layers(u, b["capaIds"])
        result = {"capaIds": self.layers(u)}
        if before != result: self.audit(u, "asignar_capas", result, before)
        return result

    def listarCapas(self, p, q, b):
        return self.listing(self.all(Capa), self.capa_json)

    def crearCapa(self, p, q, b):
        c = self.add(Capa, nombre=clean(b["nombre"]))
        result = self.capa_json(c)
        self.audit(c, "alta", result)
        return result

    def consultarCapa(self, p, q, b):
        return self.capa_json(self.get(Capa, p["capaId"]))

    def renombrarCapa(self, p, q, b):
        c = self.get(Capa, p["capaId"])
        before = self.capa_json(c)
        c.nombre = clean(b["nombre"])
        self.db.flush()
        if before != self.capa_json(c): self.audit(c, "renombrar", self.capa_json(c), before)
        return self.capa_json(c)

    def listarTiposElemento(self, p, q, b):
        conditions = []
        if q.get("capaId"):
            self.get(Capa, q["capaId"])
            conditions.append(TipoElemento.capa_id == q["capaId"])
        return self.listing(self.all(TipoElemento, *conditions), self.tipo_json)

    def crearTipoElemento(self, p, q, b):
        self.get(Capa, b["capaId"])
        t = self.add(TipoElemento, nombre=clean(b["nombre"]), capa_id=b["capaId"])
        self.add(Campo, tipo_elemento_id=t.id, nombre="Nombre", tipo_dato="texto", obligatorio=True, es_base_nombre=True)
        result = self.tipo_json(t)
        self.audit(t, "alta", result)
        return result

    def consultarTipoElemento(self, p, q, b):
        return self.tipo_json(self.get(TipoElemento, p["tipoId"]))

    def renombrarTipoElemento(self, p, q, b):
        t = self.get(TipoElemento, p["tipoId"])
        before = self.tipo_json(t)
        t.nombre = clean(b["nombre"])
        self.db.flush()
        if before != self.tipo_json(t): self.audit(t, "renombrar", self.tipo_json(t), before)
        return self.tipo_json(t)

    def listarCampos(self, p, q, b):
        self.get(TipoElemento, p["tipoId"])
        return self.listing(self.fields(p["tipoId"]), self.campo_json)

    def consultarCampo(self, p, q, b):
        c = self.get(Campo, p["campoId"])
        if c.tipo_elemento_id != p["tipoId"]: raise APIError(404, "NO_ENCONTRADO", "El campo no pertenece al tipo.")
        return self.campo_json(c)

    def ensure_unlocked(self, tipo_id):
        self.get(TipoElemento, tipo_id)
        if self.db.scalar(select(Elemento.id).where(Elemento.tipo_elemento_id == tipo_id).limit(1)):
            raise APIError(409, "ESTRUCTURA_BLOQUEADA", "El tipo ya tiene elementos; su estructura está bloqueada.")

    def write_field(self, c, b):
        name = clean(b["nombre"])
        if name.lower() == "nombre" and not c.es_base_nombre: raise APIError(409, "NOMBRE_RESERVADO", "Nombre es un campo base reservado.")
        if b["tipoDato"] == "seleccion" and not b["opciones"]: invalid("Selección requiere opciones.", "opciones")
        if b["tipoDato"] != "seleccion" and b["opciones"]: invalid("Solo selección permite opciones.", "opciones")
        labels = [clean(o["etiqueta"]).lower() for o in b["opciones"]]
        orders = [o["orden"] for o in b["opciones"]]
        if len(set(labels)) != len(labels) or len(set(orders)) != len(orders): invalid("Opciones con etiquetas u órdenes duplicados.", "opciones")
        c.nombre, c.tipo_dato, c.obligatorio = name, b["tipoDato"], b["obligatorio"]
        existing = self.all(Opcion, Opcion.campo_id == c.id)
        for option in existing: option.activa = False
        self.db.flush()
        for item in b["opciones"]:
            label = clean(item["etiqueta"])
            option = next((o for o in existing if o.etiqueta.lower() == label.lower()), None)
            if option:
                option.etiqueta, option.orden, option.activa = label, item["orden"], True
            else: self.add(Opcion, campo_id=c.id, etiqueta=label, orden=item["orden"], activa=True)
        self.db.flush()

    def crearCampo(self, p, q, b):
        self.ensure_unlocked(p["tipoId"])
        # Validar antes del primer INSERT también evita insertar opciones inválidas.
        if clean(b["nombre"]).lower() == "nombre": raise APIError(409, "NOMBRE_RESERVADO", "El campo base Nombre ya existe.")
        c = self.add(Campo, tipo_elemento_id=p["tipoId"], nombre=clean(b["nombre"]), tipo_dato=b["tipoDato"], obligatorio=b["obligatorio"], es_base_nombre=False)
        self.write_field(c, b)
        result = self.campo_json(c)
        self.audit(c, "alta", result)
        return result

    def reemplazarDefinicionCampo(self, p, q, b):
        c = self.get(Campo, p["campoId"])
        if c.tipo_elemento_id != p["tipoId"]: raise APIError(404, "NO_ENCONTRADO", "El campo no pertenece al tipo.")
        self.ensure_unlocked(p["tipoId"])
        before = self.campo_json(c)
        if c.es_base_nombre:
            if b != {"nombre": "Nombre", "tipoDato": "texto", "obligatorio": True, "opciones": []}:
                raise APIError(409, "CAMPO_BASE", "El campo base Nombre es inmutable.")
            return before
        self.write_field(c, b)
        result = self.campo_json(c)
        if before != result: self.audit(c, "reemplazar", result, before)
        return result

    def write_values(self, e, entries, creating=False):
        fields = {c.id: c for c in self.fields(e.tipo_elemento_id)}
        ids = [item["campoId"] for item in entries]
        if len(set(ids)) != len(ids): invalid("No se permiten campos repetidos.", "valores")
        for item in entries:
            c = fields.get(item["campoId"])
            if not c: invalid("El campo no pertenece al tipo.", "valores")
            old = self.db.scalar(select(Valor).where(Valor.elemento_id == e.id, Valor.campo_id == c.id))
            if item.get("vaciar"):
                if c.obligatorio: invalid("No se puede vaciar un campo obligatorio.", "valores")
                if old: self.db.delete(old)
                continue
            key = {"texto": "texto", "numero": "numero", "fecha": "fecha", "seleccion": "opcionId"}[c.tipo_dato]
            if key not in item: invalid("El valor no corresponde al tipo de campo.", "valores")
            value = item[key]
            if key == "texto":
                if c.obligatorio and not value.strip(): invalid("Un texto obligatorio no puede estar vacío.", "valores")
                if c.es_base_nombre: value = clean(value, "Nombre", 500); e.nombre = value
            if key == "numero" and not isfinite(value): invalid("El número debe ser finito.", "valores")
            if key == "fecha":
                try: value = date.fromisoformat(value)
                except ValueError: invalid("La fecha no es válida.", "valores")
            if key == "opcionId":
                option = self.get(Opcion, value)
                if option.campo_id != c.id or not option.activa: invalid("La opción no pertenece al campo.", "valores")
            row = old or Valor(elemento_id=e.id, campo_id=c.id)
            for attr in ("texto", "numero", "fecha", "opcion_id"): setattr(row, attr, None)
            setattr(row, "opcion_id" if key == "opcionId" else key, value)
            self.db.add(row)
        self.db.flush()
        present = set(self.db.scalars(select(Valor.campo_id).where(Valor.elemento_id == e.id)))
        for c in fields.values():
            if c.obligatorio and c.id not in present: invalid(f"Falta el campo obligatorio {c.nombre}.", "valores")

    def listarElementos(self, p, q, b):
        conditions = []
        if not q.get("incluirBaja", False): conditions.append(Elemento.estado == "activo")
        if "q" in q:
            value = clean(q["q"], "q", 500).lower()
            # contains(autoescape) trata % y _ como texto, no como comodines SQL.
            conditions.append(func.lower(Elemento.nombre).contains(value, autoescape=True))
        if q.get("tipoElementoId"):
            self.get(TipoElemento, q["tipoElementoId"])
            conditions.append(Elemento.tipo_elemento_id == q["tipoElementoId"])
        if q.get("capaId"):
            self.get(Capa, q["capaId"])
            conditions.append(Elemento.tipo_elemento_id.in_(select(TipoElemento.id).where(TipoElemento.capa_id == q["capaId"])))
        values = list(self.db.scalars(select(Elemento).where(*conditions).order_by(func.lower(Elemento.nombre), Elemento.id)))
        return self.listing(values, self.summary, q, True)

    def crearElemento(self, p, q, b):
        t = self.get(TipoElemento, b["tipoElementoId"])
        self.may_edit(t.capa_id)
        # El nombre se deriva de su campo base antes de insertar la fila NOT NULL.
        base = next(c for c in self.fields(t.id) if c.es_base_nombre)
        name = next((v.get("texto") for v in b["valores"] if v["campoId"] == base.id), None)
        if name is None: invalid("Falta el campo base Nombre.", "valores")
        e = self.add(Elemento, tipo_elemento_id=t.id, nombre=clean(name, "Nombre", 500),
            estado="activo", creador_id=self.user.id, ultimo_modificador_id=self.user.id)
        self.write_values(e, b["valores"], creating=True)
        result = self.elemento_json(e)
        self.audit(e, "alta", result)
        return result

    def consultarElemento(self, p, q, b):
        e = self.get(Elemento, p["elementoId"])
        if e.estado == "baja" and not q.get("incluirBaja", False): raise APIError(404, "NO_ENCONTRADO", "El elemento no está activo.")
        return self.elemento_json(e)

    def modificarElemento(self, p, q, b):
        e = self.get(Elemento, p["elementoId"])
        self.may_edit(self.get(TipoElemento, e.tipo_elemento_id).capa_id)
        before = self.elemento_json(e)
        if "valores" in b: self.write_values(e, b["valores"])
        if b.get("estado") == "activo": e.estado = "activo"
        # No renovar autoría ni bitácora si una asignación no cambia los valores.
        if before != self.elemento_json(e):
            self.touch(e)
            self.audit(e, "modificar", self.elemento_json(e), before)
        return self.elemento_json(e)

    def darBajaElemento(self, p, q, b):
        e = self.get(Elemento, p["elementoId"])
        self.may_edit(self.get(TipoElemento, e.tipo_elemento_id).capa_id)
        before = self.elemento_json(e)
        if e.estado != "baja":
            e.estado = "baja"
            self.touch(e)
            self.audit(e, "baja", self.elemento_json(e), before)
        return self.elemento_json(e)

    def listarTiposRelacion(self, p, q, b):
        conditions = []
        for key, attr in (("tipoOrigenId", TipoRelacion.tipo_origen_id), ("tipoDestinoId", TipoRelacion.tipo_destino_id)):
            if key in q: self.get(TipoElemento, q[key]); conditions.append(attr == q[key])
        return self.listing(self.all(TipoRelacion, *conditions), self.tipo_rel_json)

    def crearTipoRelacion(self, p, q, b):
        self.get(TipoElemento, b["tipoOrigenId"]); self.get(TipoElemento, b["tipoDestinoId"])
        t = self.add(TipoRelacion, nombre=clean(b["nombre"]), descripcion=clean(b["descripcion"], "descripcion", 10000),
            tipo_origen_id=b["tipoOrigenId"], tipo_destino_id=b["tipoDestinoId"])
        result = self.tipo_rel_json(t)
        self.audit(t, "alta", result)
        return result

    def consultarTipoRelacion(self, p, q, b):
        return self.tipo_rel_json(self.get(TipoRelacion, p["tipoRelacionId"]))

    def modificarTipoRelacion(self, p, q, b):
        t = self.get(TipoRelacion, p["tipoRelacionId"])
        before = self.tipo_rel_json(t)
        for key in ("nombre", "descripcion"):
            if key in b: setattr(t, key, clean(b[key], key, 120 if key == "nombre" else 10000))
        self.db.flush()
        if before != self.tipo_rel_json(t): self.audit(t, "modificar", self.tipo_rel_json(t), before)
        return self.tipo_rel_json(t)

    def validate_endpoints(self, origin, kind, destination, exclude_proposal=None, exclude_relation=None, retiring=False):
        o, d, t = self.get(Elemento, origin), self.get(Elemento, destination), self.get(TipoRelacion, kind)
        self.may_edit(self.get(TipoElemento, o.tipo_elemento_id).capa_id)
        if o.id == d.id: invalid("No se permite relacionar un elemento consigo mismo.")
        if o.estado != "activo" or d.estado != "activo": raise APIError(409, "EXTREMO_INACTIVO", "Los extremos deben estar activos.")
        if (o.tipo_elemento_id, d.tipo_elemento_id) != (t.tipo_origen_id, t.tipo_destino_id): invalid("Los extremos no coinciden con el tipo de relación.")
        if not retiring:
            duplicate = self.db.scalar(select(Relacion.id).where(Relacion.origen_id == origin,
                Relacion.destino_id == destination, Relacion.tipo_relacion_id == kind,
                Relacion.estado == "vigente", Relacion.id != exclude_relation))
            pending = self.db.scalar(select(Propuesta.id).where(Propuesta.origen_id == origin,
                Propuesta.destino_id == destination, Propuesta.tipo_relacion_id == kind,
                Propuesta.estado == "pendiente", Propuesta.operacion != "retiro", Propuesta.id != exclude_proposal))
            if duplicate or pending: raise APIError(409, "RELACION_DUPLICADA", "Ya existe el vínculo o una propuesta pendiente.")

    def prepare_proposal(self, b, existing=None):
        operation = b["operacion"]
        relation = self.get(Relacion, b["relacionId"]) if operation != "alta" else None
        if relation:
            self.may_edit(self.get(TipoElemento, self.get(Elemento, relation.origen_id).tipo_elemento_id).capa_id)
            if relation.version != b["versionBase"]: raise APIError(409, "VERSION_CAMBIADA", "La relación cambió desde la versión de origen.")
            if self.db.scalar(select(Propuesta.id).where(Propuesta.relacion_id == relation.id, Propuesta.estado == "pendiente", Propuesta.id != (existing.id if existing else None))):
                raise APIError(409, "PROPUESTA_PENDIENTE", "La relación ya tiene una propuesta pendiente.")
        if operation == "retiro":
            origin, kind, dest = relation.origen_id, relation.tipo_relacion_id, relation.destino_id
            if relation.estado == "retirada": raise APIError(409, "YA_RETIRADA", "La relación ya está retirada.")
        else: origin, kind, dest = b["origenId"], b["tipoRelacionId"], b["destinoId"]
        self.validate_endpoints(origin, kind, dest, existing.id if existing else None, relation.id if relation else None, operation == "retiro")
        justification = b["justificacion"].strip()
        if not 10 <= len(justification) <= 500: invalid("La justificación requiere entre 10 y 500 caracteres.")
        return dict(operacion=operation, origen_id=origin, destino_id=dest, tipo_relacion_id=kind,
            justificacion=justification, relacion_id=relation.id if relation else None,
            version_base=b.get("versionBase"), estado_solicitado="retirada" if operation == "retiro" else "vigente")

    def crearPropuesta(self, p, q, b):
        proposal = self.add(Propuesta, **self.prepare_proposal(b), estado="pendiente", autor_id=self.user.id)
        result = self.propuesta_json(proposal)
        self.audit(proposal, "alta_propuesta", result)
        return result

    def listarPropuestas(self, p, q, b):
        conditions = []
        if "estado" in q: conditions.append(Propuesta.estado == q["estado"])
        if "relacionId" in q:
            self.get(Relacion, q["relacionId"])
            conditions.append(or_(Propuesta.relacion_id == q["relacionId"], Propuesta.relacion_resultado_id == q["relacionId"]))
        return self.listing(self.all(Propuesta, *conditions), self.propuesta_json, q, True)

    def consultarPropuesta(self, p, q, b):
        return self.propuesta_json(self.get(Propuesta, p["propuestaId"]))

    def corregirPropuestaPendiente(self, p, q, b):
        proposal = self.get(Propuesta, p["propuestaId"])
        if proposal.estado != "pendiente": raise APIError(409, "PROPUESTA_RESUELTA", "La propuesta ya fue decidida.")
        if self.user.rol != "Administrador" and proposal.autor_id != self.user.id: raise APIError(403, "SIN_PERMISO", "Solo el autor o Administrador puede corregir la propuesta.")
        before = self.propuesta_json(proposal)
        data = {"operacion": proposal.operacion, "origenId": proposal.origen_id, "tipoRelacionId": proposal.tipo_relacion_id,
            "destinoId": proposal.destino_id, "relacionId": proposal.relacion_id, "versionBase": proposal.version_base,
            "justificacion": proposal.justificacion, **b}
        if proposal.operacion == "retiro" and any(k in b for k in ("origenId", "destinoId", "tipoRelacionId")):
            invalid("Un retiro conserva los extremos de la relación.")
        for key, value in self.prepare_proposal(data, proposal).items(): setattr(proposal, key, value)
        self.db.flush()
        result = self.propuesta_json(proposal)
        if before != result: self.audit(proposal, "corregir_propuesta", result, before)
        return result

    def decidirPropuesta(self, p, q, b):
        proposal = self.get(Propuesta, p["propuestaId"])
        if proposal.estado != "pendiente": raise APIError(409, "PROPUESTA_RESUELTA", "Solo puede decidirse una vez.")
        before = self.propuesta_json(proposal)
        relation = self.get(Relacion, proposal.relacion_id) if proposal.relacion_id else None
        if b["decision"] == "aprobar":
            data = {"operacion": proposal.operacion, "origenId": proposal.origen_id, "destinoId": proposal.destino_id,
                "tipoRelacionId": proposal.tipo_relacion_id, "relacionId": proposal.relacion_id,
                "versionBase": proposal.version_base, "justificacion": proposal.justificacion}
            self.prepare_proposal(data, proposal)
            if not relation:
                relation = self.add(Relacion, origen_id=proposal.origen_id, destino_id=proposal.destino_id,
                    tipo_relacion_id=proposal.tipo_relacion_id, justificacion=proposal.justificacion,
                    estado="vigente", version=1, creador_id=self.user.id, ultimo_modificador_id=self.user.id)
                proposal.relacion_resultado_id = relation.id
            else:
                relation.origen_id, relation.destino_id = proposal.origen_id, proposal.destino_id
                relation.tipo_relacion_id, relation.justificacion = proposal.tipo_relacion_id, proposal.justificacion
                relation.estado = proposal.estado_solicitado
                relation.version += 1
                self.touch(relation)
            proposal.estado = "aprobada"
            self.audit(relation, "aprobar_relacion", self.relacion_json(relation))
        else: proposal.estado = "rechazada"
        self.add(Decision, propuesta_id=proposal.id, resultado=b["decision"], decisor_id=self.user.id)
        result = {"propuesta": self.propuesta_json(proposal)}
        if relation: result["relacion"] = self.relacion_json(relation)
        result["entradaBitacoraId"] = self.audit(proposal, "decidir_propuesta", result["propuesta"], before)
        return result

    def listarRelaciones(self, p, q, b):
        conditions = []
        if "elementoId" in q:
            self.get(Elemento, q["elementoId"])
            conditions.append(or_(Relacion.origen_id == q["elementoId"], Relacion.destino_id == q["elementoId"]))
        if not q.get("incluirHistoricas", False):
            active = select(Elemento.id).where(Elemento.estado == "activo")
            conditions += [Relacion.estado == "vigente", Relacion.origen_id.in_(active), Relacion.destino_id.in_(active)]
        return self.listing(self.all(Relacion, *conditions), self.relacion_json, q, True)

    def consultarRelacion(self, p, q, b):
        return self.relacion_json(self.get(Relacion, p["relacionId"]))

    def consultarMapa(self, p, q, b):
        start = self.get(Elemento, p["elementoId"])
        if start.estado != "activo": raise APIError(404, "NO_ENCONTRADO", "El elemento no está activo.")
        for key, model in (("capaDestinoId", Capa), ("tipoElementoId", TipoElemento), ("tipoRelacionId", TipoRelacion)):
            if key in q: self.get(model, q[key])
        edges, nodes = [], {start.id: start}
        for r in self.all(Relacion, Relacion.estado == "vigente", or_(Relacion.origen_id == start.id, Relacion.destino_id == start.id)):
            other = self.get(Elemento, r.destino_id if r.origen_id == start.id else r.origen_id)
            t = self.get(TipoElemento, other.tipo_elemento_id)
            if other.estado != "activo": continue
            if "capaDestinoId" in q and t.capa_id != q["capaDestinoId"]: continue
            if "tipoElementoId" in q and t.id != q["tipoElementoId"]: continue
            if "tipoRelacionId" in q and r.tipo_relacion_id != q["tipoRelacionId"]: continue
            nodes[other.id] = other
            edges.append(r)
        total = len(nodes)
        selected = [start] + sorted((n for n in nodes.values() if n.id != start.id), key=lambda n: (n.nombre.lower(), n.id))[:99]
        ids = {n.id for n in selected}
        return {"elementoPartidaId": start.id, "nodos": [self.summary(n) for n in selected],
            "aristas": [{"relacionId": r.id, "origenId": r.origen_id, "destinoId": r.destino_id,
                "tipoRelacionId": r.tipo_relacion_id, "tipoRelacionNombre": self.get(TipoRelacion, r.tipo_relacion_id).nombre}
                for r in edges if r.origen_id in ids and r.destino_id in ids],
            "truncado": total > 100, "totalNodosElegibles": total}

    def listarBitacora(self, p, q, b):
        conditions = []
        for key, attr in (("objetoId", Bitacora.objeto_id), ("tipoObjeto", Bitacora.tipo_objeto), ("actorId", Bitacora.actor_id)):
            if key in q: conditions.append(attr == q[key])
        if "actorId" in q: self.get(Usuario, q["actorId"])
        rows = list(self.db.scalars(select(Bitacora).where(*conditions).order_by(Bitacora.fecha.desc(), Bitacora.id)))
        return self.listing(rows, self.audit_json, q, True)

    def consultarEntradaBitacora(self, p, q, b):
        return self.audit_json(self.get(Bitacora, p["entradaId"]))

    def cargarDemostracion(self, p, q, b):
        existing = self.db.get(CargaDemostracion, "arquitectura-ficticia-v1")
        if existing: return {**existing.resultado, "creada": False, "mensaje": "La muestra ya existe."}
        layers = {c.nombre: c for c in self.all(Capa)}
        for name in ("Negocio", "Datos", "Aplicaciones", "Tecnología", "Demostración"):
            if name not in layers:
                result = self.crearCapa({}, {}, {"nombre": name})
                layers[name] = self.get(Capa, result["id"])
        elements = []
        for name, layer in (("Objetivo", "Negocio"), ("Proyecto", "Negocio"), ("Capacidad", "Negocio"), ("Proceso", "Negocio"), ("Aplicación", "Aplicaciones")):
            t = self.db.scalar(select(TipoElemento).where(TipoElemento.capa_id == layers[layer].id, func.lower(TipoElemento.nombre) == name.lower()))
            if not t: t = self.get(TipoElemento, self.crearTipoElemento({}, {}, {"nombre": name, "capaId": layers[layer].id})["id"])
            fields = self.fields(t.id)
            if any(c.obligatorio and not c.es_base_nombre for c in fields): raise APIError(409, "MUESTRA_INCOMPATIBLE", "Un tipo de la muestra tiene campos obligatorios adicionales.")
            base = next(c for c in fields if c.es_base_nombre)
            e = self.crearElemento({}, {}, {"tipoElementoId": t.id, "valores": [{"campoId": base.id, "texto": f"{name} ficticio"}]})
            elements.append(self.get(Elemento, e["id"]))
        label = "soporta-muestra-v1"
        kind = self.db.scalar(select(TipoRelacion).where(TipoRelacion.nombre == label))
        if not kind:
            kind = self.get(TipoRelacion, self.crearTipoRelacion({}, {}, {"nombre": label, "descripcion": "Relación ficticia de demostración", "tipoOrigenId": elements[-1].tipo_elemento_id, "tipoDestinoId": elements[-2].tipo_elemento_id})["id"])
        proposal = self.crearPropuesta({}, {}, {"operacion": "alta", "origenId": elements[-1].id,
            "tipoRelacionId": kind.id, "destinoId": elements[-2].id, "justificacion": "Aplicación ficticia que soporta el proceso ficticio."})
        decision = self.decidirPropuesta({"propuestaId": proposal["id"]}, {}, {"decision": "aprobar"})
        result = {"muestraId": "arquitectura-ficticia-v1", "ficticia": True, "creada": True,
            "mensaje": "Muestra ficticia creada.", "capaIds": [c.id for c in layers.values()],
            "elementoIds": [e.id for e in elements], "relacionIds": [decision["relacion"]["id"]]}
        self.add(CargaDemostracion, id="arquitectura-ficticia-v1", resultado=result)
        return result
