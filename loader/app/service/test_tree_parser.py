from app.service.tree_parser import get_unique_from_tree_by_type

sample_tree = [
    {
        "node": {
            "id": 1,
            "type": "alpha",
            "parent_id": None,
        },
        "children": [
            {
                "node": {
                    "id": 2,
                    "type": "beta",
                    "parent_id": 1,
                },
                "children": [],
            },
            {
                "node": {
                    "id": 3,
                    "type": "beta",
                    "parent_id": 1,
                },
                "children": [
                    {
                        "node": {
                            "id": 1,
                            "type": "alpha",
                            "parent_id": None,
                        },
                        "children": [
                            {
                                "node": {
                                    "id": 2,
                                    "type": "beta",
                                    "parent_id": 1,
                                },
                                "children": [],
                            },
                            {
                                "node": {
                                    "id": 4,
                                    "type": "beta",
                                    "parent_id": 1,
                                },
                                "children": [],
                            },
                        ],
                    },
                ],
            },
        ],
    },
]


def test_tree_parser():
    all_nodes = get_unique_from_tree_by_type(sample_tree, "beta")

    assert list(all_nodes) == [
        {
            "id": 2,
            "type": "beta",
            "parent_id": 1,
        },
        {
            "id": 3,
            "type": "beta",
            "parent_id": 1,
        },
        {
            "id": 4,
            "type": "beta",
            "parent_id": 1,
        },
    ]
