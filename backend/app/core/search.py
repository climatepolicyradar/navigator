import json
import time
import logging
import os
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from opensearchpy import OpenSearch
from opensearchpy import JSONSerializer as jss
from sentence_transformers import SentenceTransformer

from app.core.config import (
    OPENSEARCH_INDEX_INNER_PRODUCT_THRESHOLD,
    OPENSEARCH_INDEX_MAX_DOC_COUNT,
    OPENSEARCH_INDEX_MAX_PASSAGES_PER_DOC,
    OPENSEARCH_INDEX_KNN_K_VALUE,
    OPENSEARCH_INDEX_N_PASSAGES_TO_SAMPLE_PER_SHARD,
    OPENSEARCH_INDEX_NAME_BOOST,
    OPENSEARCH_INDEX_DESCRIPTION_BOOST,
    OPENSEARCH_INDEX_EMBEDDED_TEXT_BOOST,
    OPENSEARCH_INDEX_NAME_KEY,
    OPENSEARCH_INDEX_DESCRIPTION_KEY,
    OPENSEARCH_INDEX_DESCRIPTION_EMBEDDING_KEY,
    OPENSEARCH_INDEX_INDEX_KEY,
    OPENSEARCH_INDEX_TEXT_BLOCK_KEY,
    OPENSEARCH_INDEX_ENCODER,
    OPENSEARCH_URL,
    OPENSEARCH_INDEX,
    OPENSEARCH_USERNAME,
    OPENSEARCH_PASSWORD,
    OPENSEARCH_REQUEST_TIMEOUT,
    OPENSEARCH_USE_SSL,
    OPENSEARCH_VERIFY_CERTS,
    OPENSEARCH_SSL_WARNINGS,
    OPENSEARCH_JIT_MAX_DOC_COUNT,
)
from app.core.util import content_type_from_path, s3_to_cdn_url
from app.api.api_v1.schemas.search import (
    FilterField,
    OpenSearchResponseDescriptionMatch,
    OpenSearchResponseNameMatch,
    OpenSearchResponseMatchBase,
    OpenSearchResponsePassageMatch,
    SearchRequestBody,
    SearchResponseBody,
    SearchResponseDocument,
    SearchResponseDocumentPassage,
    SortField,
    SortOrder,
)

_LOGGER = logging.getLogger(__name__)

_ENCODER = SentenceTransformer(
    model_name_or_path=OPENSEARCH_INDEX_ENCODER,
    cache_folder=os.environ.get("INDEX_ENCODER_CACHE_FOLDER", "/models"),
)
# Map a sort field type to the document key used by OpenSearch
_SORT_FIELD_MAP: Mapping[SortField, str] = {
    SortField.DATE: "document_date",
    SortField.TITLE: "document_name",
}
# TODO: Map a filter field type to the document key used by OpenSearch
_FILTER_FIELD_MAP: Mapping[FilterField, str] = {
    FilterField.SOURCE: "document_source_name",
    FilterField.COUNTRY: "document_country_english_shortname",
    FilterField.REGION: "document_region_english_shortname",
    FilterField.SECTOR: "document_sector_name",
    FilterField.TYPE: "document_type",
    FilterField.CATEGORY: "document_category",
    FilterField.KEYWORD: "document_keyword",
    FilterField.HAZARD: "document_hazard_name",
    FilterField.LANGUAGE: "document_language",
    FilterField.FRAMEWORK: "document_framework_name",
    # TODO: we need to fix the lookup API for instruments
    FilterField.INSTRUMENT: "document_instrument_name",
    # TODO: we still call this 'response' in the database. We might want to propagate the rename to 'topic' everywhere.
    FilterField.TOPIC: "document_response_name",
}
_REQUIRED_FIELDS = ["document_name"]
_DEFAULT_BROWSE_SORT_FIELD = SortField.DATE
_DEFAULT_SORT_ORDER = SortOrder.DESCENDING
_JSON_SERIALIZER = jss()


class QueryMode(Enum):
    """High level modes we use for querying Opensearch"""

    BROWSE = "browse"
    SEARCH = "search"


def _innerproduct_threshold_to_lucene_threshold(ip_thresh: float) -> float:
    """Maps inner product to lucene threashold.

    Opensearch documentation on mapping similarity functions to Lucene thresholds is
    here: https://github.com/opensearch-project/k-NN/blob/main/src/main/java/org/opensearch/knn/index/SpaceType.java#L33

    It defines 'inner product' as negative inner product i.e. a distance rather than
    similarity measure, so we reverse the signs of inner product here compared to the docs.
    """
    if ip_thresh > 0:
        return ip_thresh + 1
    else:
        return 1 / (1 - ip_thresh)


@dataclass(frozen=True)
class OpenSearchQueryConfig:
    """Configuration for searches sent to OpenSearch."""

    name_boost: int = OPENSEARCH_INDEX_NAME_BOOST
    description_boost: int = OPENSEARCH_INDEX_DESCRIPTION_BOOST
    embedded_text_boost: int = OPENSEARCH_INDEX_EMBEDDED_TEXT_BOOST
    lucene_threshold: float = _innerproduct_threshold_to_lucene_threshold(
        OPENSEARCH_INDEX_INNER_PRODUCT_THRESHOLD
    )  # TODO: tune me separately for descriptions?
    max_doc_count: int = OPENSEARCH_INDEX_MAX_DOC_COUNT
    max_passages_per_doc: int = OPENSEARCH_INDEX_MAX_PASSAGES_PER_DOC
    n_passages_to_sample_per_shard: int = (
        OPENSEARCH_INDEX_N_PASSAGES_TO_SAMPLE_PER_SHARD
    )
    k = OPENSEARCH_INDEX_KNN_K_VALUE
    jit_max_doc_count: int = OPENSEARCH_JIT_MAX_DOC_COUNT


@dataclass
class OpenSearchConfig:
    """Config for accessing an OpenSearch instance."""

    url: str = OPENSEARCH_URL
    username: str = OPENSEARCH_USERNAME
    password: str = OPENSEARCH_PASSWORD
    index_name: str = OPENSEARCH_INDEX
    request_timeout: int = OPENSEARCH_REQUEST_TIMEOUT
    use_ssl: bool = OPENSEARCH_USE_SSL
    verify_certs: bool = OPENSEARCH_VERIFY_CERTS
    ssl_show_warnings: bool = OPENSEARCH_SSL_WARNINGS


@dataclass
class OpenSearchResponse:
    """Opensearch response container."""

    raw_response: Mapping[str, Any]
    request_time_ms: int


class OpenSearchEncoder(json.JSONEncoder):
    """Special json encoder for OpenSearch types"""

    def default(self, obj):
        """Override"""
        return _JSON_SERIALIZER.default(obj)


class OpenSearchConnection:
    """OpenSearch connection helper, allows query based on config."""

    def __init__(
        self,
        opensearch_config: OpenSearchConfig,
    ):
        self._opensearch_config = opensearch_config
        self._opensearch_connection: Optional[OpenSearch] = None

    def query(
        self,
        search_request_body: SearchRequestBody,
        opensearch_internal_config: OpenSearchQueryConfig,
        preference: Optional[str],
    ) -> SearchResponseBody:
        """Build & make an OpenSearch query based on the given request body."""

        opensearch_request = build_opensearch_request_body(
            search_request=search_request_body,
            opensearch_internal_config=opensearch_internal_config,
        )
        opensearch_response_body = self.raw_query(opensearch_request.query, preference)

        if opensearch_request.mode == QueryMode.SEARCH:
            return process_search_response_body(
                opensearch_response_body,
                limit=search_request_body.limit,
                offset=search_request_body.offset,
            )

        if opensearch_request.mode == QueryMode.BROWSE:
            return process_browse_response_body(
                opensearch_response_body,
            )

        raise RuntimeError(
            f"Could not execute unknown query type: {opensearch_request.mode}"
        )

    def raw_query(
        self,
        request_body: Mapping[str, Any],
        preference: Optional[str],
    ) -> OpenSearchResponse:
        """Query the configured OpenSearch instance with a JSON OpenSearch body."""

        if self._opensearch_connection is None:
            login_details = (
                self._opensearch_config.username,
                self._opensearch_config.password,
            )
            self._opensearch_connection = OpenSearch(
                [self._opensearch_config.url],
                http_auth=login_details,
                use_ssl=self._opensearch_config.use_ssl,
                veriy_certs=self._opensearch_config.verify_certs,
                ssl_show_warn=self._opensearch_config.ssl_show_warnings,
            )

        start = time.time_ns()
        response = self._opensearch_connection.search(
            body=request_body,
            index=self._opensearch_config.index_name,
            request_timeout=self._opensearch_config.request_timeout,
            preference=preference,
        )
        end = time.time_ns()
        search_request_time = round((end - start) / 1e6)

        _LOGGER.info(
            "Search request completed",
            extra={
                "props": {
                    "search_request": json.dumps(request_body, cls=OpenSearchEncoder),
                    "search_request_time": search_request_time,
                },
            },
        )

        return OpenSearchResponse(
            raw_response=response,
            request_time_ms=search_request_time,
        )


def _year_range_filter(
    year_range: Tuple[Optional[int], Optional[int]]
) -> Optional[Dict[str, Any]]:
    """Get an Opensearch filter for year range.

    The filter returned is between the first term of `year_range` and the last term,
    and is inclusive. Either value can be set to None to only apply one year constraint.
    """

    policy_year_conditions = {}
    if year_range[0] is not None:
        policy_year_conditions["gte"] = f"01/01/{year_range[0]}"
    if year_range[1] is not None:
        policy_year_conditions["lte"] = f"31/12/{year_range[1]}"

    if policy_year_conditions:
        return {"range": {"document_date": policy_year_conditions}}

    return None


class QueryBuilder:
    """Helper class for building OpenSearch queries."""

    def __init__(self, config: OpenSearchQueryConfig):
        self._config = config
        self._mode: Optional[QueryMode] = None
        self._request_body: Dict[str, Any] = {}

    @property
    def query(self) -> Mapping[str, Any]:
        """Property to allow access to the build request body."""

        return self._request_body

    @property
    def mode(self) -> Optional[QueryMode]:
        """Property to allow access to the query mode for the configured request."""

        return self._mode

    def _with_search_term_base(self):
        if self._mode is not None:
            raise RuntimeError("Query base has already been configured")
        self._mode = QueryMode.SEARCH
        self._request_body = {
            "size": 0,  # only return aggregations
            "query": {
                "bool": {
                    "should": [],
                    "minimum_should_match": 1,
                },
            },
            "aggs": {
                "sample": {
                    "sampler": {
                        "shard_size": self._config.n_passages_to_sample_per_shard
                    },
                    "aggs": {
                        "top_docs": {
                            "terms": {
                                "field": OPENSEARCH_INDEX_INDEX_KEY,
                                "order": {"top_hit": _DEFAULT_SORT_ORDER.value},
                                "size": self._config.max_doc_count,
                            },
                            "aggs": {
                                "top_passage_hits": {
                                    "top_hits": {
                                        "_source": {
                                            "excludes": [
                                                "text_embedding",
                                                OPENSEARCH_INDEX_DESCRIPTION_EMBEDDING_KEY,
                                            ]
                                        },
                                        "size": self._config.max_passages_per_doc,
                                    },
                                },
                                "top_hit": {"max": {"script": {"source": "_score"}}},
                                _SORT_FIELD_MAP[SortField.DATE]: {
                                    "stats": {
                                        "field": _SORT_FIELD_MAP[SortField.DATE],
                                    },
                                },
                            },
                        },
                    },
                },
                "no_unique_docs": {"cardinality": {"field": "document_name_and_id"}},
            },
        }

    def _with_browse_base(self):
        if self._mode is not None:
            raise RuntimeError("Query base has already been configured")
        self._mode = QueryMode.BROWSE
        self._request_body = {
            "from": 0,
            "size": 10,
            "_source": {
                "excludes": ["document_description_embedding"],
            },
            "sort": {
                _SORT_FIELD_MAP[_DEFAULT_BROWSE_SORT_FIELD]: {
                    "order": _DEFAULT_SORT_ORDER.value,
                },
            },
            "query": {
                "bool": {
                    "must": [
                        {"exists": {"field": "for_search_document_description"}},
                    ],
                },
            },
        }

    def with_semantic_query(self, query_string: str):
        """Configure the query to search semantically for a given query string."""

        embedding = _ENCODER.encode(query_string)
        self._with_search_term_base()
        self._request_body["query"]["bool"]["should"] = [
            {
                "bool": {
                    "should": [
                        {
                            "match": {
                                OPENSEARCH_INDEX_NAME_KEY: {
                                    "query": query_string,
                                }
                            }
                        },
                        {
                            "match_phrase": {
                                OPENSEARCH_INDEX_NAME_KEY: {
                                    "query": query_string,
                                    "boost": 2,  # TODO: configure?
                                }
                            }
                        },
                    ],
                    "boost": self._config.name_boost,
                }
            },
            {
                "bool": {
                    "should": [
                        {
                            "match": {
                                OPENSEARCH_INDEX_DESCRIPTION_KEY: {
                                    "query": query_string,
                                    "boost": 3,  # TODO: configure?
                                }
                            }
                        },
                        {
                            "function_score": {
                                "query": {
                                    "knn": {
                                        OPENSEARCH_INDEX_DESCRIPTION_EMBEDDING_KEY: {
                                            "vector": embedding,
                                            "k": self._config.k,
                                        },
                                    },
                                },
                                "min_score": self._config.lucene_threshold,
                            }
                        },
                    ],
                    "minimum_should_match": 1,
                    "boost": self._config.description_boost,
                },
            },
            {
                "bool": {
                    "should": [
                        {
                            "match": {
                                "text": {
                                    "query": query_string,
                                },
                            }
                        },
                        {
                            "function_score": {
                                "query": {
                                    "knn": {
                                        "text_embedding": {
                                            "vector": embedding,
                                            "k": self._config.k,
                                        },
                                    },
                                },
                                "min_score": self._config.lucene_threshold,
                            }
                        },
                    ],
                    "minimum_should_match": 1,
                    "boost": self._config.embedded_text_boost,
                }
            },
        ]

    def with_exact_query(self, query_string: str):
        """Configure the query to search for an exact match to a given query string."""

        self._with_search_term_base()
        self._request_body["query"]["bool"]["should"] = [
            # Document title matching
            {
                "match_phrase": {
                    OPENSEARCH_INDEX_NAME_KEY: {
                        "query": query_string,
                        "boost": self._config.name_boost,
                    },
                }
            },
            # Document description matching
            {
                "match_phrase": {
                    OPENSEARCH_INDEX_DESCRIPTION_KEY: {
                        "query": query_string,
                        "boost": self._config.description_boost,
                    },
                }
            },
            # Text passage matching
            {
                "match_phrase": {
                    "text": {
                        "query": query_string,
                    },
                }
            },
        ]

    def with_browse_query(self):
        """Configure the query to browse documents according to supplied filters."""
        self._with_browse_base()

    def with_keyword_filter(self, field: FilterField, values: List[str]):
        """Add a keyword filter to the configured query."""

        filters = self._request_body["query"]["bool"].get("filter") or []
        filters.append({"terms": {_FILTER_FIELD_MAP[field]: values}})
        self._request_body["query"]["bool"]["filter"] = filters

    def with_year_range_filter(self, year_range: Tuple[Optional[int], Optional[int]]):
        """Add a year range filter to the configured query."""

        year_range_filter = _year_range_filter(year_range)
        if year_range_filter is not None:
            filters = self._request_body["query"]["bool"].get("filter") or []
            filters.append(year_range_filter)
            self._request_body["query"]["bool"]["filter"] = filters

    def with_search_order(self, field: SortField, order: SortOrder):
        """Set sort order for search results."""
        if self._mode != QueryMode.SEARCH:
            raise RuntimeError(
                "Cannot configure search sort ordering for non-search mode."
            )

        terms_field = self._request_body["aggs"]["sample"]["aggs"]["top_docs"]["terms"]

        if field == SortField.DATE:
            terms_field["order"] = {f"{_SORT_FIELD_MAP[field]}.avg": order.value}
        elif field == SortField.TITLE:
            terms_field["order"] = {"_key": order.value}
        else:
            raise RuntimeError(f"Unknown sort ordering field: {field}")

    def with_browse_order(self, field: SortField, order: SortOrder):
        """Set sort order for browse results."""
        if self._mode != QueryMode.BROWSE:
            raise RuntimeError(
                "Cannot configure browse sort ordering for non-browse mode."
            )

        if field in _SORT_FIELD_MAP:
            self._request_body["sort"] = {
                _SORT_FIELD_MAP[field]: {
                    "order": order.value,
                },
            }
        else:
            raise RuntimeError(f"Unknown sort ordering field: {field}")

    def with_browse_limit(self, limit: int):
        """Set result limit for browse results."""
        if self._mode != QueryMode.BROWSE:
            raise RuntimeError("Cannot configure limit when not in browse mode.")
        self._request_body["size"] = limit

    def with_browse_offset(self, offset: int):
        """Set result offset for browse results."""
        if self._mode != QueryMode.BROWSE:
            raise RuntimeError("Cannot configure offset when not in browse mode.")
        self._request_body["from"] = offset

    def with_required_fields(self, required_fields: Sequence[str]):
        """Ensure that required fields are present in opensearch responses."""
        must_clause = self._request_body["query"]["bool"].get("must") or []
        must_clause.extend(
            [{"exists": {"field": field_name}} for field_name in required_fields]
        )
        self._request_body["query"]["bool"]["must"] = must_clause


def build_opensearch_request_body(
    search_request: SearchRequestBody,
    opensearch_internal_config: Optional[OpenSearchQueryConfig] = None,
) -> QueryBuilder:
    """Build a complete OpenSearch request body."""

    search_config = opensearch_internal_config or OpenSearchQueryConfig(
        max_passages_per_doc=search_request.max_passages_per_doc,
    )
    builder = QueryBuilder(search_config)

    if search_request.query_string:
        if search_request.exact_match:
            builder.with_exact_query(search_request.query_string)
        else:
            builder.with_semantic_query(search_request.query_string)

        if search_request.sort_field is not None:
            builder.with_search_order(
                search_request.sort_field,
                search_request.sort_order or _DEFAULT_SORT_ORDER,
            )
    else:
        builder.with_browse_query()

        should_update_browse_order = (
            search_request.sort_field is not None
            or search_request.sort_order is not None
        )
        if should_update_browse_order:
            builder.with_browse_order(
                search_request.sort_field or _DEFAULT_BROWSE_SORT_FIELD,
                search_request.sort_order or _DEFAULT_SORT_ORDER,
            )

        if search_request.limit is not None:
            builder.with_browse_limit(search_request.limit)

        if search_request.offset is not None:
            builder.with_browse_offset(search_request.offset)

    if _REQUIRED_FIELDS:
        builder.with_required_fields(_REQUIRED_FIELDS)

    if search_request.keyword_filters is not None:
        for keyword, values in search_request.keyword_filters.items():
            builder.with_keyword_filter(keyword, values)

    if search_request.year_range is not None:
        builder.with_year_range_filter(search_request.year_range)

    return builder


def process_search_response_body(
    opensearch_response_body: OpenSearchResponse,
    limit: int = 10,
    offset: int = 0,
) -> SearchResponseBody:
    opensearch_json_response = opensearch_response_body.raw_response
    search_response = SearchResponseBody(
        hits=opensearch_json_response["aggregations"]["no_unique_docs"]["value"],
        query_time_ms=opensearch_response_body.request_time_ms,
        documents=[],
    )
    search_response_document = None

    result_docs = opensearch_json_response["aggregations"]["sample"]["top_docs"][
        "buckets"
    ]
    for result_doc in result_docs[offset : offset + limit]:
        for document_match in result_doc["top_passage_hits"]["hits"]["hits"]:
            document_match_source = document_match["_source"]
            if OPENSEARCH_INDEX_NAME_KEY in document_match_source:
                # Validate as a title match
                name_match = OpenSearchResponseNameMatch(**document_match_source)
                if search_response_document is None:
                    search_response_document = create_search_response_document(
                        name_match
                    )
                search_response_document.document_title_match = True
            elif OPENSEARCH_INDEX_DESCRIPTION_KEY in document_match_source:
                # Validate as a description match
                desc_match = OpenSearchResponseDescriptionMatch(**document_match_source)
                if search_response_document is None:
                    search_response_document = create_search_response_document(
                        desc_match
                    )
                search_response_document.document_description_match = True
            elif OPENSEARCH_INDEX_TEXT_BLOCK_KEY in document_match_source:
                # Process as a text block
                passage_match = OpenSearchResponsePassageMatch(**document_match_source)
                if search_response_document is None:
                    search_response_document = create_search_response_document(
                        passage_match
                    )

                response_passage = SearchResponseDocumentPassage(
                    text=passage_match.text,
                    text_block_id=passage_match.text_block_id,
                    text_block_page=passage_match.text_block_page + 1,
                    text_block_coords=passage_match.text_block_coords,
                )
                search_response_document.document_passage_matches.append(
                    response_passage
                )
            else:
                raise RuntimeError("Unexpected data in match results")

        if search_response_document is None:
            raise RuntimeError("Unexpected document match with no matching passages")

        search_response.documents.append(search_response_document)
        search_response_document = None

    return search_response


def process_browse_response_body(
    opensearch_response_body: OpenSearchResponse,
) -> SearchResponseBody:
    opensearch_json_response = opensearch_response_body.raw_response
    search_response = SearchResponseBody(
        hits=opensearch_json_response["hits"]["total"]["value"],
        query_time_ms=opensearch_response_body.request_time_ms,
        documents=[],
    )

    result_docs = opensearch_json_response["hits"]["hits"]
    for result_doc in result_docs:
        search_response_document = create_search_response_document(
            OpenSearchResponseDescriptionMatch(**result_doc["_source"])
        )
        search_response.documents.append(search_response_document)

    return search_response


def create_search_response_document(
    opensearch_match: OpenSearchResponseMatchBase,
):
    return SearchResponseDocument(
        document_name=opensearch_match.document_name,
        document_description=opensearch_match.document_description,
        document_country_code=opensearch_match.document_country_code,
        document_source_name=opensearch_match.document_source_name,
        document_date=opensearch_match.document_date,
        document_id=opensearch_match.document_id,
        document_country_english_shortname=opensearch_match.document_country_english_shortname,
        document_type=opensearch_match.document_type,
        document_category=opensearch_match.document_category,
        document_source_url=opensearch_match.document_source_url,
        document_url=s3_to_cdn_url(opensearch_match.document_url),
        document_content_type=content_type_from_path(opensearch_match.document_url),
        document_title_match=False,
        document_description_match=False,
        document_passage_matches=[],
    )
