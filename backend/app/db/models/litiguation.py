import enum
from sqlalchemy import (
    Column,
    Enum,
    Integer,
    Text,
    ForeignKey,
    Date,
)

from app.db.session import Base
from . import Case, Keyword, Document


class LitCaseKeyword(Base):  # noqa: D101
    __tablename__ = "lit_case_keyword"

    keyword_id = Column(
        Integer, ForeignKey(Keyword.id), nullable=False, primary_key=True
    )
    case_id = Column(
        Integer,
        ForeignKey(Case.id, ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )


# --------------------------------------------------
# Laws (Internal & External)
# --------------------------------------------------


class LitCaseInternalLaws(Base):  # noqa: D101
    __tablename__ = "lit_case_int_laws"

    document_id = Column(
        Integer, ForeignKey(Document.id), nullable=False, primary_key=True
    )
    case_id = Column(
        Integer,
        ForeignKey(Case.id, ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )


class LitExternalLaw(Base):  # noqa: D101
    __tablename__ = "lit_external_law"

    id = Column(Integer, primary_key=True)

    name = Column(Text, nullable=False)
    url = Column(Text, nullable=False)


class LitCaseExternalLaws(Base):  # noqa: D101
    __tablename__ = "lit_case_ext_laws"

    extlaw_id = Column(
        Integer, ForeignKey(LitExternalLaw.id), nullable=False, primary_key=True
    )
    case_id = Column(
        Integer,
        ForeignKey(Case.id, ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )


# --------------------------------------------------
# Party
# --------------------------------------------------


class LitPartyType(str, enum.Enum):
    """The type of Party involved in a case."""

    GOVERNMENT = "Government"
    SUBNATIONAL_GOVERNMENT = "Subnational government"
    INDIVIDUAL = "Individual"
    INDIVIDUAL_SUPPORTED_BY_NGO = "Individual supported by NGO"
    NGO = "NGO"
    CORPORATION = "Corporation"
    CORPORATION_SUPPORTED_BY_NGO = "Corporation supported by NGO"
    INDIGENOUS_GOVERNMENT_TRIBAL = "Indigenous government (tribal government)"
    TRADE_ASSOCIATION = "Trade association"
    SUPRANATIONAL_LEGAL_BODY = "Supranational legal body"
    INDIVIDUAL_REPRESENTING_CORPORATION = "Individual representing corporation"


class LitSideType(str, enum.Enum):
    """The role of the party in the particular case."""

    FILING_PARTY = "Filing party"
    RESPONDING_PARTY = "Responding party"
    INTERVENOR = "Intervenor"


class LitParty(Base):  # noqa: D101
    """Database model for a Litigation party."""

    __tablename__ = "lit_party"

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)
    party_type = Column(Enum(LitPartyType))
    side_type = Column(Enum(LitSideType))


class LitCaseParties(Base):  # noqa: D101
    """Database model for a Litigation party."""

    __tablename__ = "lit_case_parties"

    id = Column(Integer, primary_key=True)
    case_id = Column(Integer, ForeignKey(Case.id))
    party_id = Column(Integer, ForeignKey(LitParty.id))


# --------------------------------------------------
# Document
# --------------------------------------------------


class LitDocument(Base):  # noqa: D101
    """Database model for a Litigation document."""

    __tablename__ = "lit_document"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    case_id = Column(
        Integer, ForeignKey(Case.id)
    )  # Not sure if we should have this nullable (if its part of an event)
    language = Column(Text, nullable=False)


# --------------------------------------------------
# Event
# --------------------------------------------------


class LitEventType(str, enum.Enum):
    """The type of event in a litigation case."""

    FILING = "Filing"
    CLAIMANT_DOCUMENT_OTHER = "Claimant document: other"
    DEFENDANT_DOCUMENT = "Defendant document"
    DECISION = "Decision"
    INTERIM_DECISION = "Interim decision"
    INTERVENOR_DOCUMENT = "Intervenor document"
    HEARING = "Hearing"
    SETTLEMENT = "Settlement"
    WITHDRAWAL = "Withdrawal"
    OTHER = "Other"
    APPEAL = "Appeal"
    PRE_ACTION_EVENT = "Pre-action event"


class LitEvent(Base):  # noqa: D101
    """Database model for a Litigation event."""

    __tablename__ = "lit_event"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text)

    type = Column(Enum(LitEventType))
    date = Column(Date, nullable=False)
    case_id = Column(Integer, ForeignKey(Case.id))


class LitEventDocuments(Base):  # noqa: D101
    """Database model for the link table between Litigation event and documents."""

    __tablename__ = "lit_event_documents"

    event_id = Column(Integer, ForeignKey(LitEvent.id), primary_key=True)
    document_id = Column(Integer, ForeignKey(LitDocument.id), primary_key=True)
