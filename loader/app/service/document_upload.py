from sqlalchemy.orm import Session

from app.db.models import Document, Geography, Event
from app.service.api_client import upload_document


def upload_all_documents(db: Session):
    """Upload all source_url docs to cloud.

    The remote filename follows the template on
    https://www.notion.so/climatepolicyradar/Document-names-on-S3-6f3cd748c96141d3b714a95b42842aeb

    """

    for document_db in db.query(Document).all():
        # fetch metadata required for naming the remote doc
        geography: Geography = db.query(Geography).get(document_db.geography_id)
        event: Event = (
            db.query(Event)
            .filter(
                (Event.document_id == document_db.id) & (Event.name == "Publication")
            )
            .first()
        )
        country_code = geography.value
        publication_date = event.created_ts.date().isoformat()

        _upload_document(db, document_db, country_code, publication_date)


def _upload_document(
    db: Session, document_db: Document, country_code: str, publication_date_iso: str
):
    """Upload a single doc."""

    # TODO this depends on the new CSV layout for multi-doc actions,
    # but in the meantime, we just use "<doc name> <doc id>"
    doc_name = f"{document_db.name}-{document_db.id}"

    file_name = f"{country_code}-{publication_date_iso}-{doc_name}"

    cloud_url = upload_document(document_db.source_url, file_name)
    document_db.url = cloud_url
    db.add(document_db)
    db.commit()
