import enum
from sqlalchemy import (
    Column,
    Enum,
    Integer,
    Text,
    ForeignKey,
    Boolean,
)
from sqlalchemy.dialects.postgresql import ARRAY
from app.db.session import Base
from . import Sector, Geography


class LitBody(Base):  # noqa: D101
    """Database model for a Litigation body /  legal entity."""

    __tablename__ = "lit_body"

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)
    description = Column(Text)


class CaseStatus(str, enum.Enum):
    """The current status of a Case."""

    OPEN = "Open"
    OPEN_APPEAL = "Open - under appeal"
    CLOSED_SETTLED = "Closed - settled"
    CLOSED_WITHDRAWN = "Closed - withdrawn"
    CLOSED = "Closed"


class UNFCCCPillars(str, enum.Enum):
    """The UNFCCC Pillars"""

    ADAPTATION_RESILIENCE = "Adaptation & Resilience"
    MITIGATION = "Mitigation"
    LOSS_DAMAGE = "Loss & Damage"


class CaseOutcome(str, enum.Enum):
    """The outcome of a Case."""

    ENHANCED_CLIMATE_ACTION = "Enhanced climate action"
    NEUTRAL = "Neutral"
    HINDERED_CLIMATE_ACTION = "Hindered climate action"
    NA = "N/A"


class ClimateAlignmentClass(str, enum.Enum):
    """The class of climate alignment."""

    CLIMATE_ALIGNED = "Climate aligned"
    CLIMATE_NON_ALIGNED = "Climate non-aligned"
    JUST_TRANSITION = "Just transition"


class StrategicAlignmentClass(str, enum.Enum):
    """The class of strategic alignment."""

    ENFORCING_CLIMATE_STANDARDS = "Enforcing climate standards"
    GOVERNMENT_FRAMEWORK = "Government framework"
    PUBLIC_FINANCE = "Public finance"
    FAILURE_TO_ADAPT = "Failure to adapt"
    COMPENSATION = "Compensation"
    CLIMATE_WASHING = "Climate-washing"
    PERSONAL_RESPONSIBILITY = "Personal responsibility"
    REGULATORY_POWERS = "Regulatory powers"
    SLAPP = "Strategic litigation against public participation (SLAPP)"
    JUST_TRANSITION = "Just transition"
    CORPORATE_FRAMEWORK = "Corporate framework"
    OTHER = "Other"
    NA = "N/A"


class Case(Base):  # noqa: D101
    """Database model for a Litigation case."""

    __tablename__ = "lit_case"

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)
    year = Column(Integer)
    status = Column(Enum(CaseStatus))
    outcome = Column(Enum(CaseOutcome))
    objective = Column(Text)
    pillars = Column(Enum(UNFCCCPillars))
    summary = Column(Text)
    reference = Column(Text)
    case_class = Column(Text)
    strategic = Column(Boolean)
    alignment_class = Column(Enum(ClimateAlignmentClass))
    strategic_class = Column(Enum(StrategicAlignmentClass))
    source = Column(Text)
    keywords = Column(ARRAY(Text))

    geography_id = (Integer, ForeignKey(Geography.id))
    body_id = Column(Integer, ForeignKey(LitBody.id))
    sector_id = Column(Integer, ForeignKey(Sector.id))
