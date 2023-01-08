from datetime import datetime, timezone

import pytest

from app.db.models import (
    Document,
    Source,
    Geography,
    DocumentType,
    Language,
    Event,
    Sector,
    Response,
    Hazard,
    Framework,
    Instrument,
    DocumentLanguage,
    Category,
    Keyword,
)
from app.api.api_v1.schemas.document import DocumentCreateRequest
from app.db.crud.document import create_document, UnknownMetadataError


def test_create_documents(client, superuser_token_headers, test_db):

    # ensure meta
    test_db.add(Source(name="may it be with you"))
    test_db.add(
        Geography(
            display_value="not my favourite subject",
            slug="not-my-favourite-subject",
            value="NMFS",
            type="country",
        )
    )
    test_db.add(DocumentType(name="just my type", description="sigh"))
    test_db.add(Language(language_code="afr", name="Afrikaans"))
    test_db.add(Category(name="a category", description="a category description"))
    test_db.add(Hazard(name="some hazard", description="Imported by CPR loader"))
    test_db.add(Response(name="Mitigation", description="Imported by CPR loader"))
    test_db.add(Framework(name="some framework", description="Imported by CPR loader"))
    test_db.add(Keyword(name="some keyword", description="Imported by CPR loader"))
    test_db.commit()

    test_db.add(
        Sector(name="Energy", description="Imported by CPR loader", source_id=1)
    )
    test_db.add(
        Instrument(
            name="some instrument", description="Imported by CPR loader", source_id=1
        )
    )
    test_db.add(
        Instrument(
            name="another instrument", description="Imported by CPR loader", source_id=1
        )
    )
    test_db.commit()

    create_request_content = {
        "publication_ts": "2000-01-01T00:00:00.000000+00:00",
        "name": "Energy Sector Strategy 1387-1391 (2007/8-2012/3)",
        "postfix": "A",
        "description": "the document description",
        "source_url": "https://policy.gov.uk/name.pdf",
        "type": "just my type",
        "geography": "not my favourite subject",
        "source": "may it be with you",
        "import_id": "CCLW.001.000.XXX",
        "category": "a category",
        "languages": ["afr"],
        "events": [
            {
                "name": "Publication",
                "description": "The publication date",
                "created_ts": "2008-12-25T00:00:00+00:00",
            },
        ],
        "sectors": ["Energy"],
        "instruments": ["some instrument", "another instrument"],
        "frameworks": ["some framework"],
        "topics": ["Mitigation"],
        "hazards": ["some hazard"],
        "keywords": ["some keyword"],
    }
    create_request = DocumentCreateRequest(**create_request_content)
    create_document(test_db, create_request)
    test_db.commit()

    doc: Document = test_db.query(Document).first()
    assert doc.name == create_request_content["name"]
    assert doc.postfix == create_request_content["postfix"]
    assert doc.description == create_request_content["description"]
    assert doc.url is None
    assert doc.md5_sum is None
    assert doc.import_id == create_request_content["import_id"]
    assert doc.publication_ts == datetime(2000, 1, 1)
    assert doc.slug == (
        "not-my-favourite-subject_2000_energy-sector-strategy-"
        "1387-1391-2007-8-2012-3_000_xxx"
    )

    event = test_db.query(Event).first()
    assert event.name == "Publication"
    assert event.created_ts == datetime(2008, 12, 25, 0, 0, tzinfo=timezone.utc)
    assert test_db.query(DocumentLanguage).first().document_id == 1


def test_create_documents_fail(client, superuser_token_headers, test_db):
    """Document creation should fail unless all referenced metadata already exists."""

    # ensure meta
    test_db.add(Source(name="may it be with you"))
    test_db.add(
        Geography(
            display_value="not my favourite subject",
            slug="not-my-favourite-subject",
            value="NMFS",
            type="country",
        )
    )
    test_db.add(DocumentType(name="just my type", description="sigh"))
    test_db.add(Language(language_code="afr", name="Afrikaans"))
    test_db.add(Category(name="a category", description="a category description"))
    test_db.add(Hazard(name="some other hazard", description="Imported by CPR loader"))
    test_db.add(Response(name="Mitigation", description="Imported by CPR loader"))
    test_db.add(
        Framework(name="some other framework", description="Imported by CPR loader")
    )
    test_db.add(Keyword(name="some keyword", description="Imported by CPR loader"))
    test_db.commit()

    test_db.add(
        Sector(name="Energy", description="Imported by CPR loader", source_id=1)
    )
    test_db.add(
        Instrument(
            name="some instrument", description="Imported by CPR loader", source_id=1
        )
    )
    test_db.add(
        Instrument(
            name="another instrument", description="Imported by CPR loader", source_id=1
        )
    )
    test_db.commit()

    create_request_content = {
        "publication_ts": "2000-01-01T00:00:00.000000+00:00",
        "name": "Energy Sector Strategy 1387-1391 (2007/8-2012/3)",
        "description": "the document description",
        "source_url": "https://climate-laws.org/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBcG9IIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--be6991246abda10bef5edc0a4d196b73ce1b1a26/f",
        "type": "just my type",
        "geography": "not my favourite subject",
        "source": "may it be with you",
        "import_id": "CCLW.001.000.XXX",
        "category": "a category",
        "languages": ["afr"],
        "events": [
            {
                "name": "Publication",
                "description": "The publication date",
                "created_ts": "2008-12-25T00:00:00+00:00",
            }
        ],
        "sectors": ["Energy"],
        "instruments": ["some instrument", "another instrument"],
        "frameworks": ["some framework"],
        "topics": ["Mitigation"],
        "hazards": ["some hazard"],
        "keywords": ["some keyword"],
    }
    create_request = DocumentCreateRequest(**create_request_content)
    with pytest.raises(UnknownMetadataError):
        create_document(test_db, create_request)
        test_db.commit()

    assert len(list(test_db.query(Document).all())) == 0
    assert test_db.query(Event).first() is None
