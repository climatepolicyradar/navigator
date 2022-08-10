from fastapi import Depends, Request

from app.core.auth import get_current_active_user
from app.db.models import (
    Sector,
    DocumentType,
    Category,
)
from app.db.session import get_db
from .utils import tree_table_to_json, table_to_json
from .router import lookups_router


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
