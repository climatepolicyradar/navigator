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
)
from app.core.aws import AWS_REGION, S3Document, get_s3_client
from app.core.util import CONTENT_TYPE_MAP, s3_to_cdn_url
from app.db.crud.document import (
    UnknownMetadataError,
    create_document_relationship,
    get_document_ids,
    get_document_ids_hash,
    remove_document_relationship,
    create_relationship,
    get_document_detail,
    get_document_overviews,
    get_documents_in_relationship,
    get_relationship_by_id,
    get_relationships,
    persist_document_and_metadata,
)
from app.api.api_v1.schemas.document import (
    DocumentCreateRequest,
    DocumentDetailResponse,
    DocumentOverviewResponse,
    DocumentUploadRequest,
    DocumentUploadResponse,
    RelationshipAndDocumentsGetResponse,
    RelationshipCreateRequest,
    RelationshipEntityResponse,
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
):
    """Get matching document overviews"""
    return get_document_overviews(db, country_code, start_year, end_year)


@documents_router.get(
    "/documents/ids",
    response_model=List[str],
    summary="Get a list of all document ids",
)
async def document_ids(
    db=Depends(get_db),
):
    """Get all document ids"""
    return get_document_ids(db)


@documents_router.get(
    "/documents/ids/hash",
    response_model=str,
    summary="Get a hex hash of all document ids, useful in determining if documents have changed without retrieving the entire list.",
)
async def document_ids_hash(
    db=Depends(get_db),
):
    """Get hex hash of all document ids"""
    return get_document_ids_hash(db)


@documents_router.get(
    "/documents/{document_id}",
    response_model=DocumentDetailResponse,
    response_model_exclude_none=True,
)
async def document_detail(
    document_id: int,
    db=Depends(get_db),
):
    """Get details of the document with the given ID."""
    return get_document_detail(db, document_id)


@documents_router.post("/documents", response_model=DocumentDetailResponse)
async def post_document(
    request: Request,
    document_with_metadata: DocumentCreateRequest,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """Create a document, with associated metadata."""

    try:
        new_document = persist_document_and_metadata(db, document_with_metadata)
    except UnknownMetadataError as e:
        _LOGGER.exception(f"Could not create document for {document_with_metadata}")
        raise HTTPException(
            UNPROCESSABLE_ENTITY, f"Creating the requested document failed: {str(e)}"
        )

    return new_document


@documents_router.post(
    "/document-uploads",
    response_model=DocumentUploadResponse,
    status_code=201,
)
def create_upload_url(
    request: Request,
    document_upload_request: DocumentUploadRequest,
    current_user=Depends(get_current_active_superuser),
    s3_client=Depends(get_s3_client),
) -> DocumentUploadResponse:
    """
    Create a pre-signed URL for uploading a document

    :param Request request: the fastapi request context
    :param DocumentUploadRequest document_upload_request: details of the file to create
    :param current_user: the details of the user making the request - must be
        a superuser, defaults to Depends(get_current_active_superuser)
    :param s3_client: the s3 client to use to create a pre-signed URL, defaults
        to Depends(get_s3_client)
    :raises HTTPException: on user auth failure or client failure
    :return str: the URL to use for file upload
    """
    bucket = os.environ.get("DOCUMENT_BUCKET", "cpr-document-queue")
    s3_document = S3Document(
        bucket_name=bucket,
        region=AWS_REGION,
        key=document_upload_request.filename,
    )
    if s3_client.document_exists(s3_document) and not document_upload_request.overwrite:
        raise HTTPException(
            UNPROCESSABLE_ENTITY, "File already exists & overwrite not requested."
        )
    try:
        return DocumentUploadResponse(
            presigned_upload_url=s3_client.generate_pre_signed_url(s3_document),
            cdn_url=s3_to_cdn_url(s3_document.url),
        )
    except Exception:
        raise HTTPException(
            INTERNAL_SERVER_ERROR,
            "Internal Server Error: upload error.",
        )


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
        # s3_client.ge
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
