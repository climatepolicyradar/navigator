import logging
import os
import pathlib
from subprocess import STDOUT, check_output
from typing import Any, cast

from sqlalchemy.engine import Engine
from sqlalchemy.sql import text


def clean_tables(session, exclude, sqlalchemy_base):
    """Clean (aka: truncate) table.  SQLAlchemy models listed in exclude will be skipped."""
    non_static_tables = [
        t for t in reversed(sqlalchemy_base.metadata.sorted_tables) if t not in exclude
    ]
    for table in non_static_tables:
        # "DELETE FROM $table" is quicker than TRUNCATE for small tables
        session.execute(table.delete())

    # reset all the sequences
    sql = "SELECT c.relname FROM pg_class c WHERE c.relkind = 'S'"
    for [sequence] in session.execute(text(sql)):
        session.execute(text(f"ALTER SEQUENCE {sequence} RESTART WITH 1"))

    session.commit()
