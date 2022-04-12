from enum import Enum
from typing import Dict, List, Optional, Tuple

from pydantic import BaseModel


Coord = Tuple[float, float]


class SortOrder(str, Enum):
    """Sort ordering for use building OpenSearch query body."""

    ASCENDING = "asc"
    DESCENDING = "desc"


class SortField(str, Enum):
    """Sort field for use building OpenSearch query body."""

    DATE = "date"
    TITLE = "title"
    SCORE = "score"
    # TODO: complete enum


class SearchRequestBody(BaseModel):
    """The request body expected by the search API endpoint."""

    query_string: str
    exact_match: bool
    max_passages_per_doc: int = 10  # TODO: decide on default

    # TODO: Improve filters to allow generics & use filter types
    keyword_filters: Optional[Dict[str, List[str]]] = None
    year_range: Optional[Tuple[Optional[int], Optional[int]]] = None

    sort_field: SortField = SortField.DATE
    sort_order: SortOrder = SortOrder.DESCENDING

    limit: int = 10  # TODO: decide on default
    offset: int = 0


class SearchResponseDocumentPassage(BaseModel):
    """A Document passage match returned by the search API endpoint."""

    text: str
    text_block_id: str
    text_block_page: int
    text_block_coords: List[Coord]


class SearchResponseDocument(BaseModel):
    """A single document in a search response."""

    document_name: str
    document_country_code: str
    document_source_name: str
    document_date: str
    document_id: int
    document_geography_english_shortname: str
    document_description: str
    document_type_name: str

    # TODO: add PDF s3 location for serving
    # document_location: str

    document_title_match: bool
    document_description_match: bool
    document_passage_matches: List[SearchResponseDocumentPassage]


class SearchResponseBody(BaseModel):
    """The response body produced by the search API endpoint."""

    hits: int
    query_time_ms: int

    documents: List[SearchResponseDocument]


class OpenSearchResponseMatchBase(BaseModel):
    """Describes matches returned by an OpenSearch query"""

    document_name: str
    action_country_code: str
    action_description: str
    action_source_name: str
    action_id: int
    action_name: str
    action_date: str
    action_name_and_id: str
    document_id: int
    action_geography_english_shortname: str
    action_type_name: str


class OpenSearchResponseNameMatch(OpenSearchResponseMatchBase):
    """Describes matches returned by OpenSearch on Document name."""

    for_search_action_name: str


class OpenSearchResponseDescriptionMatch(OpenSearchResponseMatchBase):
    """Describes matches returned by OpenSearch on Document description."""

    for_search_action_description: str


class OpenSearchResponsePassageMatch(OpenSearchResponseMatchBase):
    """Describes matches returned by OpenSearch on Document passage."""

    text: str
    text_block_id: str
    text_block_page: int
    text_block_coords: List[Coord]
