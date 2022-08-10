import logging
import os
from subprocess import STDOUT, check_output
from typing import Any, cast

from sqlalchemy.engine import Engine
from sqlalchemy.sql import text

_incomparable_lines = {
    "    AS integer"  # this gets made in models, but not integrations
}

logger = logging.getLogger(__name__)


class PytestHelpers:  # noqa: D101
    def __init__(self, engine: Engine):
        self.engine = engine

    def _get_psql_compatible_url(self) -> str:
        # psql doesn't like the + syntax that is sometimes used in sqlalchemy
        return str(self.engine.url).replace("+psycopg2", "")

    def upgrade(self, migration_id: str) -> str:
        """Run the alembic upgrade command."""
        cmd = (
            f"PYTHONPATH=. "
            f"DATABASE_URL={self.engine.url} "
            f"alembic upgrade {migration_id}"
        )
        print(
            f"""--- Alembic upgrade ---
        |CWD: {os.getcwd()}
        |CMD: {cmd}
        """
        )
        out = check_output(cmd, shell=True, stderr=STDOUT).decode("utf-8")
        print(
            f"""|STDOUT:
        |{out}
        """.replace(
                "        |", ""
            )
        )
        return out

    def get_schema_str(self) -> str:
        """Get the db schema as SQL, this can be quite a big string."""
        url = self._get_psql_compatible_url()
        cmd = f"pg_dump {url} --schema-only"
        output = check_output(cmd, shell=True)
        return "\n".join(
            line
            for line in output.decode("utf-8").splitlines()
            if line and not line.startswith("--")
        )

    @staticmethod
    def assert_schema_strs_similar(a: str, b: str) -> None:
        """Rudimentary assertion to allow for column reordering on DROP, ADD.

        Long run, we should replace this with the alembic-verify package:

            alembic-verify.readthedocs.io

        """
        if os.environ.get("ALEMBIC_DEBUG"):
            open("a.sql", "w").write(a)
            open("b.sql", "w").write(b)
        lines_a, set_a = PytestHelpers._split_and_filter(a)
        lines_b, set_b = PytestHelpers._split_and_filter(b)

        if set_a != set_b:
            logger.error("Run pytest with -s to see differences!")
            print("\n\nIn models, but not migrations:\n")
            for line in set_a - set_b:
                print(line)
            print("\n\nIn migrations, but not models:\n")
            for line in set_b - set_a:
                print(line)
            print("Run again with ALEMBIC_DEBUG=1 to output schemas")

        assert set_a == set_b
        assert len(lines_a) == len(lines_b)

    @staticmethod
    def _split_and_filter(a):
        lines_a = [
            line
            for line in a.replace(",", "").splitlines()
            if line not in _incomparable_lines
        ]
        set_a = set(lines_a)
        return lines_a, set_a

    def execute(self, sql: str) -> None:
        """Execute sql."""
        conn = cast(Any, self.engine.connect())
        conn.execute(text(sql))
        conn.close()

    def drop_all(self) -> None:
        """Drop all of the tables/indexes etc."""
        self.execute("DROP SCHEMA public CASCADE")
        self.execute("CREATE SCHEMA public")

    def add_alembic(self) -> None:
        """Add alembic migration table to test DB."""
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS alembic_version (
               version_num VARCHAR(32) NOT NULL,
               CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
            )
            """
        )


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
