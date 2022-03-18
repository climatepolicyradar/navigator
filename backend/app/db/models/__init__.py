import sqlalchemy as sa
from sqlalchemy import BigInteger, SmallInteger

from app.db.session import Base


class PassageType(Base):  # noqa: D101
    __tablename__ = "passage_type"

    passage_type_id = sa.Column(
        sa.INTEGER(),
        primary_key=True,
        server_default=sa.text("nextval('passage_type_passage_type_id_seq'::regclass)"),
        autoincrement=True,
        nullable=False,
    )
    name = sa.Column(sa.VARCHAR(length=255), autoincrement=False, nullable=False)


class MetadataType(Base):  # noqa: D101
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


class MetadataValue(Base):  # noqa: D101
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
        sa.INTEGER(), sa.ForeignKey(MetadataType.metadata_type_id), nullable=False
    )
    value_name = sa.Column(sa.VARCHAR(length=255), autoincrement=False, nullable=False)

    value_description = sa.Column(
        sa.VARCHAR(length=2048),
        autoincrement=False,
        nullable=True,
    )


class MetadataValueKeywords(Base):  # noqa: D101
    __tablename__ = "metadata_value_keywords"

    metadata_keyword_id = sa.Column(
        sa.INTEGER(), primary_key=True, autoincrement=True, nullable=False
    )
    metadata_value_id = sa.Column(
        sa.Integer, sa.ForeignKey(MetadataValue.metadata_value_id), nullable=False
    )

    keyword = sa.Column(sa.VARCHAR(length=255), autoincrement=False, nullable=False)


class Source(Base):  # noqa: D101
    """The action data source.

    CCLW is the only source for alpha.
    Future will be extras like CPD (https://climatepolicydatabase.org/), etc.
    """

    __tablename__ = "source"

    source_id = sa.Column(
        sa.INTEGER(),
        primary_key=True,
        server_default=sa.text("nextval('source_source_id_seq'::regclass)"),
        autoincrement=True,
        nullable=False,
    )
    name = sa.Column(sa.String(128), autoincrement=False, nullable=False)


class Passage(Base):  # noqa: D101
    __tablename__ = "passage"

    passage_id = sa.Column(
        BigInteger, primary_key=True, autoincrement=True, nullable=False
    )
    document_id = sa.Column(
        sa.INTEGER(), sa.ForeignKey("document.document_id"), nullable=False
    )
    page_id = sa.Column(BigInteger, autoincrement=False, nullable=False)
    passage_type_id = sa.Column(
        sa.INTEGER(), sa.ForeignKey(PassageType.passage_type_id), nullable=False
    )
    parent_passage_id = sa.Column(
        sa.INTEGER(), sa.ForeignKey("passage.passage_id"), nullable=True
    )
    language_id = sa.Column(
        SmallInteger, sa.ForeignKey("language.language_id"), nullable=True
    )
    text = sa.Column(sa.TEXT(), autoincrement=False, nullable=False)


class PassageMetadata(Base):  # noqa: D101
    __tablename__ = "passage_metadata"

    passage_id = sa.Column(
        BigInteger, primary_key=True, autoincrement=False, nullable=False
    )
    metadata_value_id = sa.Column(
        sa.INTEGER(),
        sa.ForeignKey(MetadataValue.metadata_value_id),
        primary_key=True,
        nullable=False,
    )
    span_start_pos = sa.Column(sa.SMALLINT(), autoincrement=False, nullable=True)
    span_end_pos = sa.Column(sa.SMALLINT(), autoincrement=False, nullable=True)
    source = sa.Column(sa.INTEGER(), sa.ForeignKey(Source.source_id), nullable=False)
    confidence = sa.Column(sa.REAL(), autoincrement=False, nullable=True)
