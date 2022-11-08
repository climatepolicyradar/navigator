import logging
from csv import DictReader
from datetime import datetime
from enum import Enum
from html.parser import HTMLParser
from io import StringIO, TextIOWrapper
from typing import (
    Collection,
    Generator,
    Mapping,
    Optional,
    Sequence,
    TypeVar,
)

from app.api.api_v1.schemas.document import DocumentCreateRequest, Event
from app.core.validation.types import (
    DocumentValidationResult,
    ImportSchemaMismatchError,
)

_LOGGER = logging.getLogger(__file__)

ACTION_ID_FIELD = "Id"
CATEGORY_FIELD = "Category"
COUNTRY_CODE_FIELD = "Geography ISO"
DESCRIPTION_FIELD = "Description"
DOCUMENT_FIELD = "Documents"
DOCUMENT_ID_FIELD = "Document Id"
DOCUMENT_TYPE_FIELD = "Document Type"
EVENTS_FIELD = "Events"
FRAMEWORKS_FIELD = "Frameworks"
GEOGRAPHY_FIELD = "Geography"
HAZARDS_FIELD = "Natural Hazards"
INSTRUMENTS_FIELD = "Instruments"
KEYWORDS_FIELD = "Keywords"
LANGUAGES_FIELD = "Language"
PARENT_LEGISLATION_FIELD = "Parent Legislation"
SECTORS_FIELD = "Sectors"
TITLE_FIELD = "Title"
TOPICS_FIELD = "Responses"
YEAR_FIELD = "Year"
POSTFIX_FIELD = "Display comment"

_EXPECTED_FIELDS = set(
    [
        ACTION_ID_FIELD,
        CATEGORY_FIELD,
        COUNTRY_CODE_FIELD,
        DESCRIPTION_FIELD,
        DOCUMENT_FIELD,
        DOCUMENT_ID_FIELD,
        DOCUMENT_TYPE_FIELD,
        EVENTS_FIELD,
        FRAMEWORKS_FIELD,
        GEOGRAPHY_FIELD,
        HAZARDS_FIELD,
        INSTRUMENTS_FIELD,
        KEYWORDS_FIELD,
        LANGUAGES_FIELD,
        PARENT_LEGISLATION_FIELD,
        SECTORS_FIELD,
        TITLE_FIELD,
        TOPICS_FIELD,
        YEAR_FIELD,
        POSTFIX_FIELD,
    ]
)

CCLW_SOURCE = "CCLW"
META_CATEGORY_KEY = "categories"
META_DOC_TYPE_KEY = "document_types"
META_FRAMEWORK_KEY = "frameworks"
META_GEOGRAPHY_KEY = "geographies"
META_HAZARD_KEY = "hazards"
META_INSTRUMENT_KEY = "instruments"
META_KEYWORD_KEY = "keywords"
META_LANGUAGE_KEY = "languages"
META_SECTOR_KEY = "sectors"
META_SOURCE_KEY = "sources"
META_TOPIC_KEY = "topics"

# TODO: Remove cleanup when a validated form exists for adding keywords to documents.
#    This code exists only to clean up known issues with legacy data.
CLEANUP_KEYWORDS_MAP = {
    "5 G": "5G",
    "Brt": "BRT",
    "Bus": "Buses",
    "Cap And Trade": "Cap and Trade",
    "Carbon Capture And Storage": "Carbon Capture and Storage",
    "Cbdr": "CBDR",
    "Cc Gap": "CCGAP",
    "Ccs": "CCS",
    "Cdm": "CDM",
    "Co Benefits": "Co-benefits",
    "Cogeneration": "Co-generation",
    "Covid 19": "COVID-19",
    "Covid-19": "COVID-19",
    "Covid19": "COVID-19",
    "Drr": "DRR",
    "E Buses": "E-Buses",
    "E Vs": "EVs",
    "EV": "EVs",
    "Energy storage": "Energy Storage",
    "Ets": "ETS",
    "Ev": "EVs",
    "Fit": "FIT",
    "Forest": "Forests",
    "Ghg": "GHG",
    "Hf Cs": "Hydrofluorocarbons",
    "Human rights": "Human Rights",
    "K Ets": "K-ETS",
    "Lulucf": "LULUCF",
    "Mrv": "MRV",
    "Multi Modal Transport": "Multi-Modal Transport",
    "Nap": "NAP",
    "Pv": "PV",
    "Redd+ And Lulucf": "REDD+ And LULUCF",
    "S Olar": "Solar",
    "Sd Gs": "SDGs",
    "Slc Ps": "SLCPs",
    "Taxes": "Tax",
    "Transportation": "Transport",
    "Unfccc": "UNFCCC",
    "air pollution": "Air Pollution",
    "carbon sink": "Carbon Sink",
    "climate justice": "Climate Justice",
    "climate security": "Climate Security",
    "clothing": "Clothing",
    "coal": "Coal",
    "covid19": "COVID-19",
    "food waste": "Food Waste",
    "fossil fuels curbing measures": "Fossil Fuels Curbing Measures",
    "housing": "Housing",
    "taxonomy": "Taxonomy",
    "travel": "Travel",
    "wetlands": "Wetlands",
}

DEFAULT_POLICY_DATE = datetime(1900, 1, 1)
PUBLICATION_EVENT_NAME = "Publication"

CONTENT_TYPE_PDF = "application/pdf"
CONTENT_TYPE_DOCX = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)
CONTENT_TYPE_HTML = "text/html"

SINGLE_FILE_CONTENT_TYPES = {
    CONTENT_TYPE_PDF,
    CONTENT_TYPE_DOCX,
}
MULTI_FILE_CONTENT_TYPES = {CONTENT_TYPE_HTML}
SUPPORTED_CONTENT_TYPES = SINGLE_FILE_CONTENT_TYPES | MULTI_FILE_CONTENT_TYPES


class _LawPolicyDocumentType(str, Enum):
    """Document types supported by the backend API."""

    LAW = "Law"
    POLICY = "Policy"


CATEGORY_MAPPING = {
    "executive": _LawPolicyDocumentType.POLICY,
    "legislative": _LawPolicyDocumentType.LAW,
}


def _split_not_null(input_string: str, split_char: str) -> Sequence[str]:
    return [s.strip() for s in input_string.strip().split(split_char) if s]


def _extract_events(events_str: str) -> Sequence[Event]:
    events = []
    for event_string in _split_not_null(events_str, ";"):
        event_parts = event_string.split("|")
        date_str = event_parts[0]
        event_date = datetime.strptime(date_str, "%d/%m/%Y")
        event_name = event_parts[1]
        events.append(Event(name=event_name, description="", created_ts=event_date))
    return events


def validated_input(csv_file: TextIOWrapper) -> DictReader:
    """
    Checks an input file for the correct provided headers.

    :param TextIOWrapper csv_file: a file object to be processed as a CSV containing
        document specifications
    :returns DictReader: A csv.DictReader object for reading document specifications
    :raises
    """
    csv_reader = DictReader(csv_file)

    csv_fields = csv_reader.fieldnames
    if csv_fields is None:
        raise ImportSchemaMismatchError(message="File is empty", details={})

    unexpected_fields = [f for f in csv_fields if f not in _EXPECTED_FIELDS]
    missing_fields = [f for f in _EXPECTED_FIELDS if f not in set(csv_fields)]
    if unexpected_fields or missing_fields:
        raise ImportSchemaMismatchError(
            message="Provided CSV fields do not match those expected",
            details={
                "unexpected_fields": unexpected_fields,
                "missing_fields": missing_fields,
            },
        )

    return csv_reader


_ValidMetadata = Mapping[str, Mapping[str, Collection[str]]]


def import_id_from_csv_row(row: Mapping[str, str]) -> str:
    return f"CCLW.{row[CATEGORY_FIELD].strip()}.{row[ACTION_ID_FIELD].strip()}.{row[DOCUMENT_ID_FIELD].strip()}"


def extract_documents(
    csv_reader: DictReader,
    valid_metadata: _ValidMetadata,
) -> Generator[DocumentValidationResult, None, None]:
    """
    Validate the given CSV, generating document objects to be loaded

    :param DictReader csv_reader: a CSV file reader from which to read document
        specifications
    :param _ValidMetadata valid_metadata: a mapping specifying all the metadata values
        known for each known input type
    """
    valid_cclw_metadata = valid_metadata[CCLW_SOURCE]
    row_index = 1
    for row in csv_reader:
        errors_encountered: dict[str, Collection[str]] = {}

        country_code = _validated_values(
            valid_cclw_metadata,
            META_GEOGRAPHY_KEY,
            row[COUNTRY_CODE_FIELD].strip(),
            errors_encountered,
        )
        presented_category = row[CATEGORY_FIELD].strip()
        if presented_category in CATEGORY_MAPPING:
            document_category = CATEGORY_MAPPING[presented_category].value
        else:
            document_category = presented_category
            errors_encountered[META_CATEGORY_KEY] = [presented_category]

        year = row[YEAR_FIELD].strip()
        document_name = row[TITLE_FIELD].strip()
        document_description = _strip_tags(row[DESCRIPTION_FIELD])
        import_id = import_id_from_csv_row(row)
        document_url = _parse_url(row[DOCUMENT_FIELD])
        document_languages = _validated_values(
            valid_cclw_metadata,
            META_LANGUAGE_KEY,
            _split_not_null(row[LANGUAGES_FIELD], ";"),
            errors_encountered,
        )

        document_type = _validated_values(
            valid_cclw_metadata,
            META_DOC_TYPE_KEY,
            row[DOCUMENT_TYPE_FIELD].strip(),
            errors_encountered,
        )
        events = _extract_events(row[EVENTS_FIELD])
        sectors = _validated_values(
            valid_cclw_metadata,
            META_SECTOR_KEY,
            _split_not_null(row[SECTORS_FIELD], ";"),
            errors_encountered,
        )
        instruments = _validated_values(
            valid_cclw_metadata,
            META_INSTRUMENT_KEY,
            _split_not_null(row[INSTRUMENTS_FIELD], ";"),
            errors_encountered,
        )
        frameworks = _validated_values(
            valid_cclw_metadata,
            META_FRAMEWORK_KEY,
            _split_not_null(row[FRAMEWORKS_FIELD], ";"),
            errors_encountered,
        )
        topics = _validated_values(
            valid_cclw_metadata,
            META_TOPIC_KEY,
            _split_not_null(row[TOPICS_FIELD], ";"),
            errors_encountered,
        )
        hazards = _validated_values(
            valid_cclw_metadata,
            META_HAZARD_KEY,
            _split_not_null(row[HAZARDS_FIELD], ";"),
            errors_encountered,
        )
        keywords = _validated_values(
            valid_cclw_metadata,
            META_KEYWORD_KEY,
            _apply_map(CLEANUP_KEYWORDS_MAP, _split_not_null(row[KEYWORDS_FIELD], ";")),
            errors_encountered,
        )
        if errors_encountered:
            _LOGGER.error(
                f"Invalid data found for document with id 'CCLW:{import_id}'. "
                f"Invalid metadata values: '{errors_encountered}'"
            )

        publication_date = _calculate_publication_date(
            events=events,
            override_year=year,
        )
        postfix = row[POSTFIX_FIELD].strip()

        yield DocumentValidationResult(
            row=row_index,
            import_id=import_id,
            create_request=DocumentCreateRequest(
                name=document_name,
                description=document_description,
                postfix=postfix,
                source_url=document_url,
                import_id=import_id,
                publication_ts=publication_date,
                languages=document_languages,
                type=document_type,
                source=CCLW_SOURCE,
                category=document_category,
                geography=country_code,
                frameworks=frameworks,
                instruments=instruments,
                topics=topics,
                keywords=keywords,
                hazards=hazards,
                sectors=sectors,
                events=events,
            ),
            errors=errors_encountered,
        )
        row_index += 1


def _calculate_publication_date(
    events: Sequence[Event],
    override_year: str,
) -> datetime:
    """
    Calculate the publication date from a sequence of events and a given fallback year.

    Calculates the publication date of a document according to the following heuristic:
        - The date of a "Publication" event if present
        - The earliest event if no "Publication" event is found
        - The first of January on the given fallback year if no events are present
        - DEFAULT_POLICY_DATE if no other useful information can be derived

    A warning will be issued if the fallback_year does not match a discovered event.

    :param Sequence[Event] events: A sequence of parsed events associated with
        the document
    :returns datetime: The calculated publication date as described by the
        heuristic above
    """
    publication_date = None

    if override_year:
        try:
            parsed_fallback_year = int(override_year.strip())
        except ValueError:
            _LOGGER.exception(f"Could not parse specified year '{override_year}'")
        else:
            publication_date = datetime(year=parsed_fallback_year, month=1, day=1)

    if publication_date is None:
        for event in events:
            if event.name.lower() == PUBLICATION_EVENT_NAME.lower():
                return event.created_ts

            if publication_date is None or event.created_ts < publication_date:
                publication_date = event.created_ts

    if publication_date is None:
        _LOGGER.warn(
            "Publication date could not be derived from input row, "
            "falling back to setting a default policy publication date."
        )

    return publication_date or DEFAULT_POLICY_DATE


def _parse_url(url: str) -> Optional[str]:
    """
    Parse a document URL.

    In addition to parsing the URL, we also:
        - convert http to https
        - Remove any delimiters (a hang-over from the original CSV)

    :param str url: An input string representing a URL
    :returns str: An updated parsed URL as a string
    """
    if not url.strip():
        return None
    return url.split("|")[0].strip().replace("http://", "https://")


class _HTMLStripper(HTMLParser):
    """Strips HTML from strings."""

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):  # noqa:D102
        self.text.write(d)

    def get_data(self):  # noqa:D102
        return self.text.getvalue()


def _strip_tags(html: str) -> str:
    s = _HTMLStripper()
    s.feed(html)
    return s.get_data()


Value = TypeVar("Value", str, Sequence[str])


def _validated_values(
    metadata_map: Mapping[str, Collection[str]],
    metadata_key: str,
    presented_values: Value,
    errors: dict[str, Collection[str]],
) -> Value:
    if isinstance(presented_values, str):
        check_presented_values = [presented_values]
    else:
        check_presented_values = presented_values
    allowed_values = metadata_map[metadata_key]
    invalid_values = [v for v in check_presented_values if v not in allowed_values]
    if invalid_values:
        errors[metadata_key] = invalid_values
    return presented_values


def _apply_map(
    value_map: Mapping[str, str], presented_values: Sequence[str]
) -> Sequence[str]:
    return [value_map.get(v, v) for v in presented_values]
