import pytest
from app.db.models import Category, Document, DocumentType, Geography, Source

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
        "publication_ts": f"{year}-08-17",
    }

    return Document(**doc)


@pytest.fixture
def doc_browse_data(test_db):
    geos = [
        Geography(display_value="A place on the planet", value="XXX"),
        Geography(display_value="A place in the sea", value="YYY"),
        Geography(display_value="A place in the sky", value="ZZZ"),
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
        make_doc("doc1", sources[0].id, cats[0].id, geos[0].id, doc_types[0].id, 1990),
        make_doc("doc2", sources[0].id, cats[0].id, geos[1].id, doc_types[0].id, 2007),
        make_doc("doc3", sources[0].id, cats[0].id, geos[2].id, doc_types[0].id),
    ]

    test_db.add_all(docs)
    test_db.commit()

    yield {
        "db": test_db,
        "docs": docs,
        "geos": geos,
        "doc_types": doc_types,
        "sources": sources,
        "cats": cats,
    }
