from dataclasses import dataclass
from unittest.mock import patch, MagicMock

from app.db.models import APIDocument
from app.poster.main import post_all_to_backend_api
from app.service.context import Context


@patch("app.poster.main.post_doc")
@patch("app.poster.main.get_all_valid_documents")
def test_post_all_to_backend_api(mock_get_all_valid_documents, mock_post_doc):
    @dataclass
    class SomethingWithAnID:
        id: int

    doc = SomethingWithAnID(id=3)
    mock_get_all_valid_documents.return_value = [doc]
    mock_post_doc.return_value = {"id": 7}

    @dataclass
    class MockDb:
        """Mock SessionLocal for testing."""

        add = MagicMock()
        commit = MagicMock()
        flush = MagicMock()
        refresh = MagicMock()

    mock_db = MockDb()
    ctx = Context(db=mock_db, client=None)

    post_all_to_backend_api(ctx)

    mock_get_all_valid_documents.assert_called_once_with(mock_db)
    mock_post_doc.assert_called_once_with(mock_db, doc)

    assert isinstance(mock_db.add.call_args.args[0], APIDocument)
    assert mock_db.add.call_args[0][0].document_id == 3
    assert mock_db.add.call_args[0][0].remote_document_id == 7
