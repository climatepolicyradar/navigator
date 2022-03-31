def test_post_document(
    client, user_token_headers, test_s3_client, s3_document_bucket_names
):

    test_valid_filename = "./app/api/api_v1/routers/tests/data/cclw-1618-884b7d6efcf448ff92d27f37ff22cb65.pdf"

    with open(test_valid_filename, "rb") as f:
        response = client.post(
            "/api/v1/document",
            files={"file": (test_valid_filename, f, "application/pdf")},
            headers=user_token_headers,
        )

    queue_bucket_contents = test_s3_client.client.list_objects(
        Bucket=s3_document_bucket_names["queue"],
    ).get("Contents")

    assert response.status_code == 200
    # There should be 2 documents in the mocked bucket: test_document.pdf, and the document just uploaded.
    assert len(queue_bucket_contents) == 2

    test_invalid_filename = "./app/api/api_v1/routers/tests/data/empty_img.png"
    with open(test_invalid_filename, "rb") as f:
        response = client.post(
            "/api/v1/document",
            files={"file": (test_invalid_filename, f, "application/pdf")},
            headers=user_token_headers,
        )

    queue_bucket_contents = test_s3_client.client.list_objects(
        Bucket=s3_document_bucket_names["queue"],
    ).get("Contents")
    assert response.status_code == 415
    # No more documents should have been uploaded to the queue bucket.
    assert len(queue_bucket_contents) == 2
