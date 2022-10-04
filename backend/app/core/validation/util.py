import logging
from typing import Any, Collection, Mapping, Optional, Sequence

from sqlalchemy.orm import Session

from app.api.api_v1.routers.lookups.util import get_metadata

_LOGGER = logging.getLogger(__file__)


def _flatten_maybe_tree(
    maybe_tree: Sequence[Mapping[str, Any]],
    values: Optional[set[str]] = None,
) -> Collection[str]:
    def is_tree_node(maybe_node: Mapping[str, Any]) -> bool:
        return set(maybe_node.keys()) == {"node", "children"}

    def get_value(data_node: Mapping[str, str]) -> str:
        value = data_node.get("name") or data_node.get("value")
        if value is None:
            raise Exception(f"No value found in '{data_node}'")
        return value

    values = values or set()

    for maybe_node in maybe_tree:
        if is_tree_node(maybe_node):
            values.add(get_value(maybe_node["node"]))
            _flatten_maybe_tree(maybe_node["children"], values=values)
        else:
            values.add(get_value(maybe_node))

    return values


def get_valid_metadata(
    db: Session,
) -> Mapping[str, Mapping[str, Collection[str]]]:
    """
    Make a request to the backend to collect valid metadata values

    :param requests.Session session: The session used for making the request.
    :return Mapping[str, Sequence[str]]: _description_
    """
    _LOGGER.info("Retrieving valid metadata values from database")

    raw_metadata = get_metadata(db)["metadata"]

    return {
        source: {
            meta: _flatten_maybe_tree(raw_metadata[source][meta])
            for meta in raw_metadata[source]
        }
        for source in raw_metadata
    }
