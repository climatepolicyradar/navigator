from sqlalchemy import and_, exists
from sqlalchemy.orm import Session

from app.db.models import Document, User
from app.db.schemas.document import DocumentCreate


def create_document(
    db: Session,
    document: DocumentCreate,
    creator: User,
) -> Document:
    db_document = Document(
        name=document.name,
        source_url=document.source_url,
        created_by=creator.id,
        loaded_ts=document.loaded_ts,
        source_id=1,  # TODO, but for now, always CCLW (only entry with id=1)
        url=document.url,
        geography_id=1,  # TODO
        type_id=1,  # TODO
    )

    db.add(db_document)
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
