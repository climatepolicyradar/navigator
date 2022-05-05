"""Note

TODO at the moment, this is mostly a copy of backend's models.
Once the migration is done and the code works, and is tested, then put the common part
of the model in the common module.

Note that for all tables that depend on:
- geography_id
- document_type_id
- source_id
- language_id

As geographies, doc types, sources, and languages are constant, it makes sense for the lookups
to live in one place. We decided for that place to be the backend API.
Therefore, the loader would make (cached) lookups for the IDs above.
The IDs can then be posted as-is, as the IDs are guaranteed to exist in the API DB.
"""

import enum

import sqlalchemy as sa
from sqlalchemy import UniqueConstraint
from sqlalchemy.sql import func

from app.db.session import Base


class Auditable:  # noqa: D101
    created_ts = sa.Column(sa.DateTime(timezone=True), server_default=func.now())
    updated_ts = sa.Column(sa.DateTime(timezone=True), onupdate=func.now())


class DocumentInvalidReason(enum.Enum):
    """Reasons why a document might be invalid."""

    unsupported_content_type = "unsupported_content_type"
    net_ssl_error = "net_ssl_error"
    net_read_error = "net_read_error"
    net_connection_error = "net_connection_error"
    net_too_many_redirects = "net_too_many_redirects"
    net_remote_protocol_error = "net_remote_protocol_error"


class Document(Base, Auditable):
    """A document.

    source_url: Reference url to document on third party aggregator
    url: URL to document in CPR cloud storage

    source_id: from the lookup via the API
    geography_id: from the lookup via the API
    type_id: from the lookup via the API
    """

    __tablename__ = "document"

    id = sa.Column(sa.Integer, primary_key=True)
    # created_by = sa.Column(sa.Integer, sa.ForeignKey(User.id))
    # updated_by = sa.Column(sa.Integer, sa.ForeignKey(User.id))
    loaded_ts = sa.Column(sa.DateTime(timezone=True), server_default=func.now())
    name = sa.Column(sa.Text, nullable=False)
    description = sa.Column(sa.Text, nullable=False)
    source_url = sa.Column(sa.Text)
    source_id = sa.Column(sa.Integer, nullable=False)
    url = sa.Column(sa.Text)

    is_valid = sa.Column(sa.Boolean, nullable=False)
    invalid_reason = sa.Column(sa.Enum(DocumentInvalidReason))

    geography_id = sa.Column(sa.SmallInteger, nullable=False)
    type_id = sa.Column(sa.Integer, nullable=False)
    category_id = sa.Column(sa.SmallInteger, nullable=False)
    UniqueConstraint(name, geography_id, type_id, source_id, source_url)


class APIDocument(Base, Auditable):
    """A pointer to the document's ID in the API database."""

    __tablename__ = "api_document"

    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Document.id, ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    remote_document_id = sa.Column(sa.Integer, nullable=False)


class Sector(Base):
    """A document's sector.

    source_id: from the lookup via the API
    """

    __tablename__ = "sector"

    id = sa.Column(sa.Integer, primary_key=True)
    parent_id = sa.Column(sa.Integer, sa.ForeignKey("sector.id"))
    name = sa.Column(sa.Text, nullable=False)
    description = sa.Column(sa.Text, nullable=False)
    source_id = sa.Column(sa.Integer, nullable=False)

    def as_dict(self):  # noqa: D102
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name not in ["id", "parent_id"]
        }


class DocumentSector(Base):  # noqa: D101
    __tablename__ = "document_sector"

    id = sa.Column(sa.Integer, primary_key=True)
    sector_id = sa.Column(sa.Integer, sa.ForeignKey(Sector.id), nullable=False)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Document.id, ondelete="CASCADE"),
        nullable=False,
    )


class Instrument(Base):
    """A document's instrument.

    source_id: from the lookup via the API
    """

    __tablename__ = "instrument"

    id = sa.Column(sa.Integer, primary_key=True)
    parent_id = sa.Column(sa.Integer, sa.ForeignKey("instrument.id"))
    name = sa.Column(sa.Text, nullable=False)
    description = sa.Column(sa.Text, nullable=False)
    source_id = sa.Column(sa.Integer, nullable=False)

    def as_dict(self):  # noqa: D102
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name not in ["parent_id", "id"]
        }


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
    name = sa.Column(sa.Text, nullable=False)
    description = sa.Column(sa.Text, nullable=False)

    def as_dict(self):  # noqa: D102
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name not in ["id"]
        }


class DocumentFramework(Base):  # noqa: D101
    __tablename__ = "document_framework"

    id = sa.Column(sa.Integer, primary_key=True)
    framework_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Framework.id),
        nullable=False,
    )
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Document.id, ondelete="CASCADE"),
        nullable=False,
    )


class Response(Base):  # noqa: D101
    __tablename__ = "response"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text, nullable=False)
    description = sa.Column(sa.Text, nullable=False)

    def as_dict(self):  # noqa: D102
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name not in ["id"]
        }


class DocumentResponse(Base):  # noqa: D101
    __tablename__ = "document_response"

    id = sa.Column(sa.Integer, primary_key=True)
    response_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Response.id),
        nullable=False,
    )
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Document.id, ondelete="CASCADE"),
        nullable=False,
    )


class Hazard(Base):  # noqa: D101
    __tablename__ = "hazard"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text, nullable=False)
    description = sa.Column(sa.Text, nullable=False)

    def as_dict(self):  # noqa: D102
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name not in ["id"]
        }


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


class DocumentLanguage(Base):
    """A document's languages.

    language_id: from the lookup via the API
    """

    __tablename__ = "document_language"

    id = sa.Column(sa.Integer, primary_key=True)
    language_id = sa.Column(sa.Integer, nullable=False)
    document_id = sa.Column(
        sa.Integer, sa.ForeignKey(Document.id, ondelete="CASCADE"), nullable=False
    )


class PassageType(Base):  # noqa: D101
    __tablename__ = "passage_type"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text, nullable=False)


class Passage(Base):
    """A passage.

    language_id: from the lookup via the API
    """

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
    created_ts = sa.Column(sa.DateTime(timezone=True), server_default=func.now())

    def as_dict(self):  # noqa: D102
        d = {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name not in ["document_id", "id", "created_ts"]  # do date separately
        }
        d["created_ts"] = getattr(self, "created_ts").isoformat()
        return d


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
