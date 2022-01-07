from app.db import models


def test_get_lookups(client, user_token_headers, test_db):

    lookup_api_paths = [
        ("geographies", models.Geography),
        ("languages", models.Language),
        ("action_types", models.ActionType),
        ("sources", models.Source),
    ]

    for path, table in lookup_api_paths:
        response = client.get(
            f"/api/v1/{path}",
            headers=user_token_headers,
        )

        db_data = test_db.query(table).all()

        assert response.status_code == 200
        assert len(response.json()) == len(db_data)
