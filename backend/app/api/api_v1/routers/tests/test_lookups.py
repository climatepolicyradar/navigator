def test_get_lookups(client, user_token_headers):

    lookup_api_paths = [
        "geographies",
        "languages",
        "action_types",
        "sources",
    ]

    for path in lookup_api_paths:
        response = client.get(
            f"/api/v1/{path}",
            headers=user_token_headers,
        )

        assert response.status_code == 200
        # assert len(response.json()) > 0
