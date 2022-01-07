def test_post_action(
    client, user_token_headers, test_s3_client, s3_document_bucket_names
):

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
                    "s3_url": f"https://{s3_document_bucket_names['queue']}.s3.eu-west-2.amazonaws.com/test_document.pdf",
                    "year": 2009,
                    "month": 12,
                    "day": 10,
                }
            ],
        },
        headers=user_token_headers,
    )

    queue_bucket_contents = test_s3_client.client.list_objects(
        Bucket=s3_document_bucket_names["queue"],
    ).get("Contents")

    store_bucket_contents = test_s3_client.client.list_objects(
        Bucket=s3_document_bucket_names["store"],
    ).get("Contents")

    assert response.status_code == 200
    # Queue bucket is empty as test_document.pdf has been moved.
    assert queue_bucket_contents is None
    # Store bucket contains only test_document.pdf.
    assert len(store_bucket_contents) == 1
    assert store_bucket_contents[0].get("Key") == "test_document.pdf"
