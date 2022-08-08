from app.db.models import DocumentType
from app.db.session import SessionLocal

def populate_document_type(db: SessionLocal) -> None:
    """Just adds the Law and Policy types
    """
    db.add(DocumentType(name="Policy", description="Policy"))
    db.add(DocumentType(name="Law", description="Law"))

