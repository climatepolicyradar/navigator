import logging

from sqlalchemy.orm import Session

from app.db.models import Document
from app.service.api_client import post_document

logger = logging.getLogger(__file__)


def post_all_to_backend_api(db: Session):
    """Posts everything in the local database to the remote backend API."""
    for doc in db.query(Document).all():
        print("posting")
        print(doc)
        post_doc(doc)


def post_doc(doc: Document):
    payload = {
        "loaded_ts": doc.loaded_ts.isoformat(),
        "name": doc.name,
        "source_url": doc.source_url,
        "url": doc.url,
        "type_id": doc.type_id,  # this is from backend API lookup, so will exist remotely.
    }
    post_document(payload)
