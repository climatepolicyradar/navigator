"""Models.

Some of these tables are lookup tables, i.e. the ones which have a DocumentXXX counterpart.

Values for these lookups can be found here:
https://www.notion.so/climatepolicyradar/External-Pre-Existing-Classifications-0409cd1a01d44362b48b34c24d10cd4c

However, for now we write the values into the lookups as they come from the uploader.
As more sources come online, we'll set up a mapping between the source's term, and our term
(the latter which is currently based on CCLW).


These lookups are global:
- language
- geography
- source
- category
- framework
- hazard
- response (named 'topic' outside the app)

These lookups are source-specific:
- instrument
- sector
"""

import sqlalchemy as sa
from sqlalchemy import UniqueConstraint
from sqlalchemy.sql import func

from app.db.session import Base


class Auditable:  # noqa: D101
    created_ts = sa.Column(sa.DateTime(timezone=True), server_default=func.now())
    updated_ts = sa.Column(sa.DateTime(timezone=True), onupdate=func.now())


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


class Language(Base):  # noqa: D101
    __tablename__ = "language"

    id = sa.Column(sa.SmallInteger, primary_key=True)
    language_code = sa.Column(sa.CHAR(length=3), nullable=False, unique=True)
    part1_code = sa.Column(sa.CHAR(length=2))
    part2_code = sa.Column(sa.CHAR(length=3))
    name = sa.Column(sa.Text)


class Geography(Base):  # noqa: D101
    __tablename__ = "geography"

    id = sa.Column(sa.SmallInteger, primary_key=True)
    # to display to end-users
    display_value = sa.Column(sa.Text, unique=True)
    # e.g. ISO code, World Bank, etc - not necessarily for display
    # non-unique, as some unrecognised territories might share the same code, e.g.
    # at the time of writing, "Sahrawi Republic" and "Western Sahara" both share "ESH"
    value = sa.Column(sa.Text)
    type = sa.Column(sa.Text)
    parent_id = sa.Column(sa.Integer, sa.ForeignKey("geography.id"))


class Source(Base):  # noqa: D101
    """The action data source.

    CCLW is the only source for alpha.
    Future will be extras like CPD (https://climatepolicydatabase.org/), etc.
    """

    __tablename__ = "source"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(128), nullable=False, unique=True)


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

    E.g. Policy, Law (executive, legislative as per CCLW)
    """

    __tablename__ = "category"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text, nullable=False, unique=True)
    description = sa.Column(sa.Text, nullable=False)


class Document(Base, Auditable):
    """A document.

    source_url: Reference url to document on third party aggregator
    url: URL to document in CPR cloud storage
    """

    __tablename__ = "document"

    id = sa.Column(sa.Integer, primary_key=True)
    created_by = sa.Column(sa.Integer, sa.ForeignKey(User.id))
    updated_by = sa.Column(sa.Integer, sa.ForeignKey(User.id))
    loaded_ts = sa.Column(sa.DateTime(timezone=True), onupdate=func.now())
    name = sa.Column(sa.Text, nullable=False)
    source_url = sa.Column(sa.Text)
    source_id = sa.Column(sa.Integer, sa.ForeignKey(Source.id), nullable=False)
    url = sa.Column(sa.Text)

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
    UniqueConstraint(name, geography_id, type_id, source_id, source_url)


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


class Response(Base):
    """A response.

    Response is called 'topic' outside the app.
    """

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
    created_ts = sa.Column(sa.DateTime(timezone=True), server_default=func.now())


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


class DocumentLanguage(Base):
    """A document's languages."""

    __tablename__ = "document_language"

    id = sa.Column(sa.Integer, primary_key=True)
    language_id = sa.Column(sa.Integer, sa.ForeignKey(Language.id), nullable=False)
    document_id = sa.Column(
        sa.Integer, sa.ForeignKey(Document.id, ondelete="CASCADE"), nullable=False
    )
