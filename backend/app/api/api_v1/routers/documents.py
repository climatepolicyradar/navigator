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
from navigator.core.aws import get_s3_client

logger = logging.getLogger(__file__)

documents_router = r = APIRouter()

# TODO return nested documents with associations
# - only show doc IDs, association types, and a hyperlink (so the associated doc can be loaded on demand)
# - possibly a flag so nested docs can be fully hydrated?


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
