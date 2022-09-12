from typing import Any, Dict, List
from unittest.mock import ANY, MagicMock

import pytest

from app.db.models import (
    Language,
    Source,
    Category,
)
from app.api.api_v1.routers.lookups.utils import tree_table_to_json
from app.db.session import SessionLocal


@pytest.mark.parametrize(
    "path,table",
    [
        ("languages", Language),
        ("sources", Source),
        ("categories", Category),
    ],
)
def test_get_lookups(client, user_token_headers, test_db, path, table):
    response = client.get(
        f"/api/v1/{path}",
        headers=user_token_headers,
    )

    db_data = test_db.query(table).all()

    assert response.status_code == 200
    if path != "languages":
        # TODO: assert that the db contains data to confirm that the test is meaningful
        # We filter languages to only those with a value for `part1_code`
        assert len(response.json()) == len(db_data)
        # TODO: test languages


class _MockColumn:
    def __init__(self, name):
        self.name = name


class _MockTable:
    def __init__(self, columns: List[str]):
        self.columns = [_MockColumn(c) for c in columns]


class _MockRow:
    def __init__(self, data: Dict[str, Any]):
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
    db.query = lambda _: _MockQuery(data)
    processed_data = tree_table_to_json(ANY, db)

    from pprint import pprint

    pprint(processed_data)
    pprint(expected)

    assert processed_data == expected
