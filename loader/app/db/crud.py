from typing import Optional, List

from sqlalchemy.orm import Session

from app.db.models import Document, Association, APIDocument


def get_document_by_unique_constraint(
    db: Session,
    document_name,
    geography_id,
    document_type_id,
    document_source_id,
    source_url,
) -> Optional[Document]:
    maybe_existing_doc = (
        db.query(Document)
        .filter(
            Document.name == document_name,
            Document.geography_id == geography_id,
            Document.type_id == document_type_id,
            Document.source_id == document_source_id,
            Document.source_url == source_url,
        )
        .one_or_none()
    )
    return maybe_existing_doc


def get_all_valid_documents(db: Session) -> List[Document]:
    return db.query(Document).filter(Document.is_valid).all()


def get_all_associations(db: Session):
    return db.query(Association).all()


def get_all_api_documents(db: Session):
    return db.query(APIDocument).all()
