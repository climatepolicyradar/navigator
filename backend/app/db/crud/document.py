from fastapi import HTTPException
from sqlalchemy import and_, exists
from sqlalchemy.orm import Session

from app.db.models import Document
from app.dto.document import DocumentCreate


def create_document(
    db: Session,
    document: DocumentCreate,
    creator_id: int,
) -> Document:
    db_document = Document(
        name=document.name,
        description=document.description,
        source_url=document.source_url,
        created_by=creator_id,
        loaded_ts=document.loaded_ts,
        source_id=document.source_id,
        url=document.url,
        md5_sum=document.md5_sum,
        geography_id=document.geography_id,
        type_id=document.type_id,
        category_id=document.category_id,
        publication_ts=document.publication_ts,
    )

    db.add(db_document)
    # TODO don't call commit here. Perhaps in a middleware somewhere before the response is returned
    # Removing commit here will ensure: roll back the doc if there's a subsequent error persisting metadata.
    db.commit()
    db.refresh(db_document)

    return db_document


def is_document_exists(
    db: Session,
    document: DocumentCreate,
) -> bool:
    # Returns a doc by its unique constraint.

    return db.query(
        exists().where(
            and_(
                Document.name == document.name,
                Document.geography_id == document.geography_id,
                Document.type_id == document.type_id,
                Document.source_id == document.source_id,
            )
        )
    ).scalar()


def get_document(db: Session, document_id: int) -> Document:
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=404,
            detail=f"Document not found with ID {document_id}",
        )

    return document
