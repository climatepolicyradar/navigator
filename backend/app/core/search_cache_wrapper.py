import dataclasses
from typing import Optional
from fastapi import BackgroundTasks

from app.core.search import OpenSearchConnection, OpenSearchQueryConfig
from app.api.api_v1.schemas.search import SearchRequestBody, SearchResponseBody


class SearchCacheWrapper:
    """Wrapper for search to handle caching"""

    def __init__(self, os_connection: OpenSearchConnection) -> None:
        self.os_connection = os_connection

    def is_first_page(self, r: SearchRequestBody):
        """Is the first page requested for a search."""
        return r.offset == 0

    @staticmethod
    def _q(
        os_connection: OpenSearchConnection,
        search_request_body: SearchRequestBody,
        config: OpenSearchQueryConfig,
        preference: Optional[str],
    ):
        """Static function has been created so it can be used as a BackgroundTask."""
        return os_connection.query(search_request_body, config, preference)

    def query(
        self,
        search_request_body: SearchRequestBody,
        opensearch_internal_config: OpenSearchQueryConfig,
        preference: Optional[str],
        background_tasks: Optional[BackgroundTasks] = None,
    ) -> SearchResponseBody:
        """Caching equivalent of the OpenSearchConnection query function"""

        if background_tasks is not None and self.is_first_page(search_request_body):
            # override certain config values to return ASAP

            config = opensearch_internal_config

            overrides = {
                "max_doc_count": 20,
                "max_passages_per_doc": 5,
                "n_passages_to_sample_per_shard": 100_000,
            }
            config = dataclasses.replace(opensearch_internal_config, **overrides)
            response = SearchCacheWrapper._q(
                self.os_connection, search_request_body, config, preference
            )

            # In the background do the full query to prime the OpenSearch cache.
            background_tasks.add_task(
                SearchCacheWrapper._q,
                self.os_connection,
                search_request_body,
                opensearch_internal_config,
                preference,
            )
            return response

        # Fall back is to return the query result synchronously
        return SearchCacheWrapper._q(
            self.os_connection,
            search_request_body,
            opensearch_internal_config,
            preference,
        )
