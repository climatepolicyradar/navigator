import sqlalchemy as sa

from .auditable import Auditable
from app.db.session import Base


class User(Base, Auditable):  # noqa: D101
    __tablename__ = "user"

    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String, unique=True, index=True, nullable=False)
    names = sa.Column(sa.String)
    hashed_password = sa.Column(sa.String)
    is_active = sa.Column(sa.Boolean, default=False, nullable=False)
    is_superuser = sa.Column(sa.Boolean, default=False, nullable=False)
    job_role = sa.Column(sa.String)
    location = sa.Column(sa.String)
    affiliation_organisation = sa.Column(sa.String)
    affiliation_type = sa.Column(sa.ARRAY(sa.Text))
    policy_type_of_interest = sa.Column(sa.ARRAY(sa.Text))
    geographies_of_interest = sa.Column(sa.ARRAY(sa.Text))
    data_focus_of_interest = sa.Column(sa.ARRAY(sa.Text))


class PasswordResetToken(Base, Auditable):  # noqa: D101
    __tablename__ = "password_reset_token"

    id = sa.Column(sa.BigInteger, primary_key=True)
    token = sa.Column(sa.Text, unique=True, nullable=False)
    expiry_ts = sa.Column(sa.DateTime, nullable=False)
    is_redeemed = sa.Column(sa.Boolean, nullable=False, default=False)
    is_cancelled = sa.Column(sa.Boolean, nullable=False, default=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id), nullable=False)
