"""Summaries for pages.

Like searches but with pre-defined results based on the summary context.
"""
import logging
from fastapi import APIRouter, Depends, Request
from app.core.auth import get_current_active_db_user
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
def search_by_country(
    request: Request,
    geography_id: int,
    current_user=Depends(get_current_active_db_user),
    db=Depends(get_db),
):
    law_result = browse_rds(
        db, BrowseArgs(geography_id=geography_id, category=CategoryName.LAW)
    )
    policy_result = browse_rds(
        db, BrowseArgs(geography_id=geography_id, category=CategoryName.POLICY)
    )
    case_result = browse_rds(
        db, BrowseArgs(geography_id=geography_id, category=CategoryName.CASE)
    )

    # Counts
    document_counts = {}
    document_counts[CategoryName.LAW] = len(law_result.documents)
    document_counts[CategoryName.CASE] = len(case_result.documents)
    document_counts[CategoryName.POLICY] = len(policy_result.documents)

    # Top Docs
    top_documents = {}
    top_documents[CategoryName.LAW] = list(law_result.documents[:5])
    top_documents[CategoryName.CASE] = list(case_result.documents[:5])
    top_documents[CategoryName.POLICY] = list(policy_result.documents[:5])

    events = get_events_for_country(db, geography_id)

    # TODO: Add targets
    targets = []

    return SummaryCountryResponse(
        document_counts=document_counts,
        top_documents=top_documents,
        events=events,
        targets=targets,
    )
