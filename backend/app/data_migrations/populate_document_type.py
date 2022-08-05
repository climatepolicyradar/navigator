from app.db.models import DocumentType

def populate_document_type(db):
    """Just adds the Law and Policy types
    """
    db.add(DocumentType(name="Policy", description="Policy"))
    db.add(DocumentType(name="Law", description="Law"))

