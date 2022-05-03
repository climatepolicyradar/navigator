from fastapi import APIRouter, Depends, Request

from app.core.auth import get_current_active_user
from app.core.search import (
    OpenSearchConnection,
    OpenSearchConfig,
    OpenSearchQueryConfig,
)
from app.db.schemas.search import SearchRequestBody, SearchResponseBody

search_router = APIRouter()

# Use configured environment for router
_OPENSEARCH_CONFIG = OpenSearchConfig()
_OPENSEARCH_CONNECTION = OpenSearchConnection(
    opensearch_config=_OPENSEARCH_CONFIG
)
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
    return _OPENSEARCH_CONNECTION.query(
        search_request_body=search_body,
        opensearch_internal_config=_OPENSEARCH_INDEX_CONFIG,
        preference=str(current_user.id)
    )