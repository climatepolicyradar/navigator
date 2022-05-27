from unittest.mock import patch
import pytest
from app.db.models import APIDocument, Association
from app.db.schema import AssociationSchema
from app.poster.associations import get_associations
from app.service.context import Context


class MockDb:  # noqa: D101
    pass


@pytest.mark.parametrize(
    "scenario_description, associations_in_db, api_documents_in_db, expected",
    [
        [
            "an association",
            [
                Association(
                    document_id_from=1,
                    document_id_to=2,
                    name="the assoc name",
                    type="the assoc type",
                )
            ],
            [
                APIDocument(
                    document_id=1,
                    remote_document_id=11,
                ),
                APIDocument(
                    document_id=2,
                    remote_document_id=22,
                ),
            ],
            [
                AssociationSchema(
                    document_id_from=11,
                    document_id_to=22,
                    name="the assoc name",
                    type="the assoc type",
                )
            ],
        ],
        [
            "missing remote doc",
            [
                Association(
                    document_id_from=1,
                    document_id_to=2,
                    name="the assoc name",
                    type="the assoc type",
                )
            ],
            [
                APIDocument(
                    document_id=1,
                    remote_document_id=11,
                ),
                # the missing remote doc (e.g. its doc has valid=false)
                # APIDocument(
                #     document_id=2,
                #     remote_document_id=22,
                # ),
            ],
            [
                # empty, no association
            ],
        ],
    ],
)
@patch("app.poster.associations.get_all_associations")
@patch("app.poster.associations.get_all_api_documents")
def test_get_associations(
    mock_get_all_api_documents,
    mock_get_all_associations,
    scenario_description,
    associations_in_db,
    api_documents_in_db,
    expected,
):
    mock_get_all_associations.return_value = associations_in_db
    mock_get_all_api_documents.return_value = api_documents_in_db

    mock_db = MockDb()
    ctx = Context(
        db=mock_db,
        client=None,
    )

    actual = get_associations(ctx)

    assert actual == expected, f"scenario failed: {scenario_description}"
    mock_get_all_api_documents.assert_called_once_with(mock_db)
    mock_get_all_associations.assert_called_once_with(mock_db)
