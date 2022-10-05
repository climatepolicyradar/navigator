"""litigation

Revision ID: 0006
Revises: 0005
Create Date: 2022-10-05 17:15:03.956379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "lit_body",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_lit_body")),
        sa.UniqueConstraint("name", name=op.f("uq_lit_body__name")),
    )
    op.create_table(
        "lit_external_law",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("url", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_lit_external_law")),
    )
    op.create_table(
        "lit_party",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column(
            "party_type",
            sa.Enum(
                "GOVERNMENT",
                "SUBNATIONAL_GOVERNMENT",
                "INDIVIDUAL",
                "INDIVIDUAL_SUPPORTED_BY_NGO",
                "NGO",
                "CORPORATION",
                "CORPORATION_SUPPORTED_BY_NGO",
                "INDIGENOUS_GOVERNMENT_TRIBAL",
                "TRADE_ASSOCIATION",
                "SUPRANATIONAL_LEGAL_BODY",
                "INDIVIDUAL_REPRESENTING_CORPORATION",
                "NA",
                name="litpartytype",
            ),
            nullable=True,
        ),
        sa.Column(
            "side_type",
            sa.Enum(
                "FILING_PARTY", "RESPONDING_PARTY", "INTERVENOR", name="litsidetype"
            ),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_lit_party")),
        sa.UniqueConstraint("name", name=op.f("uq_lit_party__name")),
    )
    op.create_table(
        "lit_case",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "OPEN",
                "OPEN_APPEAL",
                "CLOSED_SETTLED",
                "CLOSED_WITHDRAWN",
                "CLOSED",
                name="casestatus",
            ),
            nullable=True,
        ),
        sa.Column(
            "outcome",
            sa.Enum(
                "ENHANCED_CLIMATE_ACTION",
                "NEUTRAL",
                "HINDERED_CLIMATE_ACTION",
                "NA",
                name="caseoutcome",
            ),
            nullable=True,
        ),
        sa.Column("objective", sa.Text(), nullable=True),
        sa.Column(
            "pillars",
            sa.Enum(
                "ADAPTATION_RESILIENCE",
                "MITIGATION",
                "LOSS_DAMAGE",
                name="unfcccpillars",
            ),
            nullable=True,
        ),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("reference", sa.Text(), nullable=True),
        sa.Column("case_class", sa.Text(), nullable=True),
        sa.Column("strategic", sa.Boolean(), nullable=True),
        sa.Column(
            "alignment_class",
            sa.Enum(
                "CLIMATE_ALIGNED",
                "CLIMATE_NON_ALIGNED",
                "JUST_TRANSITION",
                name="climatealignmentclass",
            ),
            nullable=True,
        ),
        sa.Column(
            "strategic_class",
            sa.Enum(
                "ENFORCING_CLIMATE_STANDARDS",
                "GOVERNMENT_FRAMEWORK",
                "PUBLIC_FINANCE",
                "FAILURE_TO_ADAPT",
                "COMPENSATION",
                "CLIMATE_WASHING",
                "PERSONAL_RESPONSIBILITY",
                "REGULATORY_POWERS",
                "SLAPP",
                "JUST_TRANSITION",
                "CORPORATE_FRAMEWORK",
                "OTHER",
                "NA",
                name="strategicalignmentclass",
            ),
            nullable=True,
        ),
        sa.Column("source", sa.Text(), nullable=True),
        sa.Column("body_id", sa.Integer(), nullable=True),
        sa.Column("sector_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["body_id"], ["lit_body.id"], name=op.f("fk_lit_case__body_id__lit_body")
        ),
        sa.ForeignKeyConstraint(
            ["sector_id"], ["sector.id"], name=op.f("fk_lit_case__sector_id__sector")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_lit_case")),
        sa.UniqueConstraint("name", name=op.f("uq_lit_case__name")),
    )
    op.create_table(
        "lit_case_ext_laws",
        sa.Column("extlaw_id", sa.Integer(), nullable=False),
        sa.Column("case_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["case_id"],
            ["lit_case.id"],
            name=op.f("fk_lit_case_ext_laws__case_id__lit_case"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["extlaw_id"],
            ["lit_external_law.id"],
            name=op.f("fk_lit_case_ext_laws__extlaw_id__lit_external_law"),
        ),
        sa.PrimaryKeyConstraint(
            "extlaw_id", "case_id", name=op.f("pk_lit_case_ext_laws")
        ),
    )
    op.create_table(
        "lit_case_int_laws",
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.Column("case_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["case_id"],
            ["lit_case.id"],
            name=op.f("fk_lit_case_int_laws__case_id__lit_case"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["document_id"],
            ["document.id"],
            name=op.f("fk_lit_case_int_laws__document_id__document"),
        ),
        sa.PrimaryKeyConstraint(
            "document_id", "case_id", name=op.f("pk_lit_case_int_laws")
        ),
    )
    op.create_table(
        "lit_case_keyword",
        sa.Column("keyword_id", sa.Integer(), nullable=False),
        sa.Column("case_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["case_id"],
            ["lit_case.id"],
            name=op.f("fk_lit_case_keyword__case_id__lit_case"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["keyword_id"],
            ["keyword.id"],
            name=op.f("fk_lit_case_keyword__keyword_id__keyword"),
        ),
        sa.PrimaryKeyConstraint(
            "keyword_id", "case_id", name=op.f("pk_lit_case_keyword")
        ),
    )
    op.create_table(
        "lit_case_parties",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("case_id", sa.Integer(), nullable=True),
        sa.Column("party_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["case_id"],
            ["lit_case.id"],
            name=op.f("fk_lit_case_parties__case_id__lit_case"),
        ),
        sa.ForeignKeyConstraint(
            ["party_id"],
            ["lit_party.id"],
            name=op.f("fk_lit_case_parties__party_id__lit_party"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_lit_case_parties")),
    )
    op.create_table(
        "lit_document",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("case_id", sa.Integer(), nullable=True),
        sa.Column("language", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["case_id"],
            ["lit_case.id"],
            name=op.f("fk_lit_document__case_id__lit_case"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_lit_document")),
    )
    op.create_table(
        "lit_event",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "type",
            sa.Enum(
                "FILING",
                "CLAIMANT_DOCUMENT_OTHER",
                "DEFENDANT_DOCUMENT",
                "DECISION",
                "INTERIM_DECISION",
                "INTERVENOR_DOCUMENT",
                "HEARING",
                "SETTLEMENT",
                "WITHDRAWAL",
                "OTHER",
                "APPEAL",
                "PRE_ACTION_EVENT",
                name="liteventtype",
            ),
            nullable=True,
        ),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("case_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["case_id"], ["lit_case.id"], name=op.f("fk_lit_event__case_id__lit_case")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_lit_event")),
    )
    op.create_table(
        "lit_event_documents",
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["document_id"],
            ["lit_document.id"],
            name=op.f("fk_lit_event_documents__document_id__lit_document"),
        ),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["lit_event.id"],
            name=op.f("fk_lit_event_documents__event_id__lit_event"),
        ),
        sa.PrimaryKeyConstraint(
            "event_id", "document_id", name=op.f("pk_lit_event_documents")
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("lit_event_documents")
    op.drop_table("lit_event")
    op.drop_table("lit_document")
    op.drop_table("lit_case_parties")
    op.drop_table("lit_case_keyword")
    op.drop_table("lit_case_int_laws")
    op.drop_table("lit_case_ext_laws")
    op.drop_table("lit_case")
    op.drop_table("lit_party")
    op.drop_table("lit_external_law")
    op.drop_table("lit_body")
    # ### end Alembic commands ###
