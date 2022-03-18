import sqlalchemy as sa

from app.db.session import Base


class User(Base):  # noqa: D101
    __tablename__ = "user"

    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String, unique=True, index=True, nullable=False)
    first_name = sa.Column(sa.String)
    last_name = sa.Column(sa.String)
    hashed_password = sa.Column(sa.String, nullable=False)
    is_active = sa.Column(sa.Boolean, default=True, nullable=False)
    is_superuser = sa.Column(sa.Boolean, default=False, nullable=False)
