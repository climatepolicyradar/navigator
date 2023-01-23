from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db


def is_database_online(db: Session = Depends(get_db)) -> bool:
    """
    Checks database health.

    TODO: More comprehensive health checks
    """
    return True
