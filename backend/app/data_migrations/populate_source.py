from app.db.models import Source
from app.db.session import SessionLocal
from .utils import has_rows


def populate_source(db: SessionLocal) -> None:
    """Add the single CCLW source."""

    if has_rows(db, Source):
        return

    db.add(Source(name="CCLW"))
