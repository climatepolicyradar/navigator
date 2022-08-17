from app.db.session import Base

from sqlalchemy.orm import Session


def has_rows(db: Session, table: Base):
    return db.query(table).count()
