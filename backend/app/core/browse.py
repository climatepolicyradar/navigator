"""Functions to support browse RDS document structure"""

from app.db.schemas.search import (
    SearchRequestBody,
    SearchResponseBody,
)


def browse_rds(request: SearchRequestBody) -> SearchResponseBody:
    """Broswe RDS"""
    return SearchResponseBody(hits=0, query_time_ms=0, documents=[])
