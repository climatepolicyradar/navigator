from dataclasses import dataclass
from datetime import datetime
from unittest.mock import patch, MagicMock

from app.loader.load.main import load
from app.model import Key, PolicyData, Doc, PolicyLookup


@patch("app.loader.load.main.get_document_validity_sync")
@patch("app.loader.load.main.get_geography_id")
@patch("app.loader.load.main.get_type_id")
def test_load_single_doc(
    mock_get_type_id,
    mock_get_geography_id,
    mock_get_document_validity_sync,
):
    @dataclass
    class MockDb:
        """Mock SessionLocal for testing."""

        add = MagicMock()
        commit = MagicMock()
        flush = MagicMock()
        refresh = MagicMock()

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

    called_doc = mock_db.add.call_args_list[0][0][0]

    assert called_doc.name == "foo"
    assert called_doc.source_url == "http://doc"
    assert called_doc.source_id == 1
    # assert called_doc.url ==  # TODO: upload to S3
    assert called_doc.is_valid
    assert called_doc.invalid_reason is None
    assert called_doc.geography_id == 456
    assert called_doc.type_id == 123

    called_event = mock_db.add.call_args_list[1][0][0]

    assert called_event.document_id == called_doc.id
    assert called_event.name == "Publication"
    assert called_event.description == "The publication date"
    assert called_event.created_ts == datetime(1979, 11, 17)

    mock_db.commit.assert_called_once()


@patch("app.loader.load.main.get_document_validity_sync")
@patch("app.loader.load.main.get_geography_id")
@patch("app.loader.load.main.get_type_id")
def test_load_two_related_docs(
    mock_get_type_id,
    mock_get_geography_id,
    mock_get_document_validity_sync,
):
    @dataclass
    class MockDb:
        """Mock SessionLocal for testing."""

        add = MagicMock()
        commit = MagicMock()
        flush = MagicMock()
        refresh = MagicMock()

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
    doc2: Doc = Doc(
        doc_url="http://doc2",
        doc_name="doc name 2",
        doc_language="en",
    )
    policy_data: PolicyData = PolicyData(
        **policy_key.__dict__,
        policy_description="foobar",
        docs=[doc, doc2],
    )
    policies: PolicyLookup = {
        policy_key: policy_data,
    }

    load(mock_db, policies)

    mock_get_type_id.assert_called_once_with(mock_db, policy_data.policy_type)
    mock_get_geography_id.assert_called_once_with(mock_db, policy_data.country_code)
    assert mock_get_document_validity_sync.call_args_list[0][0][0] == "http://doc"
    assert mock_get_document_validity_sync.call_args_list[1][0][0] == "http://doc2"

    called_doc = mock_db.add.call_args_list[0][0][0]

    assert called_doc.name == "foo"
    assert called_doc.source_url == "http://doc"
    assert called_doc.source_id == 1
    # assert called_doc.url ==  # TODO: upload to S3
    assert called_doc.is_valid
    assert called_doc.invalid_reason is None
    assert called_doc.geography_id == 456
    assert called_doc.type_id == 123

    called_event = mock_db.add.call_args_list[1][0][0]

    assert called_event.document_id == called_doc.id
    assert called_event.name == "Publication"
    assert called_event.description == "The publication date"
    assert called_event.created_ts == datetime(1979, 11, 17)

    # second doc
    called_doc2 = mock_db.add.call_args_list[2][0][0]

    assert called_doc2.name == "foo"
    assert called_doc2.source_url == "http://doc2"
    assert called_doc2.source_id == 1
    # assert called_doc.url ==  # TODO: upload to S3
    assert called_doc2.is_valid
    assert called_doc2.invalid_reason is None
    assert called_doc2.geography_id == 456
    assert called_doc2.type_id == 123

    called_event2 = mock_db.add.call_args_list[3][0][0]

    assert called_event2.document_id == called_doc2.id
    assert called_event2.name == "Publication"
    assert called_event2.description == "The publication date"
    assert called_event2.created_ts == datetime(1979, 11, 17)

    called_association = mock_db.add.call_args_list[4][0][0]

    assert called_association.document_id_from == called_doc2.id
    assert called_association.document_id_to == called_doc.id
    assert called_association.type == "related"
    assert called_association.name == "related"

    assert mock_db.commit.call_count == 2
