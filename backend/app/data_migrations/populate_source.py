from app.db.models import Source
from app.db.session import SessionLocal

def populate_source(db: SessionLocal) -> None:
    """ Add the single CCLW source.
    """
    db.add(Source(name="CCLW"))
