from datetime import datetime
from typing import List

import requests
from fastapi import APIRouter, Request, Depends, HTTPException
from navigator.core.aws import get_s3_client, S3Document
from navigator.core.log import get_logger
from sqlalchemy.exc import IntegrityError

from app.core.auth import get_current_active_user
from app.db.crud import create_action, create_document, is_action_exists
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

    # optimisation: check if action exists first
    if is_action_exists(db, action_create):
        raise HTTPException(409, detail="This action already exists")

    invalid_urls = await check_document_validity(action)

    if invalid_urls:
        raise HTTPException(
            400,
            headers={
                "invalid-urls": ", ".join(invalid_urls),
                "failed-reason": "A document has an unsupported mimetype",
            },
            detail="A document has an unsupported mimetype",
        )

    # Add action and related documents to database.
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
        )

        create_document(db, document_create)
        action.documents[idx] = document_create

    return action


async def check_document_validity(action) -> List[str]:
    invalid_urls = []
    for document in action.documents:
        if document.source_url:
            try:
                logger.debug(
                    f"Checking document validity for action, name={action.name}, url={document.source_url}"
                )
                response = requests.head(document.source_url, allow_redirects=True)
                if all(
                        [
                            c not in response.headers.get("content-type")
                            for c in ("application/pdf", "text/html")
                        ]
                ):
                    logger.warning(
                        f"Found invalid document for action, name={action.name}, url={document.source_url}"
                    )
                    invalid_urls.append(document.source_url)
            except requests.exceptions.SSLError:
                # we do not want to download insecurely
                invalid_urls.append(document.source_url)
            except requests.exceptions.ConnectionError:
                # not sure if this is worth retrying, as there's probably nothing listening on the other side
                invalid_urls.append(document.source_url)
    return invalid_urls


# TODO retry the document requests:
"""
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

s = requests.Session()
retries = Retry(
    total=10,
    read=10,
    connect=10,
    backoff_factor=1,  # 1 second, so the successive sleeps will be 0.5, 1, 2, 4, 8, 16, 32, 64, 128, 256.
    status_forcelist=[ 429, 500, 502, 503, 504 ],
    allowed_methods=False)
adapter = HTTPAdapter(max_retries=retries)
s.mount('https://', adapter)
s.mount('http://', adapter)
"""
