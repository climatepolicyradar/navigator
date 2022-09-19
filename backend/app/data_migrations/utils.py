from typing import Mapping, Optional, Sequence, cast

from app.db.session import Base

from sqlalchemy.orm import Session


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
    Load a list od data stored as JSON into a database table

    :param Session db: An open database session
    :param Base table: The table (and therefore type) of entries to create
    :param Sequence[Mapping] list: A list of data objects to load
    """
    for entry in data_list:
        db.add(table(**entry))
