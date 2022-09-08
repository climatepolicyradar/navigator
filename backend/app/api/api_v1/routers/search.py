"""Searches for documents.

All endpoints should perform document searches using the SearchRequestBody as
its input. The individual endpoints will return different responses tailored
for the type of document search being performed.
"""
import json
import logging

from fastapi import APIRouter, Depends, Request, BackgroundTasks

from app.core.auth import get_current_active_db_user
from app.core.jit_query_wrapper import jit_query_wrapper

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


@search_router.post("/searches", response_model=SearchResponseBody)
def search_documents(
    request: Request,
    search_body: SearchRequestBody,
    background_tasks: BackgroundTasks,
    current_user=Depends(get_current_active_db_user),
):
    """Search for documents matching the search criteria."""

    _LOGGER.info(
        f"Search request (jit={search_body.jit_query})",
        extra={
            "props": {
                "search_request": json.loads(search_body.json()),
            }
        },
    )

    return jit_query_wrapper(
        _OPENSEARCH_CONNECTION,
        background_tasks=background_tasks,
        search_request_body=search_body,
        opensearch_internal_config=_OPENSEARCH_INDEX_CONFIG,
        preference=str(current_user.id),
    )
