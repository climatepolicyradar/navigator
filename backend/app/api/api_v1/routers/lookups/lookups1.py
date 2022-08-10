from fastapi import Depends, Request

from app.core.auth import get_current_active_user
from app.db.models import (
    Geography,
    Language,
    Source,
    Instrument,
)
from app.db.session import get_db
from .utils import tree_table_to_json, table_to_json
from .router import lookups_router


@lookups_router.get(
    "/geographies",
)
def lookup_geographies(
    request: Request,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get tree of regions/geographies and associated metadata."""
    return tree_table_to_json(table=Geography, db=db)


@lookups_router.get(
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


@lookups_router.get(
    "/sources",
)
def lookup_sources(
    request: Request,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get list of sources and associated metadata."""
    return table_to_json(table=Source, db=db)


@lookups_router.get(
    "/instruments",
)
def lookup_instruments(
    request: Request,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get tree of instruments and associated metadata."""
    # TODO: this should follow a flat instruments structure for now.
    return tree_table_to_json(table=Instrument, db=db)
