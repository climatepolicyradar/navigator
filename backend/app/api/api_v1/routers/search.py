import json
import logging
from typing import Union

from fastapi import APIRouter, Depends, Request

from app.core.auth import get_current_active_db_user
from app.core.search import (
    OpenSearchConnection,
    OpenSearchConfig,
    OpenSearchQueryConfig,
)
from app.db.schemas.search import (
    BrowseInformation,
    SearchRequestBody,
    SearchResponseBody,
)

logger = logging.getLogger(__name__)

search_router = APIRouter()

# Use configured environment for router
_OPENSEARCH_CONFIG = OpenSearchConfig()
_OPENSEARCH_CONNECTION = OpenSearchConnection(opensearch_config=_OPENSEARCH_CONFIG)
_OPENSEARCH_INDEX_CONFIG = OpenSearchQueryConfig()


def get_browse_info() -> BrowseInformation:
    """Query RDS for browse information."""
    return BrowseInformation(
        document_counts={}, top_documents={}, events=[], targets=[]
    )


BrowseOrSearchResponse = Union[BrowseInformation, SearchResponseBody]


@search_router.post("/searches", response_model=SearchResponseBody)
def search_documents(
    request: Request,
    search_body: SearchRequestBody,
    current_user=Depends(get_current_active_db_user),
):
    """Search for documents matching the search criteria.

    TODO: Don't return documents with no source urls?
    """
    logger.info(
        "Search request",
        extra={"props": {"search_request": json.loads(search_body.json())}},
    )

    if search_body.query_string:
        """When a query string is given - hand off the complete search to OpenSearch"""
        response = _OPENSEARCH_CONNECTION.query(
            search_request_body=search_body,
            opensearch_internal_config=_OPENSEARCH_INDEX_CONFIG,
            preference=str(current_user.id),
        )
    else:
        """When no query string - search using RDS"""
        response = SearchResponseBody(
            hits=0, query_time_ms=0, browse_info=get_browse_info(), documents=[]
        )

    return response
