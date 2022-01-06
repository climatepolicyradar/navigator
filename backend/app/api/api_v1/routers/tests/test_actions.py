def test_post_action(client, user_token_headers):

    response = client.post(
        "/api/v1/action",
        json={
            "source_id": 1,
            "name": "test action",
            "year": 2008,
            "month": 9,
            "day": 12,
            "geography_id": 1,
            "type_id": 1,
            "documents": [
                {
                    "name": "test document 1",
                    "language_id": 1,
                    "source_url": None,
                    "s3_url": "https://cpr-document-queue.s3.eu-west-2.amazonaws.com/user-2-time-20220106143012-cclw-1053-abcf8dbe8b944a58923880fc75111088.pdf",
                    "year": 2009,
                    "month": 12,
                    "day": 10,
                }
            ],
        },
        headers=user_token_headers,
    )

    assert response.status_code == 200
