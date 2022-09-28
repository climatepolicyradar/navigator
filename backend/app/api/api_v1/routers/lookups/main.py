from fastapi import Depends, Request

from app.db.models import (
    Category,
    DocumentType,
    Framework,
    Geography,
    Hazard,
    Instrument,
    Keyword,
    Language,
    Response,
    Sector,
    Source,
)
from app.api.api_v1.schemas.metadata import Config
from app.db.session import get_db
from .router import lookups_router
from .utils import tree_table_to_json, table_to_json


@lookups_router.get(
    "/languages",
)
def lookup_languages(
    request: Request,
    db=Depends(get_db),
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
):
    """Get list of sources and associated metadata."""
    return table_to_json(table=Source, db=db)


@lookups_router.get("/categories")
def lookup_document_categories(
    request: Request,
    db=Depends(get_db),
):
    """Get tree of document types."""
    return table_to_json(table=Category, db=db)


@lookups_router.get("/config", response_model=Config)
def lookup_config(
    request: Request,
    db=Depends(get_db),
):
    """Get the config for the metadata."""
    cclw_source_collection = {
        "categories": table_to_json(table=Category, db=db),
        "document_types": table_to_json(table=DocumentType, db=db),
        "frameworks": table_to_json(table=Framework, db=db),
        "geographies": tree_table_to_json(table=Geography, db=db),
        "hazards": table_to_json(table=Hazard, db=db),
        "instruments": tree_table_to_json(table=Instrument, db=db),
        "keywords": table_to_json(table=Keyword, db=db),
        "languages": table_to_json(table=Language, db=db),
        "sectors": tree_table_to_json(table=Sector, db=db),
        "sources": table_to_json(table=Source, db=db),
        "topics": table_to_json(table=Response, db=db),
    }

    source_collections = {"CCLW": cclw_source_collection}

    metadata = {"metadata": source_collections}

    return metadata
