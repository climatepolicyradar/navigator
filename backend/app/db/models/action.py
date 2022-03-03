import sqlalchemy as sa
from sqlalchemy import SmallInteger, BigInteger, UniqueConstraint
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from app.db.session import Base


class Action(Base):  # noqa: D101
    __tablename__ = "action"

    action_id = sa.Column(
        sa.INTEGER(),
        primary_key=True,
        server_default=sa.text("nextval('action_action_id_seq'::regclass)"),
        autoincrement=True,
        nullable=False,
    )
    action_source_json = sa.Column(
        postgresql.JSONB(astext_type=sa.Text()),
        autoincrement=False,
        nullable=True,
    )
    name = sa.Column(sa.Text, nullable=False)
    description = sa.Column(sa.Text, nullable=True)
    action_date = sa.Column(sa.DATE(), autoincrement=False, nullable=False)
    geography_id = sa.Column(
        SmallInteger, sa.ForeignKey("geography.geography_id"), nullable=False
    )
    action_type_id = sa.Column(
        sa.Integer, sa.ForeignKey("action_type.action_type_id"), nullable=False
    )
    action_mod_date = sa.Column(
        postgresql.TIMESTAMP(),
        autoincrement=False,
        nullable=True,
    )
    action_source_id = sa.Column(
        BigInteger, sa.ForeignKey("source.source_id"), nullable=False
    )
    UniqueConstraint(name, action_date, geography_id, action_type_id, action_source_id)
    documents = relationship(
        "Document", lazy="noload", primaryjoin="Action.action_id == Document.action_id"
    )


class ActionMetadata(Base):  # noqa: D101
    __tablename__ = "action_metadata"

    action_metadata_id = sa.Column(
        sa.INTEGER(), primary_key=True, autoincrement=True, nullable=False
    )
    action_id = sa.Column(sa.INTEGER(), sa.ForeignKey(Action.action_id), nullable=False)
    metadata_value_id = sa.Column(
        sa.INTEGER(), sa.ForeignKey("metadata_value.metadata_value_id"), nullable=False
    )


class ActionSourceMetadata(Base):  # noqa: D101
    __tablename__ = "action_source_metadata"

    action_source_metadata_id = sa.Column(
        sa.INTEGER(),
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    metadata_type_id = sa.Column(
        sa.INTEGER(), sa.ForeignKey("metadata_type.metadata_type_id"), nullable=False
    )
    value = sa.Column(sa.VARCHAR(length=1024), autoincrement=False, nullable=False)
    action_id = sa.Column(sa.INTEGER(), sa.ForeignKey(Action.action_id), nullable=False)
