from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
import pandas as pd


class PostgresConnector:
    """Connect to a postgres instance and run a query."""

    def __init__(self, postgres_url: str):
        """Initialise DB connector.

        Args:
            postgres_url: URL to postgres instance
        """

        self._db_engine = self._create_db_engine(postgres_url)

    def _create_db_engine(self, postgres_url: str) -> Engine:
        """Create a SQLAlchemy engine used to connect to the database.

        Args:
            postgres_url (str): url to postgres database.
        """

        return create_engine(postgres_url)

    def run_query(self, query: str) -> pd.DataFrame:
        """Run SQL query, returning a dataframe of results.

        Args:
            query (str): SQL query.

        Returns:
            pd.DataFrame
        """

        return pd.read_sql_query(query, self._db_engine)
