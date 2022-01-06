def test_post_document(client, user_token_headers):
    test_valid_filename = "./app/api/api_v1/routers/tests/data/cclw-1053-abcf8dbe8b944a58923880fc75111088.pdf"

    with open(test_valid_filename, "rb") as f:
        response = client.post(
            "/api/v1/document",
            files={"file": (test_valid_filename, f, "application/pdf")},
            headers=user_token_headers,
        )

    assert response.status_code == 200

    test_invalid_filename = "./app/api/api_v1/routers/tests/data/empty_img.png"
    with open(test_invalid_filename, "rb") as f:
        response = client.post(
            "/api/v1/document",
            files={"file": (test_invalid_filename, f, "application/pdf")},
            headers=user_token_headers,
        )

    assert response.status_code == 415
