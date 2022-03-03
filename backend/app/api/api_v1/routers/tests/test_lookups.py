import app.db.models.lookups
from app.db import models


def test_get_lookups(client, user_token_headers, test_db):
    lookup_api_paths = [
        ("geographies", app.db.models.lookups.Geography),
        ("languages", app.db.models.lookups.Language),
        ("action_types", app.db.models.lookups.ActionType),
        ("sources", models.Source),
    ]

    for path, table in lookup_api_paths:
        response = client.get(
            f"/api/v1/{path}",
            headers=user_token_headers,
        )

        db_data = test_db.query(table).all()

        assert response.status_code == 200
        if path != "languages":
            # We filter languages to only those with a value for `part1_code`
            assert len(response.json()) == len(db_data)
