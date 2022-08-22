from enum import Enum
from typing import Dict, List, Mapping, Optional, Tuple

from pydantic import BaseModel, conlist

from app.db.schemas.metadata import Event


Coord = Tuple[float, float]


class SortOrder(str, Enum):
    """Sort ordering for use building OpenSearch query body."""

    ASCENDING = "asc"
    DESCENDING = "desc"


class SortField(str, Enum):
    """Sort field for use building OpenSearch query body."""

    DATE = "date"
    TITLE = "title"


class FilterField(str, Enum):
    """Filter field for use building OpenSearch query body."""

    SOURCE = "sources"
    COUNTRY = "countries"
    REGION = "regions"
    INSTRUMENT = "instruments"
    SECTOR = "sectors"
    TYPE = "types"
    CATEGORY = "categories"
    TOPIC = "topics"
    KEYWORD = "keywords"
    HAZARD = "hazards"
    LANGUAGE = "languages"
    FRAMEWORK = "frameworks"


class SearchRequestBody(BaseModel):
    """The request body expected by the search API endpoint."""

    query_string: str
    exact_match: bool
    max_passages_per_doc: int = 10  # TODO: decide on default

    # TODO: Improve filters to allow generics & use filter types
    keyword_filters: Optional[Dict[FilterField, List[str]]] = None
    year_range: Optional[Tuple[Optional[int], Optional[int]]] = None

    sort_field: Optional[SortField] = None
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
    document_country_english_shortname: str
    document_description: str
    document_type: str
    document_category: str
    document_source_url: str
    document_url: str
    document_content_type: str

    document_title_match: bool
    document_description_match: bool
    document_passage_matches: List[SearchResponseDocumentPassage]


class CategoryName(str, Enum):
    """Representation of what is in the database.

    TODO: Add test to ensure there is equivalence with the initial_data
    """

    LAW = "Law"
    POLICY = "Policy"
    CASE = "Case"


Top5DocumentList = conlist(SearchResponseDocument, max_items=5)


class SummaryCountryResponse(BaseModel):
    """Additional information for the Country page over geo stats"""

    document_counts: Mapping[CategoryName, int]
    top_documents: Mapping[CategoryName, Top5DocumentList]
    events: List[Event]
    targets: List[str]  # TODO: Placeholder for later


class SearchResponseBody(BaseModel):
    """The response body produced by the search API endpoint."""

    hits: int
    query_time_ms: int

    documents: List[SearchResponseDocument]


class OpenSearchResponseMatchBase(BaseModel):
    """Describes matches returned by an OpenSearch query"""

    document_name: str
    document_country_code: str
    document_description: str
    document_source_name: str
    document_id: int
    document_date: str
    document_name_and_id: str
    document_country_english_shortname: str
    document_type: str
    document_source_url: str
    document_url: str
    document_category: str


class OpenSearchResponseNameMatch(OpenSearchResponseMatchBase):
    """Describes matches returned by OpenSearch on Document name."""

    for_search_document_name: str


class OpenSearchResponseDescriptionMatch(OpenSearchResponseMatchBase):
    """Describes matches returned by OpenSearch on Document description."""

    for_search_document_description: str


class OpenSearchResponsePassageMatch(OpenSearchResponseMatchBase):
    """Describes matches returned by OpenSearch on Document passage."""

    text: str
    text_block_id: str
    text_block_page: int
    text_block_coords: List[Coord]
