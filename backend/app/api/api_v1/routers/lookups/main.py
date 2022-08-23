from fastapi import Depends, Request

from app.core.auth import get_current_active_user
from app.db.models import (
    Geography,
    Language,
    Source,
    Instrument,
    Sector,
    DocumentType,
    Category,
)
from app.db.schemas.metadata import Config
from app.db.session import get_db
from .router import lookups_router
from .utils import tree_table_to_json, table_to_json


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


@lookups_router.get(
    "/sectors",
)
def lookup_sectors(
    request: Request,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get tree of sectors and associated metadata."""
    return tree_table_to_json(table=Sector, db=db)


@lookups_router.get("/document_types")
def lookup_document_types(
    request: Request,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get tree of document types."""
    return table_to_json(table=DocumentType, db=db)


@lookups_router.get("/categories")
def lookup_document_categories(
    request: Request,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get tree of document types."""
    return table_to_json(table=Category, db=db)


@lookups_router.get("/config", response_model=Config)
def lookup_config(
    request: Request,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get the config for the metadata."""
    cclw_source_collection = {
        "geographies": tree_table_to_json(table=Geography, db=db),
        "document_types": table_to_json(table=DocumentType, db=db),
        "sectors": tree_table_to_json(table=Sector, db=db),
        "instruments": tree_table_to_json(table=Instrument, db=db),
    }

    source_collections = {"CCLW": cclw_source_collection}

    metadata = {"metadata": source_collections}

    return metadata
