-- Equipo 21 · PostgreSQL 17 · esquema revisado S05-S06-A1
BEGIN;

CREATE TABLE capas (
	nombre VARCHAR(120) COLLATE "und-x-icu" NOT NULL, 
	id UUID NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT ck_capa_nombre CHECK (length(btrim(nombre)) > 0)
);

CREATE UNIQUE INDEX uq_capa_nombre ON capas (lower(btrim(nombre)));

CREATE TABLE cargas_demostracion (
	id VARCHAR(60) NOT NULL, 
	creada_en TIMESTAMP WITH TIME ZONE NOT NULL, 
	resultado JSONB NOT NULL, 
	PRIMARY KEY (id)
);

CREATE TABLE usuarios (
	correo VARCHAR(254) COLLATE "und-x-icu" NOT NULL, 
	nombre VARCHAR(120) COLLATE "und-x-icu" NOT NULL, 
	hash_contrasena VARCHAR(60) NOT NULL, 
	rol VARCHAR(20) NOT NULL, 
	activo BOOLEAN NOT NULL, 
	creado_en TIMESTAMP WITH TIME ZONE NOT NULL, 
	id UUID NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT ck_usuario_rol CHECK (rol IN ('Administrador','Editor','Consulta')), 
	CONSTRAINT ck_usuario_nombre CHECK (length(btrim(nombre)) > 0), 
	CONSTRAINT ck_usuario_bcrypt CHECK (hash_contrasena LIKE '$2b$%%')
);

CREATE UNIQUE INDEX uq_usuario_correo ON usuarios (lower(btrim(correo)));

CREATE TABLE entradas_bitacora (
	actor_id UUID NOT NULL, 
	fecha TIMESTAMP WITH TIME ZONE NOT NULL, 
	tipo_objeto VARCHAR(50) NOT NULL, 
	objeto_id UUID NOT NULL, 
	accion VARCHAR(50) NOT NULL, 
	valores_antes JSONB, 
	valores_despues JSONB, 
	id UUID NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(actor_id) REFERENCES usuarios (id) ON DELETE RESTRICT
);

CREATE INDEX ix_entradas_bitacora_actor_id ON entradas_bitacora (actor_id);

CREATE INDEX ix_entradas_bitacora_fecha ON entradas_bitacora (fecha);

CREATE INDEX ix_entradas_bitacora_objeto_id ON entradas_bitacora (objeto_id);

CREATE TABLE permisos_edicion_capa (
	usuario_id UUID NOT NULL, 
	capa_id UUID NOT NULL, 
	asignado_por UUID NOT NULL, 
	asignado_en TIMESTAMP WITH TIME ZONE NOT NULL, 
	id UUID NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_permiso UNIQUE (usuario_id, capa_id), 
	FOREIGN KEY(usuario_id) REFERENCES usuarios (id) ON DELETE RESTRICT, 
	FOREIGN KEY(capa_id) REFERENCES capas (id) ON DELETE RESTRICT, 
	FOREIGN KEY(asignado_por) REFERENCES usuarios (id) ON DELETE RESTRICT
);

CREATE INDEX ix_permisos_edicion_capa_capa_id ON permisos_edicion_capa (capa_id);

CREATE TABLE sesiones (
	usuario_id UUID NOT NULL, 
	jti UUID NOT NULL, 
	hash_token VARCHAR(64) NOT NULL, 
	creada_en TIMESTAMP WITH TIME ZONE NOT NULL, 
	ultima_actividad_en TIMESTAMP WITH TIME ZONE NOT NULL, 
	expira_en TIMESTAMP WITH TIME ZONE NOT NULL, 
	revocada_en TIMESTAMP WITH TIME ZONE, 
	id UUID NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT ck_sesion_expira CHECK (expira_en > creada_en), 
	FOREIGN KEY(usuario_id) REFERENCES usuarios (id) ON DELETE RESTRICT, 
	UNIQUE (jti)
);

CREATE INDEX ix_sesiones_expira_en ON sesiones (expira_en);

CREATE INDEX ix_sesiones_usuario_id ON sesiones (usuario_id);

CREATE TABLE tipos_elemento (
	nombre VARCHAR(120) COLLATE "und-x-icu" NOT NULL, 
	capa_id UUID NOT NULL, 
	id UUID NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT ck_tipo_nombre CHECK (length(btrim(nombre)) > 0), 
	FOREIGN KEY(capa_id) REFERENCES capas (id) ON DELETE RESTRICT
);

CREATE INDEX ix_tipos_elemento_capa_id ON tipos_elemento (capa_id);

CREATE UNIQUE INDEX uq_tipo_nombre_capa ON tipos_elemento (capa_id, lower(btrim(nombre)));

CREATE TABLE definiciones_campo (
	tipo_elemento_id UUID NOT NULL, 
	nombre VARCHAR(120) COLLATE "und-x-icu" NOT NULL, 
	tipo_dato VARCHAR(15) NOT NULL, 
	obligatorio BOOLEAN NOT NULL, 
	es_base_nombre BOOLEAN NOT NULL, 
	id UUID NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT ck_campo_tipo CHECK (tipo_dato IN ('texto','numero','fecha','seleccion')), 
	CONSTRAINT ck_campo_nombre CHECK (length(btrim(nombre)) > 0), 
	CONSTRAINT ck_campo_base CHECK (NOT es_base_nombre OR (tipo_dato='texto' AND obligatorio AND nombre='Nombre')), 
	FOREIGN KEY(tipo_elemento_id) REFERENCES tipos_elemento (id) ON DELETE RESTRICT
);

CREATE UNIQUE INDEX uq_campo_base ON definiciones_campo (tipo_elemento_id) WHERE es_base_nombre;

CREATE UNIQUE INDEX uq_campo_nombre_tipo ON definiciones_campo (tipo_elemento_id, lower(btrim(nombre)));

CREATE TABLE elementos (
	tipo_elemento_id UUID NOT NULL, 
	nombre VARCHAR(500) COLLATE "und-x-icu" NOT NULL, 
	estado VARCHAR(10) NOT NULL, 
	id UUID NOT NULL, 
	creador_id UUID NOT NULL, 
	ultimo_modificador_id UUID NOT NULL, 
	creado_en TIMESTAMP WITH TIME ZONE NOT NULL, 
	modificado_en TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT ck_elemento_estado CHECK (estado IN ('activo','baja')), 
	CONSTRAINT ck_elemento_nombre CHECK (length(btrim(nombre)) > 0), 
	FOREIGN KEY(tipo_elemento_id) REFERENCES tipos_elemento (id) ON DELETE RESTRICT, 
	FOREIGN KEY(creador_id) REFERENCES usuarios (id) ON DELETE RESTRICT, 
	FOREIGN KEY(ultimo_modificador_id) REFERENCES usuarios (id) ON DELETE RESTRICT
);

CREATE INDEX ix_elemento_nombre ON elementos (lower(nombre), id);

CREATE INDEX ix_elementos_estado ON elementos (estado);

CREATE INDEX ix_elementos_tipo_elemento_id ON elementos (tipo_elemento_id);

CREATE TABLE tipos_relacion (
	nombre VARCHAR(120) COLLATE "und-x-icu" NOT NULL, 
	descripcion TEXT NOT NULL, 
	tipo_origen_id UUID NOT NULL, 
	tipo_destino_id UUID NOT NULL, 
	id UUID NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT ck_tipo_relacion_textos CHECK (length(btrim(nombre)) > 0 AND length(btrim(descripcion)) > 0), 
	FOREIGN KEY(tipo_origen_id) REFERENCES tipos_elemento (id) ON DELETE RESTRICT, 
	FOREIGN KEY(tipo_destino_id) REFERENCES tipos_elemento (id) ON DELETE RESTRICT
);

CREATE INDEX ix_tipos_relacion_tipo_destino_id ON tipos_relacion (tipo_destino_id);

CREATE INDEX ix_tipos_relacion_tipo_origen_id ON tipos_relacion (tipo_origen_id);

CREATE UNIQUE INDEX uq_tipo_relacion_nombre ON tipos_relacion (lower(btrim(nombre)));

CREATE TABLE opciones_campo (
	campo_id UUID NOT NULL, 
	etiqueta VARCHAR(120) COLLATE "und-x-icu" NOT NULL, 
	orden INTEGER NOT NULL, 
	activa BOOLEAN NOT NULL, 
	id UUID NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT ck_opcion CHECK (orden >= 0 AND length(btrim(etiqueta)) > 0), 
	FOREIGN KEY(campo_id) REFERENCES definiciones_campo (id) ON DELETE RESTRICT
);

CREATE UNIQUE INDEX uq_opcion_etiqueta ON opciones_campo (campo_id, lower(btrim(etiqueta)));

CREATE UNIQUE INDEX uq_opcion_orden ON opciones_campo (campo_id, orden) WHERE activa;

CREATE TABLE relaciones_validadas (
	origen_id UUID NOT NULL, 
	destino_id UUID NOT NULL, 
	tipo_relacion_id UUID NOT NULL, 
	justificacion VARCHAR(500) NOT NULL, 
	estado VARCHAR(10) NOT NULL, 
	version INTEGER NOT NULL, 
	id UUID NOT NULL, 
	creador_id UUID NOT NULL, 
	ultimo_modificador_id UUID NOT NULL, 
	creado_en TIMESTAMP WITH TIME ZONE NOT NULL, 
	modificado_en TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT ck_relacion_extremos CHECK (origen_id <> destino_id AND version >= 1), 
	CONSTRAINT ck_relacion_estado CHECK (estado IN ('vigente','retirada')), 
	CONSTRAINT ck_relacion_justificacion CHECK (length(btrim(justificacion)) BETWEEN 10 AND 500), 
	FOREIGN KEY(origen_id) REFERENCES elementos (id) ON DELETE RESTRICT, 
	FOREIGN KEY(destino_id) REFERENCES elementos (id) ON DELETE RESTRICT, 
	FOREIGN KEY(tipo_relacion_id) REFERENCES tipos_relacion (id) ON DELETE RESTRICT, 
	FOREIGN KEY(creador_id) REFERENCES usuarios (id) ON DELETE RESTRICT, 
	FOREIGN KEY(ultimo_modificador_id) REFERENCES usuarios (id) ON DELETE RESTRICT
);

CREATE INDEX ix_relaciones_validadas_destino_id ON relaciones_validadas (destino_id);

CREATE INDEX ix_relaciones_validadas_origen_id ON relaciones_validadas (origen_id);

CREATE UNIQUE INDEX uq_relacion_vigente ON relaciones_validadas (origen_id, tipo_relacion_id, destino_id) WHERE estado='vigente';

CREATE TABLE propuestas_relacion (
	operacion VARCHAR(10) NOT NULL, 
	estado VARCHAR(10) NOT NULL, 
	origen_id UUID NOT NULL, 
	destino_id UUID NOT NULL, 
	tipo_relacion_id UUID NOT NULL, 
	justificacion VARCHAR(500) NOT NULL, 
	estado_solicitado VARCHAR(10) NOT NULL, 
	relacion_id UUID, 
	relacion_resultado_id UUID, 
	version_base INTEGER, 
	autor_id UUID NOT NULL, 
	creada_en TIMESTAMP WITH TIME ZONE NOT NULL, 
	id UUID NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT ck_propuesta_estados CHECK (operacion IN ('alta','cambio','retiro') AND estado IN ('pendiente','aprobada','rechazada')), 
	CONSTRAINT ck_propuesta_extremos CHECK (origen_id <> destino_id), 
	CONSTRAINT ck_propuesta_justificacion CHECK (length(btrim(justificacion)) BETWEEN 10 AND 500), 
	CONSTRAINT ck_propuesta_objetivo CHECK ((operacion='alta' AND relacion_id IS NULL AND version_base IS NULL) OR (operacion<>'alta' AND relacion_id IS NOT NULL AND version_base>=1)), 
	CONSTRAINT ck_propuesta_solicitado CHECK (estado_solicitado IN ('vigente','retirada')), 
	FOREIGN KEY(origen_id) REFERENCES elementos (id) ON DELETE RESTRICT, 
	FOREIGN KEY(destino_id) REFERENCES elementos (id) ON DELETE RESTRICT, 
	FOREIGN KEY(tipo_relacion_id) REFERENCES tipos_relacion (id) ON DELETE RESTRICT, 
	FOREIGN KEY(relacion_id) REFERENCES relaciones_validadas (id) ON DELETE RESTRICT, 
	FOREIGN KEY(relacion_resultado_id) REFERENCES relaciones_validadas (id) ON DELETE RESTRICT, 
	FOREIGN KEY(autor_id) REFERENCES usuarios (id) ON DELETE RESTRICT
);

CREATE UNIQUE INDEX uq_propuesta_extremos ON propuestas_relacion (origen_id, tipo_relacion_id, destino_id) WHERE estado='pendiente' AND operacion <> 'retiro';

CREATE UNIQUE INDEX uq_propuesta_objetivo ON propuestas_relacion (relacion_id) WHERE estado='pendiente' AND relacion_id IS NOT NULL;

CREATE TABLE valores_campo (
	elemento_id UUID NOT NULL, 
	campo_id UUID NOT NULL, 
	texto TEXT, 
	numero FLOAT, 
	fecha DATE, 
	opcion_id UUID, 
	id UUID NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_valor_campo UNIQUE (elemento_id, campo_id), 
	CONSTRAINT ck_valor_exclusivo CHECK (num_nonnulls(texto, numero, fecha, opcion_id) = 1), 
	CONSTRAINT ck_numero_finito CHECK (numero IS NULL OR numero NOT IN ('NaN'::float8, 'Infinity'::float8, '-Infinity'::float8)), 
	FOREIGN KEY(elemento_id) REFERENCES elementos (id) ON DELETE RESTRICT, 
	FOREIGN KEY(campo_id) REFERENCES definiciones_campo (id) ON DELETE RESTRICT, 
	FOREIGN KEY(opcion_id) REFERENCES opciones_campo (id) ON DELETE RESTRICT
);

CREATE INDEX ix_valores_campo_campo_id ON valores_campo (campo_id);

CREATE TABLE decisiones_propuesta (
	propuesta_id UUID NOT NULL, 
	resultado VARCHAR(10) NOT NULL, 
	decisor_id UUID NOT NULL, 
	decidida_en TIMESTAMP WITH TIME ZONE NOT NULL, 
	id UUID NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT ck_decision_resultado CHECK (resultado IN ('aprobar','rechazar')), 
	UNIQUE (propuesta_id), 
	FOREIGN KEY(propuesta_id) REFERENCES propuestas_relacion (id) ON DELETE RESTRICT, 
	FOREIGN KEY(decisor_id) REFERENCES usuarios (id) ON DELETE RESTRICT
);

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
