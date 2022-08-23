import logging
import os
from http.client import (
    INTERNAL_SERVER_ERROR,
    UNPROCESSABLE_ENTITY,
    UNSUPPORTED_MEDIA_TYPE,
)
from pathlib import Path
from typing import List, Union

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Request,
    UploadFile,
)

from app.core.auth import (
    get_current_active_superuser,
    get_current_active_user,
    get_current_active_db_superuser,
)
from app.core.aws import get_s3_client
from app.core.util import CONTENT_TYPE_MAP
from app.db.crud.document import (
    UnknownMetadataError,
    create_document_association,
    get_document_detail,
    get_document_overviews,
    persist_document_and_metadata,
)
from app.api.api_v1.schemas.document import (
    DocumentCreateRequest,
    DocumentDetailResponse,
    DocumentOverviewResponse,
    DocumentAssociationCreateRequest,
    DocumentAssociationCreateResponse,
)

from app.db.session import get_db

_LOGGER = logging.getLogger(__file__)

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
    current_user=Depends(get_current_active_user),
):
    """Get matching document overviews"""
    return get_document_overviews(db, country_code, start_year, end_year)


@documents_router.get(
    "/documents/{document_id}",
    response_model=DocumentDetailResponse,
    response_model_exclude_none=True,
)
async def document_detail(
    document_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get details of the document with the given ID."""
    return get_document_detail(db, document_id)


@documents_router.post("/documents", response_model=DocumentDetailResponse)
async def post_document(
    request: Request,
    document_with_metadata: DocumentCreateRequest,
    db=Depends(get_db),
    current_user=Depends(get_current_active_db_superuser),
):
    """Create a document, with associated metadata."""

    try:
        new_document = persist_document_and_metadata(
            db, document_with_metadata, current_user.id
        )
    except UnknownMetadataError as e:
        _LOGGER.exception(f"Could not create document for {document_with_metadata}")
        raise HTTPException(
            UNPROCESSABLE_ENTITY, f"Creating the requested document failed: {str(e)}"
        )

    return new_document


@documents_router.post(
    "/document",
)
def document_upload(
    request: Request,
    file: UploadFile = File(...),
    current_user=Depends(get_current_active_superuser),
    s3_client=Depends(get_s3_client),
):
    """Upload a document to the queue bucket."""
    bucket = os.environ.get("DOCUMENT_BUCKET", "cpr-document-queue")
    _LOGGER.info(f"Attempting to upload {file.filename} to {bucket}")

    file_path = Path(file.filename)

    # TODO: proper content-type validation
    if file_path.suffix.lower() not in CONTENT_TYPE_MAP:
        raise HTTPException(
            UNSUPPORTED_MEDIA_TYPE, "Unsupported Media Type: must be PDF or HTML."
        )

    try:
        s3_document = s3_client.upload_fileobj(
            fileobj=file.file,
            bucket=bucket,
            key=str(file_path),
            content_type=file.content_type,
        )
    except Exception:
        raise HTTPException(
            INTERNAL_SERVER_ERROR,
            "Internal Server Error: upload error.",
        )

    # If the above function returns False, then the upload has failed.
    if not s3_document:
        raise HTTPException(
            INTERNAL_SERVER_ERROR,
            "Internal Server Error: upload failed.",
        )

    _LOGGER.info(f"Document uploaded to cloud at {s3_document.url}")
    return {
        "url": s3_document.url,
    }


@documents_router.post(
    "/associations", response_model=DocumentAssociationCreateResponse
)
async def post_association(
    request: Request,
    document_association: DocumentAssociationCreateRequest,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """Create a document, with associated metadata."""
    return create_document_association(
        db,
        document_association.document_id_from,
        document_association.document_id_to,
        document_association.name,
        document_association.type,
    )
