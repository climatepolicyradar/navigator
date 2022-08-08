from enum import unique
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy import UniqueConstraint

from app.db.session import Base


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


class GeoStatistics(Base):
    __tablename__ = "geo_statistics"

    id = sa.Column(sa.SmallInteger(), primary_key=True)
    name = sa.Column(sa.Text(), unique=True)
    geography_id = sa.Column(sa.Integer(), sa.ForeignKey("geography.id"), nullable=False)
    legislative_process = sa.Column(sa.Text(), nullable=False)
    federal = sa.Column(sa.Boolean(), nullable=False)
    federal_details = sa.Column(sa.Text(), nullable=False)
    political_groups = sa.Column(sa.Text(), nullable=False)
    global_emissions_percent = sa.Column(sa.Float(), nullable=True)
    climate_risk_index = sa.Column(sa.Float(), nullable=True)
    worldbank_income_group = sa.Column(sa.Text(), nullable=False)
    visibility_status = sa.Column(sa.Text(), nullable=False)
