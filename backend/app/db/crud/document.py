from fastapi import HTTPException
from sqlalchemy import and_, exists

from app.db.models import Document
from app.db.schemas.document import DocumentCreate


def create_document(
    db,
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
    db.flush()
    db.refresh(db_document)

    return db_document


def is_document_exists(
    db,
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


def get_document(db, document_id: int) -> Document:
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=404,
            detail=f"Document not found with ID {document_id}",
        )

    return document
