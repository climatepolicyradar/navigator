import dataclasses
from typing import Optional
from fastapi import BackgroundTasks

from app.core.search import OpenSearchConnection, OpenSearchQueryConfig
from app.api.api_v1.schemas.search import SearchRequestBody, SearchResponseBody


def is_first_page(r: SearchRequestBody):
    """Is the first page requested for a search."""
    return r.offset == 0


def _q(
    os_connection: OpenSearchConnection,
    search_request_body: SearchRequestBody,
    config: OpenSearchQueryConfig,
    preference: Optional[str],
):
    """Static function has been created so it can be used as a BackgroundTask."""
    return os_connection.query(search_request_body, config, preference)


def jit_query_wrapper(
    os_connection: OpenSearchConnection,
    search_request_body: SearchRequestBody,
    opensearch_internal_config: OpenSearchQueryConfig,
    preference: Optional[str],
    background_tasks: Optional[BackgroundTasks] = None,
) -> SearchResponseBody:
    """Wraps the OpenSearchConnection query function to provide JIT search."""

    if background_tasks is not None and is_first_page(search_request_body):
        # Override certain config values to return the first page ASAP and
        # as accurately as possible.

        config = opensearch_internal_config

        overrides = {
            "max_doc_count": config.jit_max_doc_count,
        }
        config = dataclasses.replace(opensearch_internal_config, **overrides)
        response = _q(os_connection, search_request_body, config, preference)

        # In the background do the full query to prime the OpenSearch cache.
        background_tasks.add_task(
            _q,
            os_connection,
            search_request_body,
            opensearch_internal_config,
            preference,
        )
        return response

    # Fall back is to return the query result synchronously
    return _q(
        os_connection,
        search_request_body,
        opensearch_internal_config,
        preference,
    )
