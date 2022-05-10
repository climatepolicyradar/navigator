from dataclasses import dataclass

from app.service.document_upload import _upload_document
from unittest.mock import patch, MagicMock


@patch("app.service.document_upload.upload_document")
def test_document_upload(mock_upload_document):
    mock_upload_document.return_value = "http://bucket-url", "md5 sum"

    country_code = "country-code"
    publication_date = "2022-04-26"

    @dataclass
    class MockDb:
        """Mock SessionLocal for testing."""

        add = MagicMock()
        commit = MagicMock()

    db = MockDb()

    @dataclass
    class MockDocument:
        id = 1
        name = "foo"
        source_url = "http://source-url"
        url = None

    document_db = MockDocument()

    _upload_document(db, document_db, country_code, publication_date)

    # document_db.url = "http://bucket-url"

    db.add.assert_called_once_with(document_db)
    db.commit.assert_called_once()
    mock_upload_document.assert_called_once_with(
        "http://source-url", f"{country_code}-{publication_date}-foo-1"
    )
