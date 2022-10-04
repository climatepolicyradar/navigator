from typing import Collection, Sequence

from app.core.validation.util import _flatten_maybe_tree, get_valid_metadata
from app.db.models import Keyword, Sector, Source

import pytest


NOT_A_TREE_1 = [{"name": 1}, {"name": 2}, {"name": 3}]
NOT_A_TREE_2 = [
    {"name": 1, "value": 2},
    {"name": 2, "value": 3},
    {"name": 3, "value": 4},
]
NOT_A_TREE_3 = [{"value": 2}, {"value": 3}, {"name": 4}]
NOT_A_TREE_4 = []


@pytest.mark.parametrize(
    "not_a_tree",
    [NOT_A_TREE_1, NOT_A_TREE_2, NOT_A_TREE_3, NOT_A_TREE_4],
)
def test__flatten_maybe_tree_not_a_tree(not_a_tree: Sequence):
    """Just test that we get values from JSON that does not describe a tree"""
    assert {min(d.values()) for d in not_a_tree} == _flatten_maybe_tree(not_a_tree)


IS_A_TREE_1 = [{"node": {"name": "dave"}, "children": []}]
IS_A_TREE_2 = [
    {
        "node": {"name": "dave"},
        "children": [{"node": {"name": "steve"}, "children": []}],
    }
]
IS_A_TREE_3 = [
    {
        "node": {"name": "dave"},
        "children": [
            {"node": {"name": "steve"}, "children": []},
            {
                "node": {"name": "othello"},
                "children": [
                    {"node": {"name": "ally", "value": "ignored"}, "children": []},
                ],
            },
        ],
    },
    {"node": {"value": "stewart"}, "children": []},
]
IS_A_TREE_4 = []
IS_A_TREE_1_EXPECTED = {"dave"}
IS_A_TREE_2_EXPECTED = {"dave", "steve"}
IS_A_TREE_3_EXPECTED = {"dave", "steve", "othello", "ally", "stewart"}
IS_A_TREE_4_EXPECTED = set()


@pytest.mark.parametrize(
    "is_a_tree,expected",
    [
        (IS_A_TREE_1, IS_A_TREE_1_EXPECTED),
        (IS_A_TREE_2, IS_A_TREE_2_EXPECTED),
        (IS_A_TREE_3, IS_A_TREE_3_EXPECTED),
        (IS_A_TREE_4, IS_A_TREE_4_EXPECTED),
    ],
)
def test__flatten_maybe_tree_is_a_tree(is_a_tree: Sequence, expected: Collection):
    """Test that we get values from JSON that does describe a tree"""
    assert _flatten_maybe_tree(is_a_tree) == expected


def test_valid_metadata(test_db):
    """Test the structure returned and a couple of added values"""

    # Add some test data
    test_db.add(Source(name="Primary"))
    test_db.commit()
    test_db.add(Keyword(name="some keyword", description="a keyword"))
    test_db.add(Sector(name="Energy", description="energy sector", source_id=1))
    test_db.add(
        Sector(name="Agriculture", description="agriculture sector", source_id=1)
    )
    test_db.commit()

    metadata = get_valid_metadata(test_db)
    assert "CCLW" in metadata
    cclw_metadata = metadata["CCLW"]
    assert "categories" in cclw_metadata
    assert "document_types" in cclw_metadata
    assert "frameworks" in cclw_metadata
    assert "geographies" in cclw_metadata
    assert "hazards" in cclw_metadata
    assert "instruments" in cclw_metadata
    assert "keywords" in cclw_metadata
    assert "languages" in cclw_metadata
    assert "sectors" in cclw_metadata
    assert "sources" in cclw_metadata
    assert "topics" in cclw_metadata

    assert cclw_metadata["sources"] == {"Primary"}
    assert cclw_metadata["keywords"] == {"some keyword"}
    assert cclw_metadata["sectors"] == {"Energy", "Agriculture"}
