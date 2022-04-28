from typing import Any, Dict, List

from fastapi import APIRouter, Depends, Request

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
from app.db.session import Base, SessionLocal, get_db

lookups_router = r = APIRouter()


def table_to_json(
    table: Base,
    db: SessionLocal,  # type: ignore
) -> List[Dict]:
    json_out = []

    for row in db.query(table).all():
        row_object = {col.name: getattr(row, col.name) for col in row.__table__.columns}
        json_out.append(row_object)

    return json_out


def tree_table_to_json(
    table: Base,
    db: SessionLocal,  # type: ignore
) -> List[Dict]:
    json_out = []
    child_list_map: Dict[int, Any] = {}

    for row in db.query(table).all():
        row_object = {col.name: getattr(row, col.name) for col in row.__table__.columns}
        row_children: List[Dict[str, Any]] = []
        child_list_map[row_object["id"]] = row_children

        # No parent indicates a top level element
        node_row_object = {"node": row_object, "children": row_children}
        node_id = row_object["parent_id"]
        if node_id is None:
            json_out.append(node_row_object)
        else:
            append_list = child_list_map.get(node_id)
            if append_list is None:
                raise RuntimeError(f"Could not locate parent node with id {node_id}")
            append_list.append(node_row_object)

    return json_out


@r.get(
    "/geographies",
)
def lookup_geographies(
    request: Request,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get tree of regions/geographies and associated metadata."""
    return tree_table_to_json(table=Geography, db=db)


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
    "/sources",
)
def lookup_sources(
    request: Request,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get list of sources and associated metadata."""
    return table_to_json(table=Source, db=db)


@r.get(
    "/instruments",
)
def lookup_instruments(
    request: Request,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get tree of instruments and associated metadata."""
    return tree_table_to_json(table=Instrument, db=db)


@r.get(
    "/sectors",
)
def lookup_sectors(
    request: Request,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get tree of sectors and associated metadata."""
    return tree_table_to_json(table=Sector, db=db)


@r.get("/document_types")
def lookup_document_types(
    request: Request,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get tree of document types."""
    return table_to_json(table=DocumentType, db=db)


@r.get("/categories")
def lookup_document_categories(
    request: Request,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get tree of document types."""
    return table_to_json(table=Category, db=db)
