import requests
from datetime import datetime
from fastapi import APIRouter, Request, Depends, HTTPException

from app.core.auth import get_current_active_user
from app.db.session import get_db
from app.db.schemas import ActionBase, ActionCreate, DocumentCreate
from app.db.crud import create_action, create_document
from navigator.core.aws import get_s3_client, S3Document
from navigator.core.log import get_logger

logger = get_logger(__name__)

actions_router = r = APIRouter()


@r.post("/action", response_model=ActionBase)
async def action_create(
    request: Request,
    action: ActionBase,
    db=Depends(get_db),
    s3_client=Depends(get_s3_client),
    current_user=Depends(get_current_active_user),
) -> ActionBase:
    """Add an action and its associated documents to the databases."""

    # Data validation - check that year is in the past, and all external URLs provided point to valid PDFs.
    action_date = datetime(action.year, action.month, action.day)
    if action_date > datetime.now():
        raise HTTPException(
            400,
            detail="The date of the action provided is in the future, and should be in the past.",
        )

    invalid_urls = []

    for document in action.documents:
        if document.source_url:
            response = requests.head(document.source_url, allow_redirects=True)
            if all(
                [
                    c not in response.headers.get("content-type")
                    for c in ("application/pdf", "text/html")
                ]
            ):
                invalid_urls.append(document.source_url)

    if invalid_urls:
        raise HTTPException(
            400,
            headers={
                "invalid-urls": ", ".join(invalid_urls),
                "failed-reason": f"Document URLs {', '.join(invalid_urls)} don't direct to either HTML or PDF documents. Please update or remove the URLs for these given documents.",
            },
        )

    # Add action and related documents to database.
    action_create = ActionCreate(
        name=action.name,
        description=action.description,
        year=action.year,
        month=action.month,
        day=action.day,
        geography_id=action.geography_id,
        type_id=action.type_id,
        source_id=action.source_id,
        # Modification date is set to date of document submission
        mod_date=datetime.now().date(),
        documents=action.documents,
    )

    try:
        db_action = create_action(db, action_create)
    except Exception as e:
        logger.error(e)
        raise e

    for idx, document in enumerate(action.documents):
        # Move document to cpr-document-store bucket
        if document.s3_url:
            s3_document = S3Document.from_url(document.s3_url)
            moved_document_url = s3_client.move_document(
                s3_document,
                "cpr-document-store",
            ).url
        else:
            moved_document_url = None

        # Create document in database
        document_create = DocumentCreate(
            action_id=db_action.action_id,
            name=document.name,
            language_id=document.language_id,
            source_url=document.source_url,
            s3_url=moved_document_url,
            year=document.year,
            month=document.month,
            day=document.day,
            # Modification date is set to date of document submission
            document_mod_date=datetime.now().date(),
        )

        create_document(db, document_create)
        action.documents[idx] = document_create

    return action
