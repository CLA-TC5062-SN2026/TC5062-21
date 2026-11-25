"""Paginación SQL compartida: contar y cargar solo los registros solicitados."""
from sqlalchemy import func, select

PAGE_SIZE = 25


def paginate(db, statement, serializer, page=1):
    """Conserva filtros y orden del SELECT, y serializa como máximo una página."""
    total = db.scalar(select(func.count()).select_from(statement.order_by(None).subquery()))
    rows = db.scalars(statement.limit(PAGE_SIZE).offset((page - 1) * PAGE_SIZE))
    return {"items": [serializer(row) for row in rows], "total": total,
            "pagina": page, "tamanoPagina": PAGE_SIZE}
