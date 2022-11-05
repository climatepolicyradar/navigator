import sqlalchemy as sa
from sqlalchemy import UniqueConstraint

from .auditable import Auditable
from .source import Source
from .geography import Geography
from app.db.session import Base


class DocumentType(Base):
    """A document type.

    E.g. strategy, plan, law
    """

    __tablename__ = "document_type"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text, nullable=False, unique=True)
    description = sa.Column(sa.Text, nullable=False)


class Category(Base):
    """A document category

    Currently:
        Policy, (executive)
        Law, (legislative)
        Case, (litigation)
    """

    __tablename__ = "category"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text, nullable=False, unique=True)
    description = sa.Column(sa.Text, nullable=False)


class Document(Base, Auditable):
    """A document.

    id: Internal database ID
    publication_ts: Publication timestamp, or date of first event
    name: Document title
    description: Document description
    source_url: Reference url to document on third party aggregator
    source_id: Foreign key to original Source table entry
    url: URL to document in CPR cloud storage
    md5_sum: Checksum of the document content
    slug: [TDB] Human readable identifier to be used in URLs
    import_id: [TBD] Unique identifier from the input source
    geography_id: Foreign key to Geography table entry
    type_id: Foreign key to DocumentType table entry
    category_id: Foreign key to Category table entry
    """

    __tablename__ = "document"

    id = sa.Column(sa.Integer, primary_key=True)
    publication_ts = sa.Column(sa.DateTime, nullable=False)
    name = sa.Column(sa.Text, nullable=False)
    description = sa.Column(sa.Text, nullable=False)
    source_url = sa.Column(sa.Text, nullable=True)
    source_id = sa.Column(sa.Integer, sa.ForeignKey(Source.id), nullable=False)
    url = sa.Column(sa.Text, nullable=True)  # TODO: remove
    cdn_object = sa.Column(sa.Text, nullable=True)
    md5_sum = sa.Column(sa.Text, nullable=True)
    content_type = sa.Column(sa.Text, nullable=True)
    postfix = sa.Column(sa.Text, nullable=True)

    slug = sa.Column(
        sa.Text,
        nullable=False,
        unique=True,
        index=True,
    )
    import_id = sa.Column(
        sa.Text,
        nullable=False,
        unique=True,
        index=True,
    )

    geography_id = sa.Column(
        sa.SmallInteger,
        sa.ForeignKey(Geography.id),
        nullable=False,
    )
    type_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(DocumentType.id),
        nullable=False,
    )
    category_id = sa.Column(sa.Integer, sa.ForeignKey(Category.id), nullable=False)
    UniqueConstraint(source_id, import_id)


class Association(Base):  # noqa: D101
    __tablename__ = "association"

    id = sa.Column(sa.Integer, primary_key=True)
    document_id_from = sa.Column(
        sa.Integer,
        sa.ForeignKey(Document.id, ondelete="CASCADE"),
        nullable=False,
    )
    document_id_to = sa.Column(
        sa.Integer,
        sa.ForeignKey(Document.id, ondelete="CASCADE"),
        nullable=False,
    )
    type = sa.Column(sa.Text, nullable=False)
    name = sa.Column(sa.Text, nullable=False)


class Sector(Base):  # noqa: D101
    __tablename__ = "sector"

    id = sa.Column(sa.Integer, primary_key=True)
    parent_id = sa.Column(sa.Integer, sa.ForeignKey("sector.id"))
    name = sa.Column(sa.Text, nullable=False)
    description = sa.Column(sa.Text, nullable=False)
    source_id = sa.Column(sa.Integer, sa.ForeignKey(Source.id), nullable=False)
    UniqueConstraint(name, source_id, parent_id)


class DocumentSector(Base):  # noqa: D101
    __tablename__ = "document_sector"

    id = sa.Column(sa.Integer, primary_key=True)
    sector_id = sa.Column(sa.Integer, sa.ForeignKey(Sector.id), nullable=False)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Document.id, ondelete="CASCADE"),
        nullable=False,
    )


class Instrument(Base):  # noqa: D101
    __tablename__ = "instrument"

    id = sa.Column(sa.Integer, primary_key=True)
    parent_id = sa.Column(sa.Integer, sa.ForeignKey("instrument.id"))
    name = sa.Column(sa.Text, nullable=False)
    description = sa.Column(sa.Text, nullable=False)
    source_id = sa.Column(sa.Integer, sa.ForeignKey(Source.id), nullable=False)
    UniqueConstraint(name, source_id, parent_id)


class DocumentInstrument(Base):  # noqa: D101
    __tablename__ = "document_instrument"

    id = sa.Column(sa.Integer, primary_key=True)
    instrument_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Instrument.id),
        nullable=False,
    )
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Document.id, ondelete="CASCADE"),
        nullable=False,
    )


class Framework(Base):  # noqa: D101
    __tablename__ = "framework"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text, nullable=False, unique=True)
    description = sa.Column(sa.Text, nullable=False)


class DocumentFramework(Base):  # noqa: D101
    __tablename__ = "document_framework"

    id = sa.Column(sa.Integer, primary_key=True)
    framework_id = sa.Column(sa.Integer, sa.ForeignKey(Framework.id), nullable=False)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Document.id, ondelete="CASCADE"),
        nullable=False,
    )


class Response(Base):  # noqa: D101
    # TODO: rename Response -> Topic
    __tablename__ = "response"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text, nullable=False, unique=True)
    description = sa.Column(sa.Text, nullable=False)


class DocumentResponse(Base):  # noqa: D101
    __tablename__ = "document_response"

    id = sa.Column(sa.Integer, primary_key=True)
    response_id = sa.Column(sa.Integer, sa.ForeignKey(Response.id), nullable=False)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Document.id, ondelete="CASCADE"),
        nullable=False,
    )


class Language(Base):  # noqa: D101
    __tablename__ = "language"

    id = sa.Column(sa.SmallInteger, primary_key=True)
    language_code = sa.Column(sa.CHAR(length=3), nullable=False, unique=True)
    part1_code = sa.Column(sa.CHAR(length=2))
    part2_code = sa.Column(sa.CHAR(length=3))
    name = sa.Column(sa.Text)


class DocumentLanguage(Base):
    """A document's languages."""

    __tablename__ = "document_language"

    id = sa.Column(sa.Integer, primary_key=True)
    language_id = sa.Column(sa.Integer, sa.ForeignKey(Language.id), nullable=False)
    document_id = sa.Column(
        sa.Integer, sa.ForeignKey(Document.id, ondelete="CASCADE"), nullable=False
    )


class Hazard(Base):  # noqa: D101
    __tablename__ = "hazard"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text, nullable=False, unique=True)
    description = sa.Column(sa.Text, nullable=False)


class DocumentHazard(Base):  # noqa: D101
    __tablename__ = "document_hazard"

    id = sa.Column(sa.Integer, primary_key=True)
    hazard_id = sa.Column(sa.Integer, sa.ForeignKey(Hazard.id), nullable=False)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Document.id, ondelete="CASCADE"),
        nullable=False,
    )


class Keyword(Base):  # noqa: D101
    """Document keyword."""

    __tablename__ = "keyword"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text, nullable=False)
    description = sa.Column(sa.Text, nullable=False)


class DocumentKeyword(Base):  # noqa: D101
    __tablename__ = "document_keyword"

    id = sa.Column(sa.Integer, primary_key=True)
    keyword_id = sa.Column(sa.Integer, sa.ForeignKey(Keyword.id), nullable=False)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Document.id, ondelete="CASCADE"),
        nullable=False,
    )


class PassageType(Base):  # noqa: D101
    __tablename__ = "passage_type"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text, nullable=False)


class Passage(Base):  # noqa: D101
    __tablename__ = "passage"

    id = sa.Column(sa.BigInteger, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Document.id, ondelete="CASCADE"),
        nullable=False,
    )
    page_id = sa.Column(sa.BigInteger, autoincrement=False, nullable=False)
    passage_type_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(PassageType.id),
        nullable=False,
    )
    parent_passage_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("passage.id"),
    )
    language_id = sa.Column(
        sa.SmallInteger,
        sa.ForeignKey(Language.id),
    )
    text = sa.Column(sa.TEXT(), autoincrement=False, nullable=False)


class Event(Base):  # noqa: D101
    __tablename__ = "event"

    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Document.id, ondelete="CASCADE"),
        nullable=False,
    )
    name = sa.Column(sa.Text, nullable=False)
    description = sa.Column(sa.Text, nullable=False)
    created_ts = sa.Column(sa.DateTime(timezone=True), nullable=False)


class Relationship(Base):  # noqa: D101
    __tablename__ = "relationship"

    id = sa.Column(sa.Integer, primary_key=True)
    type = sa.Column(sa.Text, nullable=False)
    name = sa.Column(sa.Text, nullable=False)
    description = sa.Column(sa.Text, nullable=False)


class DocumentRelationship(Base):  # noqa: D101
    __tablename__ = "document_relationship"

    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Document.id, ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    relationship_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Relationship.id, ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
