import dataclasses
import logging
from typing import Optional
from fastapi import BackgroundTasks

from app.core.search import OpenSearchConnection, OpenSearchQueryConfig
from app.api.api_v1.schemas.search import (
    JitQuery,
    SearchRequestBody,
    SearchResults,
)

_LOGGER = logging.getLogger(__name__)


def is_first_page(r: SearchRequestBody):
    """Is the first page requested for a search."""
    return r.offset == 0


def jit_query(
    os_connection: OpenSearchConnection,
    search_request_body: SearchRequestBody,
    config: OpenSearchQueryConfig,
    preference: Optional[str],
    is_background: bool = False,
):
    """Static function has been created so it can be used as a BackgroundTask."""
    response = os_connection.query(search_request_body, config, preference)
    if is_background:
        _LOGGER.info(
            "Background search complete.",
        )

    return response


def jit_query_wrapper(
    os_connection: OpenSearchConnection,
    search_request_body: SearchRequestBody,
    opensearch_internal_config: OpenSearchQueryConfig,
    preference: Optional[str],
    background_tasks: Optional[BackgroundTasks] = None,
) -> SearchResults:
    """Wraps the OpenSearchConnection query function to provide JIT search."""

    if (
        search_request_body.jit_query == JitQuery.ENABLED
        and background_tasks is not None
        and is_first_page(search_request_body)
    ):
        # Override certain config values to return the first page ASAP and
        # as accurately as possible.

        config = opensearch_internal_config

        overrides = {
            "max_doc_count": config.jit_max_doc_count,
        }
        config = dataclasses.replace(opensearch_internal_config, **overrides)
        _LOGGER.info(
            "Starting JIT search...",
        )

        response = jit_query(os_connection, search_request_body, config, preference)

        _LOGGER.info(
            "JIT search complete - starting background search.",
        )

        # In the background do the full query to prime the OpenSearch cache.
        background_tasks.add_task(
            jit_query,
            os_connection,
            search_request_body,
            opensearch_internal_config,
            preference,
            True,
        )
        return response

    _LOGGER.info(
        "Starting normal search...",
    )
    # Fall back is to return the query result synchronously
    return jit_query(
        os_connection,
        search_request_body,
        opensearch_internal_config,
        preference,
    )
