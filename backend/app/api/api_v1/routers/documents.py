from datetime import datetime

from fastapi import APIRouter, Request, Depends, File, UploadFile, HTTPException

from app.core.auth import get_current_active_user
from app.aws.clients import S3Client


documents_router = r = APIRouter()
s3_client = S3Client()


@r.post(
    "/document",
)
def document_upload(
    request: Request,
    file: UploadFile = File(...),
    current_user=Depends(get_current_active_user),
):

    file_extension = file.filename.split(".")[-1]
    if file_extension.lower() not in ("pdf", "html", "htm"):
        raise HTTPException(415, "Unsupported Media Type: must be PDF or HTML.")

    uploaded_filename = f"user-{current_user.id}-time-{datetime.now().strftime('%Y%m%d%H%M%S')}-{file.filename}"

    s3_document = s3_client.upload_fileobj(
        fileobj=file.file, bucket="cpr-document-queue", key=uploaded_filename
    )

    # If the above function returns False, then the upload has failed.
    if not s3_document:
        raise HTTPException(
            500,
            "Internal Server Error: upload failed.",
        )

    return {
        "url": s3_document.url,
    }
