from typing import Optional, Sequence, cast

from sqlalchemy.orm import Session

from app.core.util import tree_table_to_json, table_to_json
from app.db.models import (
    Category,
    DocumentType,
    Framework,
    Geography,
    Hazard,
    Instrument,
    Keyword,
    Language,
    Response,
    Sector,
    Source,
)


def get_metadata(db: Session):
    """Get the config for the metadata."""
    cclw_source_collection = {
        "categories": table_to_json(table=Category, db=db),
        "document_types": table_to_json(table=DocumentType, db=db),
        "frameworks": table_to_json(table=Framework, db=db),
        "geographies": tree_table_to_json(table=Geography, db=db),
        "hazards": table_to_json(table=Hazard, db=db),
        "instruments": tree_table_to_json(table=Instrument, db=db),
        "keywords": table_to_json(table=Keyword, db=db),
        "languages": table_to_json(table=Language, db=db),
        "sectors": tree_table_to_json(table=Sector, db=db),
        "sources": table_to_json(table=Source, db=db),
        "topics": table_to_json(table=Response, db=db),
    }

    source_collections = {"CCLW": cclw_source_collection}
    return {"metadata": source_collections}


def get_countries_for_region(db: Session, region_slug: str) -> Sequence[Geography]:
    geography = db.query(Geography).filter(Geography.slug == region_slug).first()
    if geography is None:
        return []

    is_valid_region = geography.parent_id is None
    if not is_valid_region:  # either unknown or not a region
        return []

    cast(Geography, geography)

    return db.query(Geography).filter(Geography.parent_id == geography.id).all()


def get_country_by_slug(db: Session, country_slug: str) -> Optional[Geography]:
    geography = db.query(Geography).filter(Geography.slug == country_slug).first()

    if geography is None:
        return None

    # TODO: improve when we go beyond countries
    is_valid_country = geography.parent_id is not None
    if not is_valid_country:
        return None

    return geography
