"""Summaries for pages.

Like searches but with pre-defined results based on the summary context.
"""
import logging
from fastapi import APIRouter, Depends, Request
from app.api.api_v1.schemas.search import (
    SummaryCountryResponse,
    CategoryName,
)
from app.core.browse import BrowseArgs, browse_rds
from app.db.session import get_db

_LOGGER = logging.getLogger(__name__)

summary_router = APIRouter()


@summary_router.get(
    "/summaries/country/{geography_slug}",
    summary="Gets a summary of the documents associated with a country.",
    response_model=SummaryCountryResponse,
)
@summary_router.get(
    "/summaries/geography/{geography_slug}",
    summary="Gets a summary of the documents associated with a geography.",
    response_model=SummaryCountryResponse,
)
def search_by_country(
    request: Request,
    geography_slug: str,
    db=Depends(get_db),
):
    """Searches the documents filtering by country and grouping by category."""
    _LOGGER.info(
        f"Getting geography summary for {geography_slug}",
        extra={"props": {"geography_slug": geography_slug}},
    )
    top_documents = {}
    document_counts = {}

    for cat in CategoryName:
        results = browse_rds(
            db, BrowseArgs(geography_slug=geography_slug, category=cat)
        )
        document_counts[cat] = len(results.documents)
        top_documents[cat] = list(results.documents[:5])

    # TODO: Add targets
    targets = []

    return SummaryCountryResponse(
        document_counts=document_counts,
        top_documents=top_documents,
        targets=targets,
    )
