"""Summaries for pages.

Like searches but with pre-defined results based on the summary context.
"""
import logging
from fastapi import APIRouter, Depends, Request
from app.core.auth import get_current_active_db_user
from app.db.schemas.search import (
    SummaryCountryResponse,
)

logger = logging.getLogger(__name__)

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
):
    # FIXME: Implement this RDS search
    return SummaryCountryResponse(
        document_counts={}, top_documents={}, events=[], targets=[]
    )
