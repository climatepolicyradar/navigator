from http.client import OK
from typing import Any
from unittest.mock import MagicMock

import pytest

from app.core.util import tree_table_to_json
from app.db.session import SessionLocal
from tests.routes.test_documents import create_4_documents


def test_endpoint_returns_correct_keys(client):
    """Tests whether we get the correct data when the /config endpoint is called."""
    url_under_test = "/api/v1/config"

    response = client.get(
        url_under_test,
    )

    response_json = response.json()

    assert response.status_code == OK
    assert set(response_json["metadata"].keys()) == {"CCLW"}
    assert set(response_json["metadata"]["CCLW"].keys()) == {
        "categories",
        "document_types",
        "frameworks",
        "geographies",
        "hazards",
        "instruments",
        "keywords",
        "languages",
        "sectors",
        "sources",
        "topics",
    }


class _MockColumn:
    def __init__(self, name):
        self.name = name


class _MockTable:
    def __init__(self, columns: list[str]):
        self.columns = [_MockColumn(c) for c in columns]


class _MockRow:
    def __init__(self, data: dict[str, Any]):
        self.__table__ = _MockTable(list(data.keys()))
        for key, value in data.items():
            setattr(self, key, value)


class _MockQuery:
    def __init__(self, query_response_data):
        self.query_response_data = query_response_data

    def all(self):
        return [_MockRow(rd) for rd in self.query_response_data]


_DATA_1 = {"id": 1, "parent_id": None, "name": "root", "data": 1}
_DATA_2 = {"id": 2, "parent_id": 1, "name": "two", "data": 2}
_DATA_3 = {"id": 3, "parent_id": 2, "name": "three", "data": 3}
TREE_TABLE_DATA_1 = [_DATA_1, _DATA_2, _DATA_3]
_EX_THREE = {"node": _DATA_3, "children": []}
_EX_TWO = {"node": _DATA_2, "children": [_EX_THREE]}
_EX_ONE = {"node": _DATA_1, "children": [_EX_TWO]}
EXPECTED_TREE_1 = [_EX_ONE]


@pytest.mark.parametrize("data,expected", [(TREE_TABLE_DATA_1, EXPECTED_TREE_1)])
def test_tree_table_to_json(data, expected):
    db = MagicMock(spec=SessionLocal)
    db_query_mock = MagicMock()
    db_query_mock.order_by = lambda _: _MockQuery(data)
    db.query = lambda _: db_query_mock

    table_mock = MagicMock()
    table_mock.id = 1
    processed_data = tree_table_to_json(table_mock, db)

    assert processed_data == expected


def test_document_ids(
    client,
    test_db,
):
    create_4_documents(test_db)

    # Test properties
    get_ids_response = client.get("/api/v1/config/ids")
    assert get_ids_response.status_code == 200
    assert get_ids_response.headers.get("ETag") == "81dc9bdb52d04dc20036dbd8313ed055"
    assert get_ids_response.json() == ["1", "2", "3", "4"]
