from typing import Optional

from app.core.search import OpenSearchConnection, OpenSearchQueryConfig
from app.api.api_v1.schemas.search import SearchRequestBody, SearchResponseBody


class SearchCacheWrapper:
    """Wrapper for search to handle caching"""

    def __init__(self, os_connection: OpenSearchConnection) -> None:
        self.os_connection = os_connection

    def query(
        self,
        search_request_body: SearchRequestBody,
        opensearch_internal_config: OpenSearchQueryConfig,
        preference: Optional[str],
    ) -> SearchResponseBody:
        """Caching equivalent of the OpenSearchConnection query function"""
        print("- " * 60)
        print("- " * 20 + "I'm in the wrapper")
        print("- " * 60)
        return self.os_connection.query(
            search_request_body, opensearch_internal_config, preference
        )
