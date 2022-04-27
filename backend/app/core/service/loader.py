from fastapi import (
    HTTPException,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.crud.document import create_document
from app.db.schemas.metadata import DocumentCreateWithMetadata


def persist_document_and_metadata(
    db: Session,
    document_with_metadata: DocumentCreateWithMetadata,
    creator_id: int,
):
    try:
        document_create = document_with_metadata.document

        db_document = create_document(db, document_create, creator_id)

        # TODO metadata
        # document_with_metadata.events

        return db_document
    except Exception as e:
        if isinstance(e, IntegrityError):
            raise HTTPException(409, detail="Document already exists")
        raise e
