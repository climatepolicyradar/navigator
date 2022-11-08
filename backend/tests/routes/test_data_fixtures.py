from dateutil.parser import parse
import pytest
from app.db.models import Category, Document, DocumentType, Geography, Source, Event
from tests.utils import json_serialize

template_doc = {
    "name": "doc",
    "description": "doc test",
    "source_url": "url1",
    "url": "url",
    "md5_sum": "sum",
    "source_id": 0,
    "category_id": 0,
    "geography_id": 0,
    "type_id": 0,
    "publication_ts": "2022-08-17",
}


def make_doc(
    name: str,
    import_id: str,
    slug: str,
    source_id: int,
    category_id: int,
    geography_id: int,
    type_id: int,
    year: int = 2022,
):
    doc = template_doc | {
        "name": name,
        "source_id": source_id,
        "category_id": category_id,
        "geography_id": geography_id,
        "type_id": type_id,
        "slug": slug,
        "import_id": import_id,
        "publication_ts": f"{year}-08-17",
    }

    return Document(**doc)


@pytest.fixture
def doc_browse_data(test_db):
    geos = [
        Geography(
            display_value="A place on the planet",
            slug="a-place-on-the-planet",
            value="XXX",
        ),
        Geography(
            display_value="A place in the sea", slug="a-place-in-the-sea", value="YYY"
        ),
        Geography(
            display_value="A place in the sky", slug="a-place-on-the-sky", value="ZZZ"
        ),
    ]
    doc_types = [DocumentType(name="doctype", description="for testing")]
    sources = [Source(name="May the source be with you")]
    cats = [Category(name="Felix", description="Persian Cat")]

    test_db.add_all(geos)
    test_db.add_all(doc_types)
    test_db.add_all(sources)
    test_db.add_all(cats)
    test_db.flush()

    # Now setup the Document set
    docs = [
        make_doc("doc1", "CCLW.executive.1111.1111", "doc1_1111_1111", sources[0].id, cats[0].id, geos[0].id, doc_types[0].id, 1990),  # type: ignore
        make_doc("doc2", "CCLW.executive.2222.2222", "doc2_2222_2222", sources[0].id, cats[0].id, geos[1].id, doc_types[0].id, 2007),  # type: ignore
        make_doc("doc3", "CCLW.executive.3333.3333", "doc3_3333_3333", sources[0].id, cats[0].id, geos[2].id, doc_types[0].id),  # type: ignore
    ]

    test_db.add_all(docs)
    test_db.commit()

    yield {
        "db": test_db,
        "docs": [json_serialize(doc) for doc in docs],
        "geos": geos,
        "doc_types": doc_types,
        "sources": sources,
        "cats": cats,
    }


@pytest.fixture
def summary_country_data(test_db):
    geos = [
        Geography(
            display_value="A place on the land", slug="a-place-on-the-land", value="XXX"
        ),
        Geography(
            display_value="A place in the sea", slug="a-place-in-the-sea", value="YYY"
        ),
    ]
    doc_types = [DocumentType(name="doctype", description="for testing")]
    sources = [Source(name="May the source be with you")]
    cats = [
        Category(name="Law", description="Persian Cat"),
        Category(name="Policy", description="Mog"),
        Category(name="Case", description="Ginger Cat"),
    ]

    test_db.add_all(geos)
    test_db.add_all(doc_types)
    test_db.add_all(sources)
    test_db.add_all(cats)
    test_db.flush()

    # Now setup the Document set

    docs = [
        # Sheba's documents
        make_doc("doc1", "CCLW.executive.1111.1111", "doc1_1111_1111", sources[0].id, cats[0].id, geos[0].id, doc_types[0].id, 1990),  # type: ignore
        make_doc("doc2", "CCLW.executive.2222.2222", "doc2_2222_2222", sources[0].id, cats[0].id, geos[0].id, doc_types[0].id, 2007),  # type: ignore
        make_doc("doc3", "CCLW.executive.3333.3333", "doc3_3333_3333", sources[0].id, cats[0].id, geos[0].id, doc_types[0].id),  # type: ignore
        # Cuddles' documents
        make_doc("doc4", "CCLW.executive.4444.4444", "doc2_4444_4444", sources[0].id, cats[1].id, geos[0].id, doc_types[0].id, 1991),  # type: ignore
        make_doc("doc5", "CCLW.executive.5555.5555", "doc3_5555_5555", sources[0].id, cats[1].id, geos[0].id, doc_types[0].id, 2005),  # type: ignore
    ]

    test_db.add_all(docs)
    test_db.flush()

    # Now some events
    events = [
        Event(
            document_id=docs[3].id,
            name="Red Dwarf Ep1",
            description="-",
            created_ts=parse("15 February 1988"),
        ),
        Event(
            document_id=docs[3].id,
            name="Red Dwarf Ep2",
            description="",
            created_ts=parse("22 February 1988"),
        ),
        Event(
            document_id=docs[3].id,
            name="Red Dwarf Ep3",
            description="",
            created_ts=parse("29 February 1988"),
        ),
        Event(
            document_id=docs[3].id,
            name="Red Dwarf Ep4",
            description="",
            created_ts=parse("7 March 1988"),
        ),
    ]

    test_db.add_all(events)

    test_db.commit()
    yield {
        "db": test_db,
        "docs": docs,
        "geos": geos,
        "doc_types": doc_types,
        "sources": sources,
        "cats": cats,
        "events": events,
    }
