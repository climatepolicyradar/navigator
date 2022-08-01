import sqlalchemy as sa
from sqlalchemy.sql import func


class Auditable:  # noqa: D101
    created_ts = sa.Column(sa.DateTime(timezone=True), server_default=func.now())
    updated_ts = sa.Column(sa.DateTime(timezone=True), onupdate=func.now())
