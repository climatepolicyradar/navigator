"""
class DBConnector:
- connect to database using env variables
- provides dataframe given sql query
"""

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
import pandas as pd


class PostgresConnector:
    def __init__(self, username: str, password: str, hostname: str):
        """Initialise DB connector.

        Args:
            username (str): _description_
            password (str): _description_
            hostname (str): _description_
        """

        self._db_engine = self._create_db_engine(username, password, hostname)

    @staticmethod
    def _make_postgres_url(username: str, password: str, hostname: str) -> str:
        return f"postgresql://{username}:{password}@{hostname}"

    def _create_db_engine(self, username: str, password: str, hostname: str) -> Engine:
        """Create a SQLAlchemy engine used to connect to the database.

        Args:
            username (str): _description_
            password (str): _description_
            hostname (str): _description_
        """

        db_url = self._make_postgres_url(username, password, hostname)

        return create_engine(db_url)

    def run_query(self, query: str) -> pd.DataFrame:
        """Run SQL query, returning a dataframe of results.

        Args:
            query (str): SQL query.

        Returns:
            pd.DataFrame
        """

        return pd.read_sql_query(query, self._db_engine)
