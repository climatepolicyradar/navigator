import time
from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional, Tuple

from opensearchpy import OpenSearch
from sentence_transformers import SentenceTransformer

from app.core.config import (
    OPENSEARCH_INDEX_INNER_PRODUCT_THRESHOLD,
    OPENSEARCH_INDEX_MAX_DOC_COUNT,
    OPENSEARCH_INDEX_MAX_PASSAGES_PER_DOC,
    OPENSEARCH_INDEX_KNN_K_VALUE,
    OPENSEARCH_INDEX_N_PASSAGES_TO_SAMPLE_PER_SHARD,
    OPENSEARCH_INDEX_NAME_BOOST,
    OPENSEARCH_INDEX_DESCRIPTION_BOOST,
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
    OPENSEARCH_PREFERENCE,
    OPENSEARCH_USE_SSL,
    OPENSEARCH_VERIFY_CERTS,
    OPENSEARCH_SSL_WARNINGS,
)
from app.db.schemas.search import (
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

_ENCODER = SentenceTransformer(
    model_name_or_path=OPENSEARCH_INDEX_ENCODER,
    cache_folder="/models",
)
_SORT_FIELD_MAP: Mapping[SortField, str] = {
    SortField.DATE: "action_date",
    SortField.TITLE: "action_name",
}


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
    lucene_threshold: float = _innerproduct_threshold_to_lucene_threshold(
        OPENSEARCH_INDEX_INNER_PRODUCT_THRESHOLD
    )  # TODO: tune me separately for descriptions?
    max_doc_count: int = OPENSEARCH_INDEX_MAX_DOC_COUNT
    max_passages_per_doc: int = OPENSEARCH_INDEX_MAX_PASSAGES_PER_DOC
    n_passages_to_sample_per_shard = (
        OPENSEARCH_INDEX_N_PASSAGES_TO_SAMPLE_PER_SHARD
    )
    k = OPENSEARCH_INDEX_KNN_K_VALUE


@dataclass
class OpenSearchConfig:
    """Config for accessing an OpenSearch instance."""

    url: str = OPENSEARCH_URL
    username: str = OPENSEARCH_USERNAME
    password: str = OPENSEARCH_PASSWORD
    index_name: str = OPENSEARCH_INDEX
    request_timeout: int = OPENSEARCH_REQUEST_TIMEOUT
    preference: str = OPENSEARCH_PREFERENCE
    use_ssl: bool = OPENSEARCH_USE_SSL
    verify_certs: bool = OPENSEARCH_VERIFY_CERTS
    ssl_show_warnings: bool = OPENSEARCH_SSL_WARNINGS


@dataclass
class OpenSearchResponse:
    """Opensearch response container."""

    raw_response: Dict[str, Any]
    request_time_ms: int


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
    ) -> SearchResponseBody:
        """Build & make an OpenSearch query based on the given request body."""

        opensearch_request_body = build_opensearch_request_body(
            search_request=search_request_body,
            opensearch_internal_config=opensearch_internal_config,
        )

        opensearch_response_body = self.raw_query(opensearch_request_body)

        return process_opensearch_response_body(
            opensearch_response_body,
            limit=search_request_body.limit,
            offset=search_request_body.offset,
        )

    def raw_query(self, request_body: Dict[str, Any]) -> OpenSearchResponse:
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

        start = time.time()
        response = self._opensearch_connection.search(
            body=request_body,
            index=self._opensearch_config.index_name,
            request_timeout=self._opensearch_config.request_timeout,
            preference=self._opensearch_config.preference,
        )
        end = time.time()

        # TODO: Log request time:
        # f"query execution time: {round(end-start, 2)}s"

        # TODO: Log response info:
        # passage_hit_count = response['hits']['total']['value']
        # # note: 'gte' values are returned when there are more than 10,000 results by default
        # if response['hits']['total']['relation'] == "eq":
        #     passage_hit_qualifier = "exactly"
        # elif response['hits']['total']['relation'] == "gte":
        #     passage_hit_qualifier = "at least"
        # else:
        #     passage_hit_qualifier = "unknown (unexpected)"
        #
        # doc_hit_count = response['aggregations']['sample']['bucketcount']['count']
        # f"returned {passage_hit_qualifier} {passage_hit_count} passage(s) in {doc_hit_count} document(s)"

        return OpenSearchResponse(
            raw_response=response,
            request_time_ms=round(1000 * (end - start)),
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
        return {"range": {"action_date": policy_year_conditions}}

    return None


def build_opensearch_request_body(
    search_request: SearchRequestBody,
    opensearch_internal_config: Optional[OpenSearchQueryConfig] = None,
) -> Dict[str, Any]:
    """Build a complete OpenSearch request body."""

    search_config = opensearch_internal_config or OpenSearchQueryConfig(
        max_passages_per_doc=search_request.max_passages_per_doc,
    )
    builder = QueryBuilder(search_config)

    if search_request.exact_match:
        builder.with_exact_query(search_request.query_string)
    else:
        builder.with_semantic_query(search_request.query_string)

    if search_request.keyword_filters is not None:
        for keyword, values in search_request.keyword_filters.items():
            builder.with_keyword_filter(keyword, values)

    if search_request.year_range is not None:
        builder.with_year_range_filter(search_request.year_range)

    if search_request.sort_field is not None:
        builder.order_by(search_request.sort_field, search_request.sort_order)

    return builder.query


class QueryBuilder:
    """Helper class for building OpenSearch queries."""

    def __init__(self, search_config):
        self._search_config = search_config
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
                        "shard_size": self._search_config.n_passages_to_sample_per_shard
                    },
                    "aggs": {
                        "top_docs": {
                            "terms": {
                                "field": OPENSEARCH_INDEX_INDEX_KEY,
                                "order": {
                                    "top_hit": SortOrder.DESCENDING.value
                                },
                                "size": self._search_config.max_doc_count,
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
                                        "size": self._search_config.max_passages_per_doc,
                                    },
                                },
                                "top_hit": {
                                    "max": {"script": {"source": "_score"}}
                                },
                                _SORT_FIELD_MAP[SortField.DATE]: {
                                    "stats": {
                                        "field": _SORT_FIELD_MAP[
                                            SortField.DATE
                                        ],
                                    },
                                },
                            },
                        },
                        "bucketcount": {
                            "stats_bucket": {
                                "buckets_path": "top_docs._count",
                            },
                        },
                    },
                },
            },
        }

    @property
    def query(self):
        """Property to allow access to the build request body."""

        return self._request_body

    def with_semantic_query(self, query_string: str):
        """Configure the query to search semantically for a given query string."""

        embedding = _ENCODER.encode(query_string)
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
                    "boost": self._search_config.name_boost,
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
                                            "k": self._search_config.k,
                                        },
                                    },
                                },
                                "min_score": self._search_config.lucene_threshold,
                            }
                        },
                    ],
                    "minimum_should_match": 1,
                    "boost": self._search_config.description_boost,
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
                                            "k": self._search_config.k,
                                        },
                                    },
                                },
                                "min_score": self._search_config.lucene_threshold,
                            }
                        },
                    ],
                    "minimum_should_match": 1,
                }
            },
        ]

    def with_exact_query(self, query_string: str):
        """Configure the query to search for an exact match to a given query string."""

        self._request_body["query"]["bool"]["should"] = [
            # Document title matching
            {
                "match_phrase": {
                    OPENSEARCH_INDEX_NAME_KEY: {
                        "query": query_string,
                        "boost": self._search_config.name_boost,
                    },
                }
            },
            # Document description matching
            {
                "match_phrase": {
                    OPENSEARCH_INDEX_DESCRIPTION_KEY: {
                        "query": query_string,
                        "boost": self._search_config.description_boost,
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

    def with_keyword_filter(self, field: str, values: List[str]):
        """Add a keyword filter to the configured query."""

        filters = self._request_body["query"]["bool"].get("filter") or []
        filters.append({"terms": {field: values}})
        self._request_body["query"]["bool"]["filter"] = filters

    def with_year_range_filter(
        self, year_range: Tuple[Optional[int], Optional[int]]
    ):
        """Add a year range filter to the configured query."""

        year_range_filter = _year_range_filter(year_range)
        if year_range_filter is not None:
            filters = self._request_body["query"]["bool"].get("filter") or []
            filters.append(year_range_filter)
            self._request_body["query"]["bool"]["filter"] = filters

    def order_by(self, field: SortField, order: SortOrder):
        """Change sort order for results."""
        terms_field = self._request_body["aggs"]["sample"]["aggs"]["top_docs"][
            "terms"
        ]
        if field == SortField.DATE:
            terms_field["order"] = {
                f"{_SORT_FIELD_MAP[field]}.avg": order.value
            }
        elif field == SortField.TITLE:
            terms_field["order"] = {"_key": order.value}
        else:
            raise RuntimeError("Unknown sort ordering field: {field}")


def process_opensearch_response_body(
    opensearch_response_body: OpenSearchResponse,
    limit: int = 10,
    offset: int = 0,
) -> SearchResponseBody:
    opensearch_json_response = opensearch_response_body.raw_response
    search_response = SearchResponseBody(
        hits=opensearch_json_response["aggregations"]["sample"]["bucketcount"][
            "count"
        ],
        query_time_ms=opensearch_response_body.request_time_ms,
        documents=[],
    )
    search_response_document = None

    result_docs = opensearch_json_response["aggregations"]["sample"][
        "top_docs"
    ]["buckets"]
    for result_doc in result_docs[offset : offset + limit]:
        for document_match in result_doc["top_passage_hits"]["hits"]["hits"]:
            document_match_source = document_match["_source"]
            if OPENSEARCH_INDEX_NAME_KEY in document_match_source:
                # Validate as a title match
                name_match = OpenSearchResponseNameMatch(
                    **document_match_source
                )
                if search_response_document is None:
                    search_response_document = create_search_response_document(
                        name_match
                    )
                search_response_document.document_title_match = True
            elif OPENSEARCH_INDEX_DESCRIPTION_KEY in document_match_source:
                # Validate as a description match
                desc_match = OpenSearchResponseDescriptionMatch(
                    **document_match_source
                )
                if search_response_document is None:
                    search_response_document = create_search_response_document(
                        desc_match
                    )
                search_response_document.document_description_match = True
            elif OPENSEARCH_INDEX_TEXT_BLOCK_KEY in document_match_source:
                # Process as a text block
                passage_match = OpenSearchResponsePassageMatch(
                    **document_match_source
                )
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
            raise RuntimeError(
                "Unexpected document match with no matching passages"
            )

        search_response.documents.append(search_response_document)
        search_response_document = None

    return search_response


def create_search_response_document(
    passage_match: OpenSearchResponseMatchBase,
):
    return SearchResponseDocument(
        document_name=passage_match.action_name,
        document_description=passage_match.action_description,
        document_country_code=passage_match.action_country_code,
        document_source_name=passage_match.action_source_name,
        document_date=passage_match.action_date,
        document_id=passage_match.document_id,
        document_geography_english_shortname=passage_match.action_geography_english_shortname,
        document_type_name=passage_match.action_type_name,
        document_title_match=False,
        document_description_match=False,
        document_passage_matches=[],
    )
