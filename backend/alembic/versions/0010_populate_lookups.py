"""change category from multi to single relationship

Revision ID: 0010
Revises: 0009
Create Date: 2022-05-03 09:58:39.936352

"""
from alembic import op
from sqlalchemy import String, SmallInteger, Integer
from sqlalchemy.sql import table, column, TableClause


# revision identifiers, used by Alembic.
revision = "0010"
down_revision = "0009"
branch_labels = None
depends_on = None

category_tbl: TableClause = table(
    "category",
    column("id", SmallInteger),
    column("name", String),
    column("description", String),
)

document_type_tbl: TableClause = table(
    "document_type",
    column("id", SmallInteger),
    column("name", String),
    column("description", String),
)

response_tbl: TableClause = table(
    "response",
    column("id", Integer),
    column("name", String),
    column("description", String),
)

sector_tbl: TableClause = table(
    "sector",
    column("id", Integer),
    column("parent_id", Integer),
    column("name", String),
    column("description", String),
    column("source_id", Integer),
)

instrument_tbl: TableClause = table(
    "instrument",
    column("id", Integer),
    column("parent_id", Integer),
    column("name", String),
    column("description", String),
    column("source_id", Integer),
)


def upgrade():
    # add data for the category lookup
    for category in ["Law", "Policy"]:
        op.execute(
            category_tbl.insert().values(
                name=category,
                description=category,
            )
        )

    # add data for the document type lookup

    # first, remove the incorrect data put there by 0002
    op.execute(document_type_tbl.delete())

    for document_type in [
        "Accord",
        "Act",
        "Action Plan",
        "Agenda",
        "Constitution",
        "Decision",
        "Decree",
        "Decree Law",
        "Directive",
        "Discussion Paper",
        "Edict",
        "EU Decision",
        "EU Directive",
        "EU Regulation",
        "Framework",
        "Law",
        "Law and plan",
        "Order",
        "Ordinance",
        "Plan",
        "Policy",
        "Programme",
        "Roadmap",
        "Regulation",
        "Resolution",
        "Royal Decree",
        "Rules",
        "Strategic Assessment",
        "Strategy",
        "Vision",
    ]:
        op.execute(
            document_type_tbl.insert().values(
                name=document_type,
                description=document_type,
            )
        )

    # add topics
    for topic in [
        "Mitigation",
        "Adaptation",
        "Loss & Damage",
        "Disaster Risk Management(DRM)",
    ]:
        op.execute(
            response_tbl.insert().values(
                name=topic,
                description=topic,
            )
        )

    # add sectors
    for sector in [
        "Adaptation",
        "Agriculture",
        "Buildings",
        "Coastal zones",
        "Cross cutting areas",
        "Disaster risk management (DRM)",
        "Economy-wide",
        "Energy",
        "Environment",
        "Finance",
        "Health",
        "Industry",
        "LULUCF",
        "Public sector",
        "Rural",
        "Social development",
        "Tourism",
        "Transport",
        "Transportation",
        "Urban",
        "Waste",
        "Water",
        "Other",
    ]:
        op.execute(
            sector_tbl.insert().values(
                name=sector,
                description=sector,
                source_id=1,
            )
        )

    # add instruments
    instruments_dict = {}
    for instrument in [
        ["Direct investment", "Early warning systems"],
        ["Direct investment", "Green procurement"],
        ["Direct investment", "Nature based solutions and ecosystem restoration"],
        ["Direct investment", "Other"],
        ["Direct investment", "Provision of climate funds"],
        ["Economic", "Carbon pricing and emissions trading"],
        ["Economic", "Climate finance tools"],
        ["Economic", "Insurance"],
        ["Economic", "Subsidies"],
        ["Economic", "Tax incentives"],
        ["Economic", "Other"],
        ["Governance", "Capacity building"],
        ["Governance", "Institutional mandates"],
        ["Governance", "International cooperation"],
        ["Governance", "MRV"],
        ["Governance", "Other"],
        ["Governance", "Planning"],
        ["Governance", "Processes, plans and strategies"],
        ["Governance", "Subnational and citizen participation"],
        ["Information", "Education, training and knowledge dissemination"],
        ["Information", "Research and development, knowledge generation"],
        ["Regulation", "Disclosure obligations"],
        ["Regulation", "Moratoria and bans"],
        ["Regulation", "Other"],
        ["Regulation", "Standards, obligations and norms"],
        ["Regulation", "Zoning and spatial planning"],
    ]:
        parent_instrument = instrument[0]
        child_instrument = instrument[1]
        if parent_instrument not in instruments_dict:
            instruments_dict[parent_instrument] = [child_instrument]
        else:
            instruments_dict[parent_instrument].append(child_instrument)

    for parent, children in instruments_dict.items():
        op.execute(
            instrument_tbl.insert().values(
                name=parent,
                description=parent,
                source_id=1,
            )
        )

        parent_id = (
            instrument_tbl.select()
            .with_only_columns(instrument_tbl.columns["id"])
            .where(instrument_tbl.columns["name"] == parent)
            .scalar_subquery()
        )

        for child in children:
            op.execute(
                instrument_tbl.insert().values(
                    name=child,
                    description=child,
                    source_id=1,
                    parent_id=parent_id,
                )
            )


def downgrade():
    op.execute(instrument_tbl.delete())
    op.execute(sector_tbl.delete())
    op.execute(response_tbl.delete())
    op.execute(document_type_tbl.delete())
    op.execute(category_tbl.delete())
