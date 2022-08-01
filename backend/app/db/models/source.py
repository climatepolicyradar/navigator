import sqlalchemy as sa
from sqlalchemy.sql import func

from app.db.session import Base


class Source(Base):  # noqa: D101
    """The action data source.

    CCLW is the only source for alpha.
    Future will be extras like CPD (https://climatepolicydatabase.org/), etc.
    """

    __tablename__ = "source"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(128), nullable=False, unique=True)
