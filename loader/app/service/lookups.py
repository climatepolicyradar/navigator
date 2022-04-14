from typing import Optional

from app.db.models import Geography, DocumentType, Language
from app.db.session import SessionLocal


# TODO implement caching, as lookups won't change
# https://docs.sqlalchemy.org/en/14/orm/examples.html?highlight=dogpile#module-examples.dogpile_caching


def get_type_id(db: SessionLocal, type_name) -> Optional[int]:
    result = db.query(DocumentType).filter(DocumentType.name == type_name).one_or_none()
    if result:
        return result.id
    return None


def get_geography_id(db: SessionLocal, country_code) -> Optional[int]:
    result = db.query(Geography).filter(Geography.value == country_code).first()
    if result:
        return result.id
    return None


def get_language_id(db: SessionLocal, language_code) -> Optional[int]:
    result = db.query(Language).filter(Language.language_code == language_code).first()
    if result:
        return result.id
    return None


def get_language_id_by_part1_code(db: SessionLocal, part1_code) -> Optional[int]:
    result = db.query(Language).filter(Language.part1_code == part1_code).first()
    if result:
        return result.id
    return None
