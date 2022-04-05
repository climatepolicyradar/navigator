import os

from fastapi import APIRouter, Depends, Request

from app.core.auth import get_current_active_user
from app.core.search import (
    OpenSearchConnection,
    OpenSearchConfig,
    build_opensearch_request_body,
    process_opensearch_response_body,
)
from app.db.schemas.search import SearchRequestBody, SearchResponseBody

search_router = APIRouter()

# TODO: Load more settings from env
_OPENSEARCH_CONNECTION = OpenSearchConnection(
    OpenSearchConfig(
        url=os.environ["OPENSEARCH_URL"],
        username=os.environ["OPENSEARCH_USER"],
        password=os.environ["OPENSEARCH_PASSWORD"],
        index_name=os.environ["OPENSEARCH_INDEX"],
    )
)


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
    opensearch_request_body = build_opensearch_request_body(search_body)
    opensearch_response_body = _OPENSEARCH_CONNECTION.query(opensearch_request_body)
    return process_opensearch_response_body(opensearch_response_body)
