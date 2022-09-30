from typing import Any, Dict, List

from sqlalchemy.orm import Session

from app.db.session import Base


def table_to_json(
    table: Base,
    db: Session,
) -> List[Dict]:
    json_out = []

    for row in db.query(table).all():
        row_object = {col.name: getattr(row, col.name) for col in row.__table__.columns}
        json_out.append(row_object)

    return json_out


def tree_table_to_json(
    table: Base,
    db: Session,
) -> List[Dict]:
    json_out = []
    child_list_map: Dict[int, Any] = {}

    for row in db.query(table).all():
        row_object = {col.name: getattr(row, col.name) for col in row.__table__.columns}
        row_children: List[Dict[str, Any]] = []
        child_list_map[row_object["id"]] = row_children

        # No parent indicates a top level element
        node_row_object = {"node": row_object, "children": row_children}
        node_id = row_object["parent_id"]
        if node_id is None:
            json_out.append(node_row_object)
        else:
            append_list = child_list_map.get(node_id)
            if append_list is None:
                raise RuntimeError(f"Could not locate parent node with id {node_id}")
            append_list.append(node_row_object)

    return json_out
