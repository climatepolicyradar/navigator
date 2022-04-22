import datetime

from app.db.models import Document
from app.db.schemas.document import DocumentCreateInternal
from sqlalchemy.orm import Session


def create_document(
    db: Session,
    document: DocumentCreateInternal,
) -> Document:
    db_document = Document(
        action_id=document.action_id,
        name=document.name,
        language_id=document.language_id,
        source_url=document.source_url,
        s3_url=document.s3_url,
        document_date=datetime.date(document.year, document.month, document.day),
        document_mod_date=document.document_mod_date,
        is_valid=document.is_valid,
        invalid_reason=document.invalid_reason,
    )

    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    return db_document


"""
# TODO might be useful for docs
def is_action_exists(
    db: Session,
    action: ActionCreate,
) -> bool:
    # Returns an doc by its unique constraint.

    return db.query(
        exists().where(
            and_(
                Action.name == action.name,
                Action.action_date
                == datetime.date(action.year, action.month, action.day),
                Action.geography_id == action.geography_id,
                Action.action_type_id == action.action_type_id,
                Action.action_source_id == action.action_source_id,
            )
        )
    ).scalar()
"""
