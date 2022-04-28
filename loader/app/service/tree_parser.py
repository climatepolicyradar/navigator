"""Tree result parser for backend API lookup results.

See backend's app.api.api_v1.routers.lookups.tree_table_to_json

A tree had 0/1/many nodes.
A node typically looks like this:

    {
        "node": {
            "id": 63,
            "display_value": "North America",
            "value": "North America",
            "type": "World Bank Region",
            "parent_id": None,
        },
        "children": [
            {
                "node": {
                    "id": 64,
                    "display_value": "Canada",
                    "value": "CAN",
                    "type": "ISO-3166",
                    "parent_id": 63,
                },
                "children": [],
            },
            {
                "node": {
                    "id": 388,
                    "display_value": "United States of America",
                    "value": "USA",
                    "type": "ISO-3166",
                    "parent_id": 63,
                },
                "children": [],
            },
        ],
    },
"""
from typing import List, Generator


def get_from_tree_by_type(
    tree: List[dict], node_type: str
) -> Generator[dict, None, None]:
    """Yields all nodes with specific type from a tree recursively.

    Wrap with get_unique_from_tree_by_type for unique nodes.

    The lookup trees coming from backend API will usually be quite simple in that each
    depth will have the same 'type', but the recursive approach works for any tree.
    """

    for node in tree:
        if node["node"]["type"] == node_type:
            yield node["node"]
        yield from get_from_tree_by_type(node["children"], node_type)


def get_unique_from_tree_by_type(
    tree: List[dict], node_type: str
) -> Generator[dict, None, None]:
    """Yields unique nodes from a 'get_from_tree_by_type' result."""

    seen = {}
    for node in get_from_tree_by_type(tree, node_type):
        key = frozenset(node.items())
        if key in seen:
            continue
        else:
            seen[key] = node
            yield node
