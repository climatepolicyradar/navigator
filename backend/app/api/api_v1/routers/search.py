"""Searches for documents.

All endpoints should perform document searches using the SearchRequestBody as
its input. The individual endpoints will return different responses tailored
for the type of document search being performed.
"""
import json
import logging
from app.db.crud.document import get_postfix_map
from app.db.session import get_db

from fastapi import APIRouter, Request, BackgroundTasks, Depends

from app.api.api_v1.schemas.search import (
    SearchRequestBody,
    SearchResults,
    SearchResultsResponse,
    SearchResultResponse,
)
from app.core.jit_query_wrapper import jit_query_wrapper
from app.core.search import (
    OpenSearchConnection,
    OpenSearchConfig,
    OpenSearchQueryConfig,
)

_LOGGER = logging.getLogger(__name__)

# Use configured environment for router
_OPENSEARCH_CONFIG = OpenSearchConfig()
_OPENSEARCH_CONNECTION = OpenSearchConnection(opensearch_config=_OPENSEARCH_CONFIG)
_OPENSEARCH_INDEX_CONFIG = OpenSearchQueryConfig()

search_router = APIRouter()


@search_router.post("/searches", response_model=SearchResultsResponse)
def search_documents(
    request: Request,
    search_body: SearchRequestBody,
    background_tasks: BackgroundTasks,
    db=Depends(get_db),
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

    results: SearchResults = jit_query_wrapper(
        _OPENSEARCH_CONNECTION,
        background_tasks=background_tasks,
        search_request_body=search_body,
        opensearch_internal_config=_OPENSEARCH_INDEX_CONFIG,
        preference="default_search_preference",
    )

    # Now augment the search results with db data to form the response
    doc_ids = [doc.document_id for doc in results.documents]
    postfix_map = get_postfix_map(db, doc_ids)

    response: SearchResultsResponse = SearchResultsResponse(
        hits=results.hits,
        query_time_ms=results.query_time_ms,
        documents=[
            SearchResultResponse(
                **doc.dict(), document_postfix=postfix_map[doc.document_id]
            )
            for doc in results.documents
        ],
    )

    return response
