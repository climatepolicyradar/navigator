import ssl
from datetime import datetime

import httpx
from fastapi import APIRouter, Request, Depends, HTTPException
from navigator.core.aws import get_s3_client, S3Document
from navigator.core.log import get_logger
from sqlalchemy.exc import IntegrityError

from app.core.auth import get_current_active_user
from app.db.crud import create_action, create_document, is_action_exists
from app.db.models import DocumentInvalidReason
from app.db.schemas import ActionBase, ActionCreate, DocumentCreate
from app.db.session import get_db

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

    # optimisation: check if action exists first
    if is_action_exists(db, action):
        raise HTTPException(409, detail="This action already exists")

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
        if isinstance(e, IntegrityError):
            raise HTTPException(409, detail="This item already exists")
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
            is_valid=False,  # will be set by assign_document_validity
        )

        await assign_document_validity(action, document_create)

        create_document(db, document_create)
        action.documents[idx] = document_create

    return action


# TODO move all below to util module
transport = httpx.AsyncHTTPTransport(retries=3)
supported_content_types = ["application/pdf", "text/html"]


async def assign_document_validity(action: ActionBase, document: DocumentCreate):
    if document.source_url:
        try:
            logger.debug(
                f"Checking document validity for action, name={action.name}, url={document.source_url}"
            )
            logger.handlers[0].flush()
            async with httpx.AsyncClient(transport=transport, timeout=10) as client:
                response = await client.head(document.source_url, follow_redirects=True)
                content_type = response.headers.get("content-type")
                if content_type not in supported_content_types:
                    logger.warning(
                        f"Invalid document, unsupported content type, action name={action.name}, url={document.source_url}"
                    )
                    logger.handlers[0].flush()
                    document.is_valid = False
                    document.invalid_reason = (
                        DocumentInvalidReason.unsupported_content_type
                    )
                else:
                    document.is_valid = True

        except (ssl.SSLCertVerificationError, ssl.SSLError):
            # we do not want to download insecurely
            logger.warning(
                f"Invalid document, SSL error, action name={action.name}, url={document.source_url}"
            )
            document.is_valid = False
            document.invalid_reason = DocumentInvalidReason.net_ssl_error
        except (httpx.ConnectError, httpx.ConnectTimeout):
            # not sure if this is worth retrying, as there's probably nothing listening on the other side
            logger.warning(
                f"Invalid document, connection error, action name={action.name}, url={document.source_url}"
            )
            document.is_valid = False
            document.invalid_reason = DocumentInvalidReason.net_connection_error
        except (httpx.ReadError, httpx.ReadTimeout):
            logger.warning(
                f"Invalid document, read error, action name={action.name}, url={document.source_url}"
            )
            document.is_valid = False
            document.invalid_reason = DocumentInvalidReason.net_read_error
        except httpx.TooManyRedirects:
            logger.warning(
                f"Invalid document, too many redirects, action name={action.name}, url={document.source_url}"
            )
            document.is_valid = False
            document.invalid_reason = DocumentInvalidReason.net_too_many_redirects
