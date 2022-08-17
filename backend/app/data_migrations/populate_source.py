from sqlalchemy.orm import Session

from app.db.models import Source
from .utils import has_rows


def populate_source(db: Session) -> None:
    """Add the single CCLW source."""

    if has_rows(db, Source):
        return

    db.add(Source(name="CCLW"))
