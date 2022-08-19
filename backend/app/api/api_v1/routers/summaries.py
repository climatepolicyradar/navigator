"""Summaries for pages.

Like searches but with pre-defined results based on the summary context.
"""
import logging

from fastapi import APIRouter, Depends, Request

from app.core.auth import get_current_active_db_user

from app.db.schemas.search import (
    SummaryCountryResponse,
    SearchRequestBody,
)

logger = logging.getLogger(__name__)

summary_router = APIRouter()


@summary_router.post(
    "/summaries/country",
    summary="Gets a summary of the documents associated with a country.",
    response_model=SummaryCountryResponse,
)
def search_by_country(
    request: Request,
    search_body: SearchRequestBody,
    current_user=Depends(get_current_active_db_user),
):
    return SummaryCountryResponse(
        document_counts={}, top_documents={}, events=[], targets=[]
    )
