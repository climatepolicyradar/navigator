from csv import DictReader
from io import BytesIO, TextIOWrapper

import pytest

from app.core.validation.cclw.law_policy.process_csv import (
    POSTFIX_FIELD,
    extract_documents,
    validated_input,
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
)
from app.core.validation.types import ImportSchemaMismatchError
from app.core.validation.util import get_valid_metadata
from app.db.models import (
    Source,
    Geography,
    DocumentType,
    Language,
    Sector,
    Response,
    Hazard,
    Framework,
    Instrument,
    Category,
    Keyword,
)


CCLW_FIELDNAMES = [
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


INVALID_CSV_MISSING_HEADERS = (
    f"{POSTFIX_FIELD},{ACTION_ID_FIELD},{CATEGORY_FIELD},{COUNTRY_CODE_FIELD},{DESCRIPTION_FIELD},"
    f"{DOCUMENT_FIELD},{DOCUMENT_ID_FIELD},{DOCUMENT_TYPE_FIELD},{EVENTS_FIELD},"
    f"{FRAMEWORKS_FIELD},{GEOGRAPHY_FIELD},{HAZARDS_FIELD},{INSTRUMENTS_FIELD},"
    f"{KEYWORDS_FIELD},{PARENT_LEGISLATION_FIELD},{SECTORS_FIELD},"
    f"{TITLE_FIELD},{TOPICS_FIELD},{YEAR_FIELD}\n"
)
MISSING_HEADERS = [LANGUAGES_FIELD]
INVALID_CSV_EXTRA_HEADERS = (
    f"{POSTFIX_FIELD},{ACTION_ID_FIELD},{CATEGORY_FIELD},{COUNTRY_CODE_FIELD},{DESCRIPTION_FIELD},"
    f"{DOCUMENT_FIELD},sneaky,{DOCUMENT_ID_FIELD},{DOCUMENT_TYPE_FIELD},{EVENTS_FIELD},"
    f"{FRAMEWORKS_FIELD},{GEOGRAPHY_FIELD},{HAZARDS_FIELD},{INSTRUMENTS_FIELD},"
    f"{KEYWORDS_FIELD},{LANGUAGES_FIELD},{PARENT_LEGISLATION_FIELD},{SECTORS_FIELD},"
    f"{TITLE_FIELD},{TOPICS_FIELD},extra,{YEAR_FIELD}\n"
)
EXTRA_HEADERS = ["sneaky", "extra"]
INVALID_CSV_MIXED_ERRORS = (
    f"{POSTFIX_FIELD},{ACTION_ID_FIELD},{CATEGORY_FIELD},{COUNTRY_CODE_FIELD},{DESCRIPTION_FIELD},"
    f"{DOCUMENT_FIELD},{DOCUMENT_ID_FIELD},{DOCUMENT_TYPE_FIELD},{EVENTS_FIELD},"
    f"{FRAMEWORKS_FIELD},sneaky,{GEOGRAPHY_FIELD},{HAZARDS_FIELD},{INSTRUMENTS_FIELD},"
    f"{KEYWORDS_FIELD},{PARENT_LEGISLATION_FIELD},{SECTORS_FIELD},"
    f"{TITLE_FIELD},extra,{TOPICS_FIELD},{YEAR_FIELD}\n"
)
VALID_CSV_HEADER = (
    f"{POSTFIX_FIELD},{ACTION_ID_FIELD},{DOCUMENT_ID_FIELD},{TITLE_FIELD},{DESCRIPTION_FIELD},"
    f"{COUNTRY_CODE_FIELD},{DOCUMENT_FIELD},{CATEGORY_FIELD},{EVENTS_FIELD},"
    f"{SECTORS_FIELD},{INSTRUMENTS_FIELD},{FRAMEWORKS_FIELD},{TOPICS_FIELD},"
    f"{HAZARDS_FIELD},{DOCUMENT_TYPE_FIELD},{YEAR_FIELD},{LANGUAGES_FIELD},"
    f"{KEYWORDS_FIELD},{GEOGRAPHY_FIELD},{PARENT_LEGISLATION_FIELD}\n"
)


@pytest.mark.parametrize(
    "csv_header_line,expected_missing,expected_extra",
    [
        (INVALID_CSV_MISSING_HEADERS, MISSING_HEADERS, []),
        (INVALID_CSV_EXTRA_HEADERS, [], EXTRA_HEADERS),
        (INVALID_CSV_MIXED_ERRORS, MISSING_HEADERS, EXTRA_HEADERS),
    ],
)
def test_validated_input__invalid(csv_header_line, expected_missing, expected_extra):
    with pytest.raises(ImportSchemaMismatchError) as e:
        csv_file = TextIOWrapper(BytesIO(csv_header_line.encode("utf8")))
        validated_input(csv_file)

    assert e.value.details == {
        "unexpected_fields": expected_extra,
        "missing_fields": expected_missing,
    }


def test_validated_input__valid():
    csv_file = TextIOWrapper(BytesIO(VALID_CSV_HEADER.encode("utf8")))
    validated_csv_file = validated_input(csv_file)
    assert isinstance(validated_csv_file, DictReader)
    assert validated_csv_file.fieldnames is not None
    assert set(validated_csv_file.fieldnames) == set(CCLW_FIELDNAMES)


INVALID_LINE_1 = (
    ",1,2,name,description,GEO,https://dave|en,executive,01/01/2014|Approved||,"
    "unknown_sector,instrument,framework,topic,hazard,doctype,2014,language,"
    "unknown_keyword,geography\n"
)
INVALID_LINE_1_ERRORS = {
    "sectors": ["unknown_sector"],
    "keywords": ["unknown_keyword"],
}
INVALID_FILE_1 = VALID_CSV_HEADER + INVALID_LINE_1


def test_extract_documents_invalid(test_db):
    # ensure metadata exists
    test_db.add(Source(name="CCLW"))
    test_db.add(
        Geography(
            display_value="geography", slug="geography", value="GEO", type="country"
        )
    )
    test_db.add(DocumentType(name="doctype", description="doctype"))
    test_db.add(Language(language_code="LAN", name="language"))
    test_db.add(Category(name="executive", description="executive"))
    test_db.add(Keyword(name="keyword", description="keyword"))
    test_db.add(Hazard(name="hazard", description="hazard"))
    test_db.add(Response(name="topic", description="topic"))
    test_db.add(Framework(name="framework", description="framework"))

    test_db.commit()

    test_db.add(Instrument(name="instrument", description="instrument", source_id=1))
    test_db.add(Sector(name="sector", description="sector", source_id=1))

    test_db.commit()

    csv_file = TextIOWrapper(BytesIO(INVALID_FILE_1.encode("utf8")))
    validated_files = list(
        extract_documents(
            csv_reader=validated_input(csv_file),
            valid_metadata=get_valid_metadata(test_db),
        )
    )
    assert len(validated_files) == 1
    assert validated_files[0].errors == INVALID_LINE_1_ERRORS


VALID_LINE_1 = (
    "pf1,1,2,name1,description1,GEO,https://dave|en,executive,01/01/2014|Approved||,"
    "sector,instrument,framework,topic,hazard1,doctype,2014,language,"
    "keyword1,geography\n"
)
VALID_LINE_2 = (
    "pf2,2,33,name2,description2,GEO,https://steve|en,executive,25/12/2015|Approved||,"
    "sector,instrument,framework,topic,hazard1;hazard2,doctype,2015,language,"
    "keyword1;keyword2,geography\n"
)
VALID_FILE_1 = VALID_CSV_HEADER + VALID_LINE_1 + VALID_LINE_2


def test_extract_documents_valid(test_db):
    # ensure metadata exists
    test_db.add(Source(name="CCLW"))
    test_db.add(
        Geography(
            display_value="geography", slug="geography", value="GEO", type="country"
        )
    )
    test_db.add(DocumentType(name="doctype", description="doctype"))
    test_db.add(Language(language_code="LAN", name="language"))
    test_db.add(Category(name="executive", description="executive"))
    test_db.add(Keyword(name="keyword1", description="keyword1"))
    test_db.add(Keyword(name="keyword2", description="keyword2"))
    test_db.add(Hazard(name="hazard1", description="hazard1"))
    test_db.add(Hazard(name="hazard2", description="hazard2"))
    test_db.add(Response(name="topic", description="topic"))
    test_db.add(Framework(name="framework", description="framework"))

    test_db.commit()

    test_db.add(Instrument(name="instrument", description="instrument", source_id=1))
    test_db.add(Sector(name="sector", description="sector", source_id=1))

    test_db.commit()

    csv_file = TextIOWrapper(BytesIO(VALID_FILE_1.encode("utf8")))
    validated_files = list(
        extract_documents(
            csv_reader=validated_input(csv_file),
            valid_metadata=get_valid_metadata(test_db),
        )
    )
    assert len(validated_files) == 2
    assert validated_files[0].create_request.postfix == "pf1"
    assert validated_files[0].create_request.source_url == "https://dave"
    assert validated_files[0].create_request.keywords == ["keyword1"]
    assert validated_files[0].create_request.hazards == ["hazard1"]
    assert validated_files[1].create_request.postfix == "pf2"
    assert validated_files[1].create_request.source_url == "https://steve"
    assert validated_files[1].create_request.keywords == ["keyword1", "keyword2"]
    assert validated_files[1].create_request.hazards == ["hazard1", "hazard2"]
