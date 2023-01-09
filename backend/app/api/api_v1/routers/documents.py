# import logging  # TODO: Uncomment when adding endpoint logs
from typing import List, Union

from fastapi import (
    APIRouter,
    Depends,
    Request,
)

from app.core.auth import (
    get_current_active_superuser,
)
from app.db.crud.document import (
    create_document_relationship,
    remove_document_relationship,
    create_relationship,
    get_document_detail,
    get_document_overviews,
    get_documents_in_relationship,
    get_relationship_by_id,
    get_relationships,
)
from app.api.api_v1.schemas.document import (
    DocumentDetailResponse,
    DocumentOverviewResponse,
    RelationshipAndDocumentsGetResponse,
    RelationshipCreateRequest,
    RelationshipEntityResponse,
)

from app.db.session import get_db

# _LOGGER = logging.getLogger(__file__)  # TODO: Uncomment when adding endpoint logs

documents_router = APIRouter()


@documents_router.get(
    "/documents",
    response_model=List[DocumentOverviewResponse],
    summary="Get a list of documents",
)
async def document_browse(
    country_code: Union[str, None] = None,
    start_year: Union[int, None] = None,
    end_year: Union[int, None] = None,
    db=Depends(get_db),
):
    """Get matching document overviews"""
    return get_document_overviews(db, country_code, start_year, end_year)


@documents_router.get(
    "/documents/{import_id_or_slug}",
    response_model=DocumentDetailResponse,
)
async def document_detail(
    import_id_or_slug: str,
    db=Depends(get_db),
):
    """Get details of the document with the given ID."""
    return get_document_detail(db, import_id_or_slug)


@documents_router.post(
    "/document-relationships",
    response_model=RelationshipEntityResponse,
    status_code=201,
)
async def post_relationship(
    request: Request,
    relationship: RelationshipCreateRequest,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """Create a relationship"""
    return create_relationship(
        db,
        relationship.name,
        relationship.type,
        relationship.description,
    )


@documents_router.get(
    "/document-relationships", response_model=List[RelationshipEntityResponse]
)
async def get_all_relationships(
    request: Request,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """Get all relationships"""
    return get_relationships(db).relationships


@documents_router.get(
    "/document-relationships/{relationship_id}",
    response_model=RelationshipAndDocumentsGetResponse,
)
async def get_relationship(
    request: Request,
    relationship_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """Get a single relationship and all documents"""
    return RelationshipAndDocumentsGetResponse(
        documents=get_documents_in_relationship(db, relationship_id),
        relationship=get_relationship_by_id(db, relationship_id),
    )


@documents_router.put(
    "/document-relationships/{relationship_id}/documents/{document_id}", status_code=201
)
async def put_document_relationship(
    request: Request,
    document_id: int,
    relationship_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """Create a document-relationship link"""
    create_document_relationship(
        db,
        document_id,
        relationship_id,
    )


@documents_router.delete(
    "/document-relationships/{relationship_id}/documents/{document_id}"
)
async def delete_document_relationship(
    request: Request,
    document_id: int,
    relationship_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """Removes a document-relationship link"""
    remove_document_relationship(
        db,
        document_id,
        relationship_id,
    )
