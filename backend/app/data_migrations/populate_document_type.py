from sqlalchemy.orm import Session

from app.db.models import DocumentType
from .utils import has_rows


def populate_document_type(db: Session) -> None:
    """Just adds the Law and Policy types"""

    if has_rows(db, DocumentType):
        return

    db.add(DocumentType(name="Policy", description="Policy"))
    db.add(DocumentType(name="Law", description="Law"))
