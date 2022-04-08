from dataclasses import dataclass
from datetime import datetime
from unittest.mock import patch, MagicMock

from app.loader.load.main import load
from app.model import Key, PolicyData, Doc, PolicyLookup


@dataclass
class MockDb:
    """Mock SessionLocal for testing."""

    add = MagicMock()
    commit = MagicMock()


@patch("app.loader.load.main.get_document_validity_sync")
@patch("app.loader.load.main.get_geography_id")
@patch("app.loader.load.main.get_type_id")
def test_load(
    mock_get_type_id,
    mock_get_geography_id,
    mock_get_document_validity_sync,
):
    mock_get_type_id.return_value = 123
    mock_get_geography_id.return_value = 456
    mock_get_document_validity_sync.return_value = None

    mock_db = MockDb()

    policy_key = Key(
        policy_name="foo",
        policy_type="Law",
        country_code="cc",
        policy_date=datetime(1979, 11, 17),
    )
    doc: Doc = Doc(
        doc_url="http://doc",
        doc_name="doc name",
        doc_language="en",
    )
    policy_data: PolicyData = PolicyData(
        **policy_key.__dict__,
        policy_description="foobar",
        docs=[doc],
    )
    policies: PolicyLookup = {
        policy_key: policy_data,
    }

    load(mock_db, policies)

    mock_get_type_id.assert_called_once_with(mock_db, policy_data.policy_type)
    mock_get_geography_id.assert_called_once_with(mock_db, policy_data.country_code)
    mock_get_document_validity_sync.assert_called_once_with("http://doc")

    called_doc = mock_db.add.call_args[0][0]
    mock_db.add.assert_called_once()
    assert called_doc.name == "foo"
    assert called_doc.source_url == "http://doc"
    assert called_doc.source_id == 1
    # assert called_doc.url ==  # TODO: upload to S3
    assert called_doc.is_valid
    assert called_doc.invalid_reason is None
    assert called_doc.geography_id == 456
    assert called_doc.type_id == 123

    mock_db.commit.assert_called_once()
