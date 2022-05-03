import logging
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Request,
    UploadFile,
)

from app.core.auth import get_current_active_superuser
from app.core.service.loader import persist_document_and_metadata
from app.db.schemas.document import DocumentInDB
from app.db.schemas.metadata import DocumentCreateWithMetadata
from app.db.session import get_db
from navigator.core.aws import get_s3_client

logger = logging.getLogger(__file__)

documents_router = r = APIRouter()

# TODO for get_document, return nested documents with associations
# - only show doc IDs, association types, and a hyperlink (so the associated doc can be loaded on demand)
# - possibly a flag so nested docs can be fully hydrated?


@r.post("/documents", response_model=DocumentInDB)
async def post_document(
    request: Request,
    document_with_metadata: DocumentCreateWithMetadata,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """Create a document, with associated metadata."""

    db_document = persist_document_and_metadata(
        db, document_with_metadata, current_user.id
    )

    return DocumentInDB.from_orm(db_document)


@r.post(
    "/document",
)
def document_upload(
    request: Request,
    file: UploadFile = File(...),
    current_user=Depends(get_current_active_superuser),
    s3_client=Depends(get_s3_client),
):
    """Upload a document to the queue bucket."""

    file_path = Path(file.filename)

    if file_path.suffix.lower() not in (".pdf", ".html", ".htm"):
        raise HTTPException(415, "Unsupported Media Type: must be PDF or HTML.")

    s3_document = s3_client.upload_fileobj(
        fileobj=file.file, bucket="cpr-document-queue", key=str(file_path)
    )

    # If the above function returns False, then the upload has failed.
    if not s3_document:
        raise HTTPException(
            500,
            "Internal Server Error: upload failed.",
        )

    logging.info(f"Document uploaded to cloud at {s3_document.url}")
    return {
        "url": s3_document.url,
    }
