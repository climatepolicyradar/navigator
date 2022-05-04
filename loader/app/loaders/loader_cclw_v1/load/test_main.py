from dataclasses import dataclass
from datetime import datetime
from unittest.mock import patch, MagicMock

from app.loaders.loader_cclw_v1.load.main import load
from app.model import Key, PolicyData, Doc, PolicyLookup


@patch("app.loaders.loader_cclw_v1.load.main.get_category_id")
@patch("app.loaders.loader_cclw_v1.load.main.get_language_id")
@patch("app.loaders.loader_cclw_v1.load.main.get_document_by_unique_constraint")
@patch("app.loaders.loader_cclw_v1.load.main.get_document_validity_sync")
@patch("app.loaders.loader_cclw_v1.load.main.get_geography_id")
@patch("app.loaders.loader_cclw_v1.load.main.get_type_id")
def test_load_single_doc(
    mock_get_document_type_id,
    mock_get_geography_id,
    mock_get_document_validity_sync,
    mock_get_document_by_unique_constraint,
    mock_get_language_id,
    mock_get_category_id,
):
    @dataclass
    class MockDb:
        """Mock SessionLocal for testing."""

        add = MagicMock()
        commit = MagicMock()
        flush = MagicMock()
        refresh = MagicMock()

    mock_get_document_type_id.return_value = 123
    mock_get_geography_id.return_value = 456
    mock_get_document_validity_sync.return_value = None
    mock_get_document_by_unique_constraint.return_value = None
    mock_get_language_id.return_value = 789
    mock_get_category_id.return_value = 321

    mock_db = MockDb()

    policy_key = Key(
        policy_name="foo",
        policy_category="Law",
        country_code="cc",
        policy_date=datetime(1979, 11, 17),
    )
    doc: Doc = Doc(
        doc_url="http://doc",
        doc_name="doc name",
        doc_languages=["en"],
        document_type="doc type",
        hazards=[],
        events=[],
        responses=[],
        frameworks=[],
        sectors=[],
        instruments=[],
        keywords=[],
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

    mock_get_document_type_id.assert_called_once_with(doc.document_type)
    mock_get_category_id.assert_called_once_with(policy_data.policy_category)
    mock_get_geography_id.assert_called_once_with(policy_data.country_code)
    mock_get_language_id.assert_called_once_with(doc.doc_languages[0])
    mock_get_document_validity_sync.assert_called_once_with("http://doc")
    mock_get_document_by_unique_constraint.assert_called_once_with(
        mock_db, "foo", 456, 123, 1, "http://doc"
    )

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


@patch("app.loaders.loader_cclw_v1.load.main.get_category_id")
@patch("app.loaders.loader_cclw_v1.load.main.get_language_id")
@patch("app.loaders.loader_cclw_v1.load.main.get_document_by_unique_constraint")
@patch("app.loaders.loader_cclw_v1.load.main.get_document_validity_sync")
@patch("app.loaders.loader_cclw_v1.load.main.get_geography_id")
@patch("app.loaders.loader_cclw_v1.load.main.get_type_id")
def test_load_two_related_docs(
    mock_get_document_type_id,
    mock_get_geography_id,
    mock_get_document_validity_sync,
    mock_get_document_by_unique_constraint,
    mock_get_language_id,
    mock_get_category_id,
):
    @dataclass
    class MockDb:
        """Mock SessionLocal for testing."""

        add = MagicMock()
        commit = MagicMock()
        flush = MagicMock()
        refresh = MagicMock()

    mock_get_document_type_id.side_effect = [123, 234]
    mock_get_geography_id.return_value = 456
    mock_get_document_validity_sync.return_value = None
    mock_get_document_by_unique_constraint.return_value = None
    mock_get_language_id.side_effect = [789, 890]
    mock_get_category_id.return_value = 321

    mock_db = MockDb()

    policy_key = Key(
        policy_name="foo",
        policy_category="Law",
        country_code="cc",
        policy_date=datetime(1979, 11, 17),
    )
    doc: Doc = Doc(
        doc_url="http://doc",
        doc_name="doc name",
        doc_languages=["en"],
        document_type="doc1 type",
        hazards=[],
        events=[],
        responses=[],
        frameworks=[],
        sectors=[],
        instruments=[],
        keywords=[],
    )
    doc2: Doc = Doc(
        doc_url="http://doc2",
        doc_name="doc name 2",
        doc_languages=["af"],
        document_type="doc2 type",
        hazards=[],
        events=[],
        responses=[],
        frameworks=[],
        sectors=[],
        instruments=[],
        keywords=[],
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

    mock_get_category_id.assert_called_once_with(policy_data.policy_category)
    assert mock_get_document_type_id.call_args_list[0][0][0] == doc.document_type
    assert mock_get_document_type_id.call_args_list[1][0][0] == doc2.document_type
    mock_get_geography_id.assert_called_once_with(policy_data.country_code)
    assert mock_get_language_id.call_args_list[0][0][0] == doc.doc_languages[0]
    assert mock_get_language_id.call_args_list[1][0][0] == doc2.doc_languages[0]
    assert mock_get_document_validity_sync.call_args_list[0][0][0] == "http://doc"
    assert mock_get_document_validity_sync.call_args_list[1][0][0] == "http://doc2"
    assert mock_get_document_by_unique_constraint.call_args_list[0][0] == (
        mock_db,
        "foo",
        456,
        123,
        1,
        "http://doc",
    )
    assert mock_get_document_by_unique_constraint.call_args_list[1][0] == (
        mock_db,
        "foo",
        456,
        234,
        1,
        "http://doc2",
    )

    # assert first doc was added
    called_doc = mock_db.add.call_args_list[0][0][0]

    assert called_doc.name == "foo"
    assert called_doc.source_url == "http://doc"
    assert called_doc.source_id == 1
    # assert called_doc.url ==  # TODO: upload to S3
    assert called_doc.is_valid
    assert called_doc.invalid_reason is None
    assert called_doc.geography_id == 456
    assert called_doc.type_id == 123

    # assert first doc's event was added
    called_event = mock_db.add.call_args_list[1][0][0]

    assert called_event.document_id == called_doc.id
    assert called_event.name == "Publication"
    assert called_event.description == "The publication date"
    assert called_event.created_ts == datetime(1979, 11, 17)

    # assert first doc's language was added
    called_doc_language = mock_db.add.call_args_list[2][0][0]
    assert called_doc_language.document_id == called_doc.id
    assert called_doc_language.language_id == 789

    # assert second doc was added
    called_doc2 = mock_db.add.call_args_list[3][0][0]

    assert called_doc2.name == "foo"
    assert called_doc2.source_url == "http://doc2"
    assert called_doc2.source_id == 1
    # assert called_doc.url ==  # TODO: upload to S3
    assert called_doc2.is_valid
    assert called_doc2.invalid_reason is None
    assert called_doc2.geography_id == 456
    assert called_doc2.type_id == 234

    # assert second doc's association was added
    called_association = mock_db.add.call_args_list[4][0][0]

    assert called_association.document_id_from == called_doc2.id
    assert called_association.document_id_to == called_doc.id
    assert called_association.type == "related"
    assert called_association.name == "related"

    # assert second doc's event was added
    called_event2 = mock_db.add.call_args_list[5][0][0]

    assert called_event2.document_id == called_doc2.id
    assert called_event2.name == "Publication"
    assert called_event2.description == "The publication date"
    assert called_event2.created_ts == datetime(1979, 11, 17)

    # assert second doc's language was added
    called_doc2_language = mock_db.add.call_args_list[6][0][0]
    assert called_doc2_language.document_id == called_doc2.id
    assert called_doc2_language.language_id == 890

    assert mock_db.commit.call_count == 2
