import datetime

from sqlalchemy.orm import Session

import app.db.models.document
import app.db.schemas.document


def create_document(
    db: Session,
    document: app.db.schemas.document.DocumentCreate,
) -> app.db.models.document.Document:
    db_document = app.db.models.document.Document(
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
