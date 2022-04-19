from typing import Optional

from sqlalchemy.orm import Session

from app.db.models import Document


def get_document_by_unique_constraint(
    db: Session,
    policy_name,
    geography_id,
    document_type_id,
    document_source_id,
    source_url,
) -> Optional[Document]:
    maybe_existing_doc = (
        db.query(Document)
        .filter(
            Document.name == policy_name,
            Document.geography_id == geography_id,
            Document.type_id == document_type_id,
            Document.source_id == document_source_id,
            Document.source_url == source_url,
        )
        .one_or_none()
    )
    return maybe_existing_doc
