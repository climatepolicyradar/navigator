import logging

from sqlalchemy.orm import Session

from app.db.crud import get_all_valid_documents
from app.db.models import (
    APIDocument,
)
from app.poster.post import post_doc

logger = logging.getLogger(__file__)


def post_all_to_backend_api(db: Session):
    """Posts everything in the local database to the remote backend API."""
    for doc in get_all_valid_documents(db):
        # TODO: optimisation: check if we've uploaded already? (via APIDocument)
        try:
            response = post_doc(db, doc)

            # once we've uploaded, make a note of it.
            if "id" in response:
                remote_document_id = response["id"]
                apidoc = APIDocument(
                    document_id=doc.id,
                    remote_document_id=remote_document_id,
                )
                db.add(apidoc)
                db.commit()
                logger.info(
                    f"Document uploaded to API, doc.id={doc.id}, remote doc.id={remote_document_id}"
                )
            else:
                detail = response["detail"]
                logger.warning(
                    f"Document could not be posted to API, doc.id={doc.id}, error={detail}"
                )
        except Exception as e:
            logger.error(
                f"Document could not be posted to API, doc.id={doc.id}", exc_info=e
            )