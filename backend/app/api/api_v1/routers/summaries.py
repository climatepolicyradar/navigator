"""Summaries for pages.

Like searches but with pre-defined results based on the summary context.
"""
import logging
from fastapi import APIRouter, Depends, Request
from app.api.api_v1.schemas.search import (
    SummaryCountryResponse,
    CategoryName,
)
from app.core.browse import BrowseArgs, browse_rds, get_events_for_country
from app.db.session import get_db

_LOGGER = logging.getLogger(__name__)

summary_router = APIRouter()


@summary_router.get(
    "/summaries/country/{geography_id}",
    summary="Gets a summary of the documents associated with a country.",
    response_model=SummaryCountryResponse,
)
@summary_router.get(
    "/summaries/geography/{geography_id}",
    summary="Gets a summary of the documents associated with a geography.",
    response_model=SummaryCountryResponse,
)
def search_by_country(
    request: Request,
    geography_id: int,
    db=Depends(get_db),
):
    """Searches the documents filtering by country and grouping by category."""
    top_documents = {}
    document_counts = {}

    for cat in CategoryName:
        results = browse_rds(db, BrowseArgs(geography_id=geography_id, category=cat))
        document_counts[cat] = len(results.documents)
        top_documents[cat] = list(results.documents[:5])

    events = get_events_for_country(db, geography_id)

    # TODO: Add targets
    targets = []

    return SummaryCountryResponse(
        document_counts=document_counts,
        top_documents=top_documents,
        events=events,
        targets=targets,
    )
