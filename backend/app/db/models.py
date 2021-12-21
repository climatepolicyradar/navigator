import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from .session import Base


class User(Base):
    __tablename__ = "user"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    email = sa.Column(sa.String, unique=True, index=True, nullable=False)
    first_name = sa.Column(sa.String)
    last_name = sa.Column(sa.String)
    hashed_password = sa.Column(sa.String, nullable=False)
    is_active = sa.Column(sa.Boolean, default=True)
    is_superuser = sa.Column(sa.Boolean, default=False)


class PassageType(Base):
    __tablename__ = "passage_type"

    passage_type_id = sa.Column(
        sa.INTEGER(),
        primary_key=True,
        server_default=sa.text("nextval('passage_type_passage_type_id_seq'::regclass)"),
        autoincrement=True,
        nullable=False,
    )
    name = sa.Column(sa.VARCHAR(length=255), autoincrement=False, nullable=False)


class MetadataType(Base):
    __tablename__ = "metadata_type"

    metadata_type_id = sa.Column(
        sa.INTEGER(),
        primary_key=True,
        server_default=sa.text(
            "nextval('metadata_type_metadata_type_id_seq'::regclass)"
        ),
        autoincrement=True,
        nullable=False,
    )

    type_name = sa.Column(sa.VARCHAR(length=128), autoincrement=False, nullable=False)

    type_description = sa.Column(
        sa.VARCHAR(length=2048),
        autoincrement=False,
        nullable=True,
    )


class MetadataValue(Base):
    __tablename__ = "metadata_value"

    metadata_value_id = sa.Column(
        sa.INTEGER(),
        primary_key=True,
        server_default=sa.text(
            "nextval('metadata_value_metadata_value_id_seq'::regclass)"
        ),
        autoincrement=True,
        nullable=False,
    )

    metadata_type_id = sa.Column(
        "metadata_type_id", sa.INTEGER(), autoincrement=False, nullable=False
    )
    value_name = sa.Column(sa.VARCHAR(length=255), autoincrement=False, nullable=False)

    value_description = sa.Column(
        sa.VARCHAR(length=2048),
        autoincrement=False,
        nullable=True,
    )


class MetadataValueKeywords(Base):
    __tablename__ = "metadata_value_keywords"

    metadata_keyword_id = sa.Column(
        sa.INTEGER(), primary_key=True, autoincrement=True, nullable=False
    )
    metadata_value_id = sa.Column(sa.INTEGER(), autoincrement=False, nullable=False)

    keyword = sa.Column(sa.VARCHAR(length=255), autoincrement=False, nullable=False)


class Language(Base):
    __tablename__ = "language"

    language_id = sa.Column(
        sa.INTEGER(), primary_key=True, autoincrement=True, nullable=False
    )
    language_code = sa.Column(sa.CHAR(length=3), autoincrement=False, nullable=False)
    part1_code = sa.Column(sa.CHAR(length=2), autoincrement=False, nullable=False)
    part2_code = sa.Column(sa.CHAR(length=3), autoincrement=False, nullable=False)
    name = sa.Column(sa.VARCHAR(length=128), autoincrement=False, nullable=True)


class Geography(Base):
    __tablename__ = "geography"

    geography_id = sa.Column(
        sa.INTEGER(),
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
        nullable=False,
    )


class Source(Base):
    __tablename__ = "source"

    source_id = sa.Column(
        sa.INTEGER(),
        primary_key=True,
        server_default=sa.text("nextval('source_source_id_seq'::regclass)"),
        autoincrement=True,
        nullable=False,
    )
    name = sa.Column(sa.CHAR(length=1024), autoincrement=False, nullable=False)


class ActionType(Base):
    __tablename__ = "action_type"

    action_type_id = sa.Column(
        sa.INTEGER(),
        primary_key=True,
        server_default=sa.text("nextval('action_type_action_type_id_seq'::regclass)"),
        autoincrement=True,
        nullable=False,
    )
    action_parent_type_id = sa.Column(sa.INTEGER(), autoincrement=False, nullable=True)
    type_name = sa.Column(sa.VARCHAR(length=255), autoincrement=False, nullable=False)
    type_description = sa.Column(
        sa.VARCHAR(length=2048),
        autoincrement=False,
        nullable=True,
    )


class Action(Base):
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
    name = sa.Column(sa.VARCHAR(length=255), autoincrement=False, nullable=False)
    description = sa.Column(sa.VARCHAR(length=2048), autoincrement=False, nullable=True)
    action_date = sa.Column(sa.DATE(), autoincrement=False, nullable=False)
    geography_id = sa.Column(sa.INTEGER(), autoincrement=False, nullable=False)
    action_type_id = sa.Column(sa.INTEGER(), autoincrement=False, nullable=False)
    action_mod_date = sa.Column(
        postgresql.TIMESTAMP(),
        autoincrement=False,
        nullable=True,
    )
    action_source_id = sa.Column(sa.INTEGER(), autoincrement=False, nullable=False)


class ActionMetadata(Base):
    __tablename__ = "action_metadata"

    action_metadata_id = sa.Column(
        sa.INTEGER(), primary_key=True, autoincrement=True, nullable=False
    )
    action_id = sa.Column(sa.INTEGER(), autoincrement=False, nullable=False)
    metadata_value_id = sa.Column(sa.INTEGER(), autoincrement=False, nullable=False)


class ActionSourceMetadata(Base):
    __tablename__ = "action_source_metadata"

    action_source_metadata_id = sa.Column(
        sa.INTEGER(),
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    metadata_type_id = sa.Column(sa.INTEGER(), autoincrement=False, nullable=False)
    value = sa.Column(sa.VARCHAR(length=1024), autoincrement=False, nullable=False)
    action_id = sa.Column(sa.INTEGER(), autoincrement=False, nullable=False)


class Document(Base):
    __tablename__ = "document"

    document_id = sa.Column(
        sa.INTEGER(), primary_key=True, autoincrement=True, nullable=False
    )
    action_id = sa.Column(sa.INTEGER(), autoincrement=False, nullable=False)
    document_date = sa.Column(
        postgresql.TIMESTAMP(), autoincrement=False, nullable=False
    )
    name = sa.Column(sa.VARCHAR(length=255), autoincrement=False, nullable=False)
    source_url = sa.Column(sa.VARCHAR(length=1024), autoincrement=False, nullable=True)
    s3_url = sa.Column(sa.VARCHAR(length=1024), autoincrement=False, nullable=True)
    language_id = sa.Column(sa.INTEGER(), autoincrement=False, nullable=True)
    document_mod_date = sa.Column(
        postgresql.TIMESTAMP(),
        autoincrement=False,
        nullable=True,
    )


class Passage(Base):
    __tablename__ = "passage"

    passage_id = sa.Column(
        sa.INTEGER(), primary_key=True, autoincrement=True, nullable=False
    )
    document_id = sa.Column(sa.INTEGER(), autoincrement=False, nullable=False)
    page_id = sa.Column(sa.INTEGER(), autoincrement=False, nullable=False)
    passage_type_id = sa.Column(sa.INTEGER(), autoincrement=False, nullable=False)
    parent_passage_id = sa.Column(sa.INTEGER(), autoincrement=False, nullable=True)
    language_id = sa.Column(sa.INTEGER(), autoincrement=False, nullable=True)
    text = sa.Column(sa.TEXT(), autoincrement=False, nullable=False)


class PassageMetadata(Base):
    __tablename__ = "passage_metadata"

    passage_id = sa.Column(
        sa.INTEGER(), primary_key=True, autoincrement=False, nullable=False
    )
    metadata_value_id = sa.Column(
        sa.INTEGER(), primary_key=True, autoincrement=False, nullable=False
    )
    span_start_pos = sa.Column(sa.SMALLINT(), autoincrement=False, nullable=True)
    span_end_pos = sa.Column(sa.SMALLINT(), autoincrement=False, nullable=True)
    source = sa.Column(sa.INTEGER(), autoincrement=False, nullable=False)
    confidence = sa.Column(sa.REAL(), autoincrement=False, nullable=True)
