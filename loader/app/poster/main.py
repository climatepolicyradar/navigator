import logging

from sqlalchemy.orm import Session

from app.db.models import Document, APIDocument
from app.service.api_client import post_document

logger = logging.getLogger(__file__)


def post_all_to_backend_api(db: Session):
    """Posts everything in the local database to the remote backend API."""
    debug_count = 0
    for doc in db.query(Document).all():
        debug_count += 1
        if debug_count > 10:
            print("done for testing purposes")
            break
        # optimisation: check if we've uploaded already
        # read from api_document
        try:
            response = post_doc(doc)
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


def post_doc(doc: Document) -> dict:
    payload = {
        "document": {
            "loaded_ts": doc.loaded_ts.isoformat(),
            "name": doc.name,
            "source_url": doc.source_url,
            "url": doc.url,
            "type_id": doc.type_id,  # this is from backend API lookup, so will exist remotely.
        },
        "source_id": doc.source_id,
        "events": [],  # TODO
        "sectors": [],  # TODO
        "instruments": [],  # TODO
        "frameworks": [],  # TODO
        "responses": [],  # TODO
        "hazards": [],  # TODO
        "language_codes": [],  # TODO
    }
    response = post_document(payload)
    return response.json()
