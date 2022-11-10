from enum import Enum
from typing import Mapping, Optional, Sequence

from pydantic import BaseModel, conlist


Coord = tuple[float, float]


class SortOrder(str, Enum):
    """Sort ordering for use building OpenSearch query body."""

    ASCENDING = "asc"
    DESCENDING = "desc"


class SortField(str, Enum):
    """Sort field for use building OpenSearch query body."""

    DATE = "date"
    TITLE = "title"


class JitQuery(str, Enum):
    """Flag used for determining if a jit query is to be used."""

    ENABLED = "enabled"
    DISABLED = "disabled"


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


class IncludedResults(str, Enum):
    """Filter field to exclude specific results from the search based on search indices."""

    PDFS_TRANSLATED = "pdfsTranslated"
    HTMLS_NON_TRANSLATED = "htmlsNonTranslated"
    HTMLS_TRANSLATED = "htmlsTranslated"


IncludedResultsList = Optional[conlist(IncludedResults, min_items=1)]


class SearchRequestBody(BaseModel):
    """The request body expected by the search API endpoint."""

    query_string: str
    exact_match: bool = False
    max_passages_per_doc: int = 10  # TODO: decide on default

    # TODO: Improve filters to allow generics & use filter types
    keyword_filters: Optional[Mapping[FilterField, Sequence[str]]] = None
    year_range: Optional[tuple[Optional[int], Optional[int]]] = None

    sort_field: Optional[SortField] = None
    sort_order: SortOrder = SortOrder.DESCENDING

    jit_query: Optional[JitQuery] = JitQuery.ENABLED
    include_results: IncludedResultsList = None

    limit: int = 10  # TODO: decide on default
    offset: int = 0


class SearchResponseDocumentPassage(BaseModel):
    """A Document passage match returned by the search API endpoint."""

    text: str
    text_block_id: str
    text_block_page: Optional[int]
    text_block_coords: Optional[Sequence[Coord]]


class SearchResult(BaseModel):
    """A single document in a search response."""

    document_name: str
    document_geography: str
    document_sectors: Sequence[str]
    document_source: str
    document_date: str
    document_id: str
    document_slug: str
    document_description: str
    document_type: str
    document_category: str
    document_source_url: Optional[str]
    document_url: Optional[str]
    document_content_type: Optional[str]
    document_title_match: bool
    document_description_match: bool
    document_passage_matches: list[SearchResponseDocumentPassage]


class SearchResultResponse(SearchResult):
    """The object that is returned in the response.

    Used to extend with postfix
    """

    document_postfix: Optional[str]


class CategoryName(str, Enum):
    """Representation of what is in the database.

    TODO: Add test to ensure there is equivalence with the initial_data
    """

    LAW = "Law"
    POLICY = "Policy"
    CASE = "Case"


Top5DocumentList = conlist(SearchResult, max_items=5)


class SummaryCountryResponse(BaseModel):
    """Additional information for the Country page over geo stats"""

    document_counts: Mapping[CategoryName, int]
    top_documents: Mapping[CategoryName, Top5DocumentList]
    targets: Sequence[str]  # TODO: Placeholder for later


class SearchResults(BaseModel):
    """The response body produced by the search API endpoint."""

    hits: int
    query_time_ms: int

    documents: list[SearchResult]


class SearchResultsResponse(BaseModel):
    """The response body produced by the search API endpoint."""

    hits: int
    query_time_ms: int

    documents: Sequence[SearchResultResponse]


class OpenSearchResponseMatchBase(BaseModel):
    """Describes matches returned by an OpenSearch query"""

    document_name: str
    document_geography: str
    document_description: str
    document_sectors: Sequence[str]
    document_source: str
    document_id: str  # Changed semantics to be import_id, not database id
    document_date: str
    document_type: str
    document_source_url: Optional[str]
    document_cdn_object: Optional[str]
    document_category: str
    document_content_type: Optional[str]
    document_slug: str


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
    text_block_coords: Sequence[Coord]
