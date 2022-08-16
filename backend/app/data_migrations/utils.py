from app.db.session import SessionLocal
from app.db.session import Base


def has_rows(db: SessionLocal, table: Base):
    return db.query(table).count()
