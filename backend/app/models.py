"""Modelo físico PostgreSQL; la DDL exportada vive en S05_S06_A1/esquema_bd.sql."""
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import (Boolean, CheckConstraint, Date, DateTime, ForeignKey,
                        Float, Index, Integer, String, Text, UniqueConstraint, text)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def now():
    return datetime.now(timezone.utc)


def uid():
    return str(uuid4())


class Base(DeclarativeBase):
    pass


class Identity:
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=uid)


class Usuario(Identity, Base):
    __tablename__ = "usuarios"
    correo: Mapped[str] = mapped_column(String(254, collation="und-x-icu"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(120, collation="und-x-icu"), nullable=False)
    hash_contrasena: Mapped[str] = mapped_column(String(60), nullable=False)
    rol: Mapped[str] = mapped_column(String(20), nullable=False, default="Consulta")
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    __table_args__ = (
        CheckConstraint("rol IN ('Administrador','Editor','Consulta')", name="ck_usuario_rol"),
        CheckConstraint("length(btrim(nombre)) > 0", name="ck_usuario_nombre"),
        CheckConstraint("hash_contrasena LIKE '$2b$%'", name="ck_usuario_bcrypt"),
        Index("uq_usuario_correo", text("lower(btrim(correo))"), unique=True),
    )


class Sesion(Identity, Base):
    __tablename__ = "sesiones"
    usuario_id: Mapped[str] = mapped_column(ForeignKey("usuarios.id", ondelete="RESTRICT"), index=True)
    jti: Mapped[str] = mapped_column(UUID(as_uuid=False), unique=True, nullable=False)
    hash_token: Mapped[str] = mapped_column(String(64), nullable=False)
    creada_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    ultima_actividad_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    expira_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    revocada_en: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    __table_args__ = (CheckConstraint("expira_en > creada_en", name="ck_sesion_expira"),)


class Capa(Identity, Base):
    __tablename__ = "capas"
    nombre: Mapped[str] = mapped_column(String(120, collation="und-x-icu"), nullable=False)
    __table_args__ = (CheckConstraint("length(btrim(nombre)) > 0", name="ck_capa_nombre"),
                      Index("uq_capa_nombre", text("lower(btrim(nombre))"), unique=True))


class Permiso(Identity, Base):
    __tablename__ = "permisos_edicion_capa"
    usuario_id: Mapped[str] = mapped_column(ForeignKey("usuarios.id", ondelete="RESTRICT"))
    capa_id: Mapped[str] = mapped_column(ForeignKey("capas.id", ondelete="RESTRICT"), index=True)
    asignado_por: Mapped[str] = mapped_column(ForeignKey("usuarios.id", ondelete="RESTRICT"))
    asignado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    __table_args__ = (UniqueConstraint("usuario_id", "capa_id", name="uq_permiso"),)


class TipoElemento(Identity, Base):
    __tablename__ = "tipos_elemento"
    nombre: Mapped[str] = mapped_column(String(120, collation="und-x-icu"), nullable=False)
    capa_id: Mapped[str] = mapped_column(ForeignKey("capas.id", ondelete="RESTRICT"), index=True)
    __table_args__ = (CheckConstraint("length(btrim(nombre)) > 0", name="ck_tipo_nombre"),
                      Index("uq_tipo_nombre_capa", "capa_id", text("lower(btrim(nombre))"), unique=True))


class Campo(Identity, Base):
    __tablename__ = "definiciones_campo"
    tipo_elemento_id: Mapped[str] = mapped_column(ForeignKey("tipos_elemento.id", ondelete="RESTRICT"))
    nombre: Mapped[str] = mapped_column(String(120, collation="und-x-icu"), nullable=False)
    tipo_dato: Mapped[str] = mapped_column(String(15), nullable=False)
    obligatorio: Mapped[bool] = mapped_column(Boolean, nullable=False)
    es_base_nombre: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    __table_args__ = (
        CheckConstraint("tipo_dato IN ('texto','numero','fecha','seleccion')", name="ck_campo_tipo"),
        CheckConstraint("length(btrim(nombre)) > 0", name="ck_campo_nombre"),
        CheckConstraint("NOT es_base_nombre OR (tipo_dato='texto' AND obligatorio AND nombre='Nombre')", name="ck_campo_base"),
        Index("uq_campo_nombre_tipo", "tipo_elemento_id", text("lower(btrim(nombre))"), unique=True),
        Index("uq_campo_base", "tipo_elemento_id", unique=True, postgresql_where=text("es_base_nombre")),
    )


class Opcion(Identity, Base):
    __tablename__ = "opciones_campo"
    campo_id: Mapped[str] = mapped_column(ForeignKey("definiciones_campo.id", ondelete="RESTRICT"))
    etiqueta: Mapped[str] = mapped_column(String(120, collation="und-x-icu"), nullable=False)
    orden: Mapped[int] = mapped_column(Integer, nullable=False)
    activa: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    __table_args__ = (
        CheckConstraint("orden >= 0 AND length(btrim(etiqueta)) > 0", name="ck_opcion"),
        Index("uq_opcion_orden", "campo_id", "orden", unique=True, postgresql_where=text("activa")),
        Index("uq_opcion_etiqueta", "campo_id", text("lower(btrim(etiqueta))"), unique=True),
    )


class Trazable:
    creador_id: Mapped[str] = mapped_column(ForeignKey("usuarios.id", ondelete="RESTRICT"))
    ultimo_modificador_id: Mapped[str] = mapped_column(ForeignKey("usuarios.id", ondelete="RESTRICT"))
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    modificado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class Elemento(Identity, Trazable, Base):
    __tablename__ = "elementos"
    tipo_elemento_id: Mapped[str] = mapped_column(ForeignKey("tipos_elemento.id", ondelete="RESTRICT"), index=True)
    nombre: Mapped[str] = mapped_column(String(500, collation="und-x-icu"), nullable=False)
    estado: Mapped[str] = mapped_column(String(10), default="activo", nullable=False, index=True)
    __table_args__ = (CheckConstraint("estado IN ('activo','baja')", name="ck_elemento_estado"),
                      CheckConstraint("length(btrim(nombre)) > 0", name="ck_elemento_nombre"),
                      Index("ix_elemento_nombre", text("lower(nombre)"), "id"))


class Valor(Identity, Base):
    __tablename__ = "valores_campo"
    elemento_id: Mapped[str] = mapped_column(ForeignKey("elementos.id", ondelete="RESTRICT"))
    campo_id: Mapped[str] = mapped_column(ForeignKey("definiciones_campo.id", ondelete="RESTRICT"), index=True)
    texto: Mapped[str | None] = mapped_column(Text)
    numero: Mapped[float | None] = mapped_column(Float)
    fecha: Mapped[datetime | None] = mapped_column(Date)
    opcion_id: Mapped[str | None] = mapped_column(ForeignKey("opciones_campo.id", ondelete="RESTRICT"))
    __table_args__ = (
        UniqueConstraint("elemento_id", "campo_id", name="uq_valor_campo"),
        CheckConstraint("num_nonnulls(texto, numero, fecha, opcion_id) = 1", name="ck_valor_exclusivo"),
        CheckConstraint("numero IS NULL OR numero NOT IN ('NaN'::float8, 'Infinity'::float8, '-Infinity'::float8)", name="ck_numero_finito"),
    )


class TipoRelacion(Identity, Base):
    __tablename__ = "tipos_relacion"
    nombre: Mapped[str] = mapped_column(String(120, collation="und-x-icu"), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    tipo_origen_id: Mapped[str] = mapped_column(ForeignKey("tipos_elemento.id", ondelete="RESTRICT"), index=True)
    tipo_destino_id: Mapped[str] = mapped_column(ForeignKey("tipos_elemento.id", ondelete="RESTRICT"), index=True)
    __table_args__ = (CheckConstraint("length(btrim(nombre)) > 0 AND length(btrim(descripcion)) > 0", name="ck_tipo_relacion_textos"),
                      Index("uq_tipo_relacion_nombre", text("lower(btrim(nombre))"), unique=True))


class Relacion(Identity, Trazable, Base):
    __tablename__ = "relaciones_validadas"
    origen_id: Mapped[str] = mapped_column(ForeignKey("elementos.id", ondelete="RESTRICT"), index=True)
    destino_id: Mapped[str] = mapped_column(ForeignKey("elementos.id", ondelete="RESTRICT"), index=True)
    tipo_relacion_id: Mapped[str] = mapped_column(ForeignKey("tipos_relacion.id", ondelete="RESTRICT"))
    justificacion: Mapped[str] = mapped_column(String(500), nullable=False)
    estado: Mapped[str] = mapped_column(String(10), default="vigente", nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    __table_args__ = (
        CheckConstraint("origen_id <> destino_id AND version >= 1", name="ck_relacion_extremos"),
        CheckConstraint("estado IN ('vigente','retirada')", name="ck_relacion_estado"),
        CheckConstraint("length(btrim(justificacion)) BETWEEN 10 AND 500", name="ck_relacion_justificacion"),
        Index("uq_relacion_vigente", "origen_id", "tipo_relacion_id", "destino_id", unique=True, postgresql_where=text("estado='vigente'")),
    )


class Propuesta(Identity, Base):
    __tablename__ = "propuestas_relacion"
    operacion: Mapped[str] = mapped_column(String(10), nullable=False)
    estado: Mapped[str] = mapped_column(String(10), default="pendiente", nullable=False)
    origen_id: Mapped[str] = mapped_column(ForeignKey("elementos.id", ondelete="RESTRICT"))
    destino_id: Mapped[str] = mapped_column(ForeignKey("elementos.id", ondelete="RESTRICT"))
    tipo_relacion_id: Mapped[str] = mapped_column(ForeignKey("tipos_relacion.id", ondelete="RESTRICT"))
    justificacion: Mapped[str] = mapped_column(String(500), nullable=False)
    estado_solicitado: Mapped[str] = mapped_column(String(10), nullable=False)
    relacion_id: Mapped[str | None] = mapped_column(ForeignKey("relaciones_validadas.id", ondelete="RESTRICT"))
    relacion_resultado_id: Mapped[str | None] = mapped_column(ForeignKey("relaciones_validadas.id", ondelete="RESTRICT"))
    version_base: Mapped[int | None] = mapped_column(Integer)
    autor_id: Mapped[str] = mapped_column(ForeignKey("usuarios.id", ondelete="RESTRICT"))
    creada_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    __table_args__ = (
        CheckConstraint("operacion IN ('alta','cambio','retiro') AND estado IN ('pendiente','aprobada','rechazada')", name="ck_propuesta_estados"),
        CheckConstraint("origen_id <> destino_id", name="ck_propuesta_extremos"),
        CheckConstraint("length(btrim(justificacion)) BETWEEN 10 AND 500", name="ck_propuesta_justificacion"),
        CheckConstraint("(operacion='alta' AND relacion_id IS NULL AND version_base IS NULL) OR (operacion<>'alta' AND relacion_id IS NOT NULL AND version_base>=1)", name="ck_propuesta_objetivo"),
        CheckConstraint("estado_solicitado IN ('vigente','retirada')", name="ck_propuesta_solicitado"),
        Index("uq_propuesta_objetivo", "relacion_id", unique=True, postgresql_where=text("estado='pendiente' AND relacion_id IS NOT NULL")),
        Index("uq_propuesta_extremos", "origen_id", "tipo_relacion_id", "destino_id", unique=True, postgresql_where=text("estado='pendiente' AND operacion <> 'retiro'")),
    )


class Decision(Identity, Base):
    __tablename__ = "decisiones_propuesta"
    propuesta_id: Mapped[str] = mapped_column(ForeignKey("propuestas_relacion.id", ondelete="RESTRICT"), unique=True)
    resultado: Mapped[str] = mapped_column(String(10), nullable=False)
    decisor_id: Mapped[str] = mapped_column(ForeignKey("usuarios.id", ondelete="RESTRICT"))
    decidida_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    __table_args__ = (CheckConstraint("resultado IN ('aprobar','rechazar')", name="ck_decision_resultado"),)


class Bitacora(Identity, Base):
    __tablename__ = "entradas_bitacora"
    actor_id: Mapped[str] = mapped_column(ForeignKey("usuarios.id", ondelete="RESTRICT"), index=True)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, index=True)
    tipo_objeto: Mapped[str] = mapped_column(String(50), nullable=False)
    objeto_id: Mapped[str] = mapped_column(UUID(as_uuid=False), nullable=False, index=True)
    accion: Mapped[str] = mapped_column(String(50), nullable=False)
    valores_antes: Mapped[dict | None] = mapped_column(JSONB)
    valores_despues: Mapped[dict | None] = mapped_column(JSONB)


class CargaDemostracion(Base):
    __tablename__ = "cargas_demostracion"
    id: Mapped[str] = mapped_column(String(60), primary_key=True)
    creada_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    resultado: Mapped[dict] = mapped_column(JSONB, nullable=False)
