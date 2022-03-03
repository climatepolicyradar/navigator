import sqlalchemy as sa
from sqlalchemy import SmallInteger

from app.db.session import Base


class Language(Base):  # noqa: D101
    __tablename__ = "language"

    language_id = sa.Column(
        SmallInteger, primary_key=True, autoincrement=True, nullable=False
    )
    language_code = sa.Column(sa.CHAR(length=3), autoincrement=False, nullable=False)
    part1_code = sa.Column(sa.CHAR(length=2), autoincrement=False, nullable=True)
    part2_code = sa.Column(sa.CHAR(length=3), autoincrement=False, nullable=True)
    name = sa.Column(sa.VARCHAR(length=128), autoincrement=False, nullable=True)


class Geography(Base):  # noqa: D101
    __tablename__ = "geography"

    geography_id = sa.Column(
        SmallInteger,
        primary_key=True,
        server_default=sa.text("nextval('geography_geography_id_seq'::regclass)"),
        autoincrement=True,
        nullable=False,
    )
    country_code = sa.Column(sa.CHAR(length=3), autoincrement=False, nullable=False)
    english_shortname = sa.Column(
        sa.VARCHAR(length=128),
        autoincrement=False,
        nullable=False,
    )
    french_shortname = sa.Column(
        sa.VARCHAR(length=128),
        autoincrement=False,
        nullable=True,
    )


class ActionType(Base):  # noqa: D101
    __tablename__ = "action_type"

    action_type_id = sa.Column(
        sa.INTEGER(),
        primary_key=True,
        server_default=sa.text("nextval('action_type_action_type_id_seq'::regclass)"),
        autoincrement=True,
        nullable=False,
    )
    # TODO FK?
    action_parent_type_id = sa.Column(sa.INTEGER(), autoincrement=False, nullable=True)
    type_name = sa.Column(sa.VARCHAR(length=255), autoincrement=False, nullable=False)
    type_description = sa.Column(
        sa.VARCHAR(length=2048),
        autoincrement=False,
        nullable=True,
    )
