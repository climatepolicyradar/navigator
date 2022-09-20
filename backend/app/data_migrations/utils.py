from typing import Mapping, Optional, Sequence, cast

from sqlalchemy.orm import Session

from app.db.models import Source
from app.db.session import Base


def has_rows(db: Session, table: Base) -> bool:
    return db.query(table).count() > 0


def load_tree(
    db: Session,
    table: Base,
    data_tree_list: Sequence[Mapping[str, Mapping]],
) -> None:
    """
    Load a tree of data stored as JSON into a database table

    :param Session db: An open database session
    :param Base table: The table (and therefore type) of entries to create
    :param Sequence[Mapping[str, Mapping]] tree_list: A tree-list of data to load
    """
    _load_tree(db=db, table=table, data_tree_list=data_tree_list, parent_id=None)


def _load_tree(
    db: Session,
    table: Base,
    data_tree_list: Sequence[Mapping[str, Mapping]],
    parent_id: Optional[int] = None,
) -> None:
    for entry in data_tree_list:
        data = entry["node"]

        parent_db_entry = table(parent_id=parent_id, **data)
        db.add(parent_db_entry)

        child_nodes = cast(Sequence[Mapping[str, Mapping]], entry["children"])
        if child_nodes:
            db.flush()
            _load_tree(db, table, child_nodes, parent_db_entry.id)


def load_list(db: Session, table: Base, data_list: Sequence[Mapping]) -> None:
    """
    Load a list of data stored as JSON into a database table

    :param Session db: An open database session
    :param Base table: The table (and therefore type) of entries to create
    :param Sequence[Mapping] list: A list of data objects to load
    """
    for entry in data_list:
        db.add(table(**entry))


def map_source_ids(
    db: Session,
    data_tree_list: Sequence[Mapping[str, Mapping]],
) -> Sequence[Mapping[str, Mapping]]:
    new_tree = []

    for entry in data_tree_list:
        data = entry["node"]
        if "source" in data:
            new_entry = {}
            new_data = {**data}
            source_id = db.query(Source.id).filter_by(name=data["source"]).scalar()
            new_data["source_id"] = source_id
            del new_data["source"]
            new_entry["node"] = new_data
            new_entry["children"] = map_source_ids(
                db, cast(Sequence[Mapping[str, Mapping]], entry["children"])
            )
            new_tree.append(new_entry)

    return new_tree
