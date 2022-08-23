"""Functions to support browsing the RDS document structure"""

from app.api.api_v1.schemas.search import (
    SearchRequestBody,
    SearchResponseBody,
)


def browse_rds(request: SearchRequestBody) -> SearchResponseBody:
    """Broswe RDS"""
    # FIXME: Implement this RDS search
    return SearchResponseBody(hits=0, query_time_ms=0, documents=[])
