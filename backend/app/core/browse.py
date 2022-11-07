"""Functions to support browsing the RDS document structure"""

from time import perf_counter
from typing import List, Optional
from pydantic import BaseModel
from app.db.models.document import Category, Document, Event, Geography, DocumentType
from app.api.api_v1.schemas.metadata import Event as MetaEvent
from app.api.api_v1.schemas.search import (
    SearchResult,
    SearchResults,
)
from sqlalchemy import extract
from sqlalchemy.orm import Session


class BrowseArgs(BaseModel):
    """Arguements for the browse_rds function"""

    geography_id: Optional[int] = None
    country_code: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    category: Optional[str] = None


def to_search_resp_doc(row: dict) -> SearchResult:
    return SearchResult(
        document_id=row["id"],
        document_name=row["name"],
        document_description=row["description"],
        document_date=str(row["publication_ts"]),
        document_category=row["category"],
        document_country_code=row["country_code"],
        document_country_english_shortname=row["country_name"],
        # Stuff we don't use
        document_source_name="",
        document_type="",
        document_source_url="",
        document_url="",
        document_content_type="",
        document_title_match=False,
        document_description_match=False,
        document_passage_matches=[],
    )


def browse_rds(db: Session, req: BrowseArgs) -> SearchResults:
    """Broswe RDS"""

    t0 = perf_counter()
    query = (
        db.query(
            Document.id,
            Document.name,
            Document.description,
            Document.publication_ts,
            Category.name.label("category"),
            Geography.display_value.label("country_name"),
            Geography.value.label("country_code"),
        )
        .join(Geography, Document.geography_id == Geography.id)
        .join(DocumentType, Document.type_id == DocumentType.id)
        .join(Category, Document.category_id == Category.id)
    )

    if req.geography_id is not None:
        query = query.filter(Geography.id == req.geography_id)

    if req.country_code is not None:
        query = query.filter(Geography.value == req.country_code)

    if req.start_year is not None:
        query = query.filter(extract("year", Document.publication_ts) >= req.start_year)

    if req.end_year is not None:
        query = query.filter(extract("year", Document.publication_ts) <= req.end_year)

    if req.category is not None:
        query = query.filter(Category.name == req.category)

    query = query.order_by(Document.publication_ts.desc())

    documents = [to_search_resp_doc(dict(row)) for row in query.all()]

    return SearchResults(
        hits=len(documents),
        query_time_ms=int((perf_counter() - t0) * 1e3),
        documents=documents,
    )


def get_events_for_country(db: Session, geography_id: int) -> List[MetaEvent]:
    query = (
        db.query(
            Event.name,
            Event.description,
            Event.created_ts,
        )
        .join(Document, Document.id == Event.document_id)
        .filter(Document.geography_id == geography_id)
    )
    query = query.order_by(Event.created_ts.desc())

    return [MetaEvent(**(dict(ev))) for ev in query.all()]
