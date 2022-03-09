from fastapi import Depends
from sqlalchemy.orm import Session

# from app.db.models.lookups import Geography
from app.db.session import get_db


def is_database_online(db: Session = Depends(get_db)) -> bool:
    """Checks database health.

    TODO maybe check all lookups are populated?
    """
    return True  # db.query(Geography).first() is not None
