from fastapi import APIRouter, Depends, Request

from app.core.auth import get_current_active_user
from app.db.models import Source
from app.db.models.lookups import Geography, Language, ActionType
from app.db.session import Base, SessionLocal, get_db

lookups_router = r = APIRouter()


def table_to_json(table: Base, db: SessionLocal) -> dict:
    json_out = []

    for row in db.query(table).all():
        row_object = {}
        for col in row.__table__.columns:
            row_object[col.name] = getattr(row, col.name)

        json_out.append(row_object)

    return json_out


@r.get(
    "/geographies",
)
def lookup_geographies(
    request: Request,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get list of geographies and associated metadata."""
    return table_to_json(table=Geography, db=db)


@r.get(
    "/languages",
)
def lookup_languages(
    request: Request,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get list of languages and associated metadata."""
    return [
        item
        for item in table_to_json(table=Language, db=db)
        if item["part1_code"] is not None
    ]


@r.get(
    "/action_types",
)
def lookup_action_types(
    request: Request,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get list of action types and associated metadata."""
    return table_to_json(table=ActionType, db=db)


@r.get(
    "/sources",
)
def lookup_sources(
    request: Request,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get list of sources and associated metadata."""
    return table_to_json(table=Source, db=db)
