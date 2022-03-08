import ssl
from datetime import datetime
from sqlite3 import IntegrityError
from typing import List, Optional

import httpx
from app.core.auth import get_current_active_user
from app.db.crud.action import create_action, get_actions_query, is_action_exists
from app.db.crud.document import create_document
from app.db.models.document import DocumentInvalidReason
from app.db.schemas.action import ActionCreate, ActionInDB
from app.db.schemas.document import DocumentCreateInternal
from app.db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from navigator.core.aws import S3Document, get_s3_client
from navigator.core.log import get_logger

logger = get_logger(__name__)
actions_router = r = APIRouter()


@r.get(
    "/actions",
    response_model=Page[ActionInDB],
    response_model_exclude_none=True,
)
async def action_list(
    db=Depends(get_db),
) -> List[ActionInDB]:
    return paginate(get_actions_query(db))


@r.post("/actions", response_model=ActionInDB)
async def action_create(
    request: Request,
    action: ActionCreate,
    db=Depends(get_db),
    s3_client=Depends(get_s3_client),
    current_user=Depends(get_current_active_user),
) -> ActionInDB:
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
    # TODO maybe https://pydantic-docs.helpmanual.io/usage/models/#parsing-data-into-a-specified-type ?
    action_create = ActionCreate(
        name=action.name,
        description=action.description,
        year=action.year,
        month=action.month,
        day=action.day,
        geography_id=action.geography_id,
        action_type_id=action.action_type_id,
        action_source_id=action.action_source_id,
        # Modification date is set to date of document submission
        mod_date=datetime.now().date(),
        documents=action.documents,
    )

    try:
        db_action = create_action(db, action_create)
    except Exception as e:
        if isinstance(e, IntegrityError):
            raise HTTPException(
                409, detail=f"Database integrity error, underlying={e.orig}"
            )
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
        document_create = DocumentCreateInternal(
            action_id=db_action.action_id,
            name=document.name,
            language_id=document.language_id,
            source_url=document.source_url,
            year=document.year,
            month=document.month,
            day=document.day,
            s3_url=moved_document_url,
            # Modification date is set to date of document submission
            document_mod_date=datetime.now().date(),
            is_valid=False,  # will be set by assign_document_validity
        )

        document_create.is_valid = True
        if document_create.source_url:
            logger.debug(
                f"Checking document validity for action, name={action.name}, url={document.source_url}"
            )
            # TODO do we need to check s3_url?
            invalid_reason = await get_document_validity(document_create.source_url)
            if invalid_reason:
                document_create.is_valid = False
                document_create.invalid_reason = invalid_reason
                logger.warning(
                    f"Invalid document, action name={action.name}, reason={invalid_reason} url={document.source_url}"
                )

        create_document(db, document_create)
        action.documents[idx] = document_create

    db.refresh(db_action)

    return ActionInDB.from_orm(db_action)


# TODO move all below to util module
transport = httpx.AsyncHTTPTransport(retries=3)
supported_content_types = ["application/pdf", "text/html"]


async def get_document_validity(source_url: str) -> Optional[DocumentInvalidReason]:
    try:
        async with httpx.AsyncClient(transport=transport, timeout=10) as client:
            response = await client.head(source_url, follow_redirects=True)
            content_type = response.headers.get("content-type")
            if content_type not in supported_content_types:
                return DocumentInvalidReason.unsupported_content_type
            else:
                return None  # no reason needed

    except (ssl.SSLCertVerificationError, ssl.SSLError):
        # we do not want to download insecurely
        return DocumentInvalidReason.net_ssl_error
    except (httpx.ConnectError, httpx.ConnectTimeout):
        # not sure if this is worth retrying, as there's probably nothing listening on the other side
        return DocumentInvalidReason.net_connection_error
    except (httpx.ReadError, httpx.ReadTimeout):
        return DocumentInvalidReason.net_read_error
    except httpx.TooManyRedirects:
        return DocumentInvalidReason.net_too_many_redirects
