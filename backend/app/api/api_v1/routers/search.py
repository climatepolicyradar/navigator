"""Searches for documents.

All endpoints should perform document searches using the SearchRequestBody as
its input. The individual endpoints will return different responses tailored
for the type of document search being performed.
"""
import json
import logging
from app.core.search_cache_wrapper import SearchCacheWrapper

from fastapi import APIRouter, Depends, Request

from app.core.auth import get_current_active_db_user

# from app.core.browse import BrowseArgs, browse_rds
from app.core.search import (
    OpenSearchConnection,
    OpenSearchConfig,
    OpenSearchQueryConfig,
)
from app.api.api_v1.schemas.search import SearchRequestBody, SearchResponseBody

_LOGGER = logging.getLogger(__name__)

search_router = APIRouter()

# Use configured environment for router
_OPENSEARCH_CONFIG = OpenSearchConfig()
_OPENSEARCH_CONNECTION = OpenSearchConnection(opensearch_config=_OPENSEARCH_CONFIG)
_OPENSEARCH_INDEX_CONFIG = OpenSearchQueryConfig()

_OPENSEARCH_WRAPPER = SearchCacheWrapper(_OPENSEARCH_CONNECTION)


@search_router.post("/searches", response_model=SearchResponseBody)
def search_documents(
    request: Request,
    search_body: SearchRequestBody,
    current_user=Depends(get_current_active_db_user),
):
    """Search for documents matching the search criteria."""

    _LOGGER.info(
        "Search request",
        extra={"props": {"search_request": json.loads(search_body.json())}},
    )

    """When a query string is given - hand off the complete search to OpenSearch"""
    return _OPENSEARCH_WRAPPER.query(
        search_request_body=search_body,
        opensearch_internal_config=_OPENSEARCH_INDEX_CONFIG,
        preference=str(current_user.id),
    )
