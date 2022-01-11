from fastapi import APIRouter, Request, Depends

from app.db import models
from app.db.session import Base, get_db, SessionLocal
from app.core.auth import get_current_active_user


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
    return table_to_json(table=models.Geography, db=db)


@r.get(
    "/languages",
)
def lookup_languages(
    request: Request,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get list of languages and associated metadata."""
    return table_to_json(table=models.Language, db=db)


@r.get(
    "/action_types",
)
def lookup_action_types(
    request: Request,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get list of action types and associated metadata."""
    return table_to_json(table=models.ActionType, db=db)


@r.get(
    "/sources",
)
def lookup_sources(
    request: Request,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get list of sources and associated metadata."""
    return table_to_json(table=models.Source, db=db)
