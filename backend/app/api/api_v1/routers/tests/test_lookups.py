import pytest

from app.db.models import (
    Geography,
    Language,
    Source,
    Instrument,
    Sector,
    DocumentType,
    Category,
)


@pytest.mark.parametrize(
    "path,table",
    [
        ("geographies", Geography),
        ("languages", Language),
        ("sources", Source),
        ("instruments", Instrument),
        ("sectors", Sector),
        ("types", DocumentType),
        ("categories", Category),
    ],
)
def test_get_lookups(client, user_token_headers, test_db, path, table):
    response = client.get(
        f"/api/v1/{path}",
        headers=user_token_headers,
    )

    db_data = test_db.query(table).all()

    assert response.status_code == 200
    if path != "languages":
        # TODO: assert that the db contains data to confirm that the test is meaningful
        # We filter languages to only those with a value for `part1_code`
        assert len(response.json()) == len(db_data)
        # TODO: test languages


@pytest.mark.parametrize(
    "path",
    [
        "geographies",
        "languages",
        "sources",
        "instruments",
        "sectors",
        "types",
        "categories",
    ],
)
def test_get_lookups_unauth(client, path, table):
    response = client.get(f"/api/v1/{path}")
    assert response.status_code == 403
