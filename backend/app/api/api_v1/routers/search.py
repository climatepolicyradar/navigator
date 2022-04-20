from fastapi import APIRouter, Depends, Request

from app.core.auth import get_current_active_user
from app.core.search import (
    OpenSearchConnection,
    OpenSearchConfig,
    OpenSearchQueryConfig,
    build_opensearch_request_body,
    process_opensearch_response_body,
)
from app.db.schemas.search import SearchRequestBody, SearchResponseBody

search_router = APIRouter()

# Use configured environment for router
_OPENSEARCH_CONFIG = OpenSearchConfig()
_OPENSEARCH_CONNECTION = OpenSearchConnection(opensearch_config=_OPENSEARCH_CONFIG)
_OPENSEARCH_INDEX_CONFIG = OpenSearchQueryConfig()


@search_router.post(
    "/searches",
    response_model=SearchResponseBody,
)
def search_documents(
    request: Request,
    search_body: SearchRequestBody,
    current_user=Depends(get_current_active_user),
):
    """Search for documents matching the search criteria."""
    opensearch_request_body = build_opensearch_request_body(
        search_request=search_body,
        search_internal_config=_OPENSEARCH_INDEX_CONFIG,
    )
    opensearch_response_body = _OPENSEARCH_CONNECTION.query(
        opensearch_request_body, preference=str(current_user.id)
    )
    return process_opensearch_response_body(opensearch_response_body)
