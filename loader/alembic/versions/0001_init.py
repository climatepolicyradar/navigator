"""init

Revision ID: 0001
Revises:
Create Date: 2022-04-06 12:59:44.456122

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "document_type",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_document_type")),
    )
    op.create_table(
        "framework",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_framework")),
    )
    op.create_table(
        "geography",
        sa.Column("id", sa.SmallInteger(), nullable=False),
        sa.Column("display_value", sa.Text(), nullable=True),
        sa.Column("value", sa.Text(), nullable=True),
        sa.Column("type", sa.Text(), nullable=True),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["geography.id"],
            name=op.f("fk_geography__parent_id__geography"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_geography")),
        sa.UniqueConstraint("display_value", name=op.f("uq_geography__display_value")),
    )
    op.create_table(
        "hazard",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_hazard")),
    )
    op.create_table(
        "language",
        sa.Column("id", sa.SmallInteger(), nullable=False),
        sa.Column("language_code", sa.CHAR(length=3), nullable=False),
        sa.Column("part1_code", sa.CHAR(length=2), nullable=True),
        sa.Column("part2_code", sa.CHAR(length=3), nullable=True),
        sa.Column("name", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_language")),
    )
    op.create_table(
        "passage_type",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_passage_type")),
    )
    op.create_table(
        "response",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_response")),
    )
    op.create_table(
        "source",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_source")),
    )
    op.create_table(
        "document",
        sa.Column(
            "created_ts",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_ts", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "loaded_ts",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("source_url", sa.Text(), nullable=True),
        sa.Column("source_id", sa.Integer(), nullable=False),
        sa.Column("url", sa.Text(), nullable=True),
        sa.Column("is_valid", sa.Boolean(), nullable=False),
        sa.Column(
            "invalid_reason",
            sa.Enum(
                "unsupported_content_type",
                "net_ssl_error",
                "net_read_error",
                "net_connection_error",
                "net_too_many_redirects",
                "net_remote_protocol_error",
                name="documentinvalidreason",
            ),
            nullable=True,
        ),
        sa.Column("geography_id", sa.SmallInteger(), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["geography_id"],
            ["geography.id"],
            name=op.f("fk_document__geography_id__geography"),
        ),
        sa.ForeignKeyConstraint(
            ["source_id"], ["source.id"], name=op.f("fk_document__source_id__source")
        ),
        sa.ForeignKeyConstraint(
            ["type_id"],
            ["document_type.id"],
            name=op.f("fk_document__type_id__document_type"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_document")),
    )
    op.create_table(
        "instrument",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("source_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["instrument.id"],
            name=op.f("fk_instrument__parent_id__instrument"),
        ),
        sa.ForeignKeyConstraint(
            ["source_id"], ["source.id"], name=op.f("fk_instrument__source_id__source")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_instrument")),
    )
    op.create_table(
        "sector",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("source_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["parent_id"], ["sector.id"], name=op.f("fk_sector__parent_id__sector")
        ),
        sa.ForeignKeyConstraint(
            ["source_id"], ["source.id"], name=op.f("fk_sector__source_id__source")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_sector")),
    )
    op.create_table(
        "association",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("document_id_from", sa.Integer(), nullable=False),
        sa.Column("document_id_to", sa.Integer(), nullable=False),
        sa.Column("type", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["document_id_from"],
            ["document.id"],
            name=op.f("fk_association__document_id_from__document"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["document_id_to"],
            ["document.id"],
            name=op.f("fk_association__document_id_to__document"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_association")),
    )
    op.create_table(
        "document_framework",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("framework_id", sa.Integer(), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["document_id"],
            ["document.id"],
            name=op.f("fk_document_framework__document_id__document"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["framework_id"],
            ["framework.id"],
            name=op.f("fk_document_framework__framework_id__framework"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_document_framework")),
    )
    op.create_table(
        "document_hazard",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hazard_id", sa.Integer(), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["document_id"],
            ["document.id"],
            name=op.f("fk_document_hazard__document_id__document"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["hazard_id"],
            ["hazard.id"],
            name=op.f("fk_document_hazard__hazard_id__hazard"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_document_hazard")),
    )
    op.create_table(
        "document_instrument",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("instrument_id", sa.Integer(), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["document_id"],
            ["document.id"],
            name=op.f("fk_document_instrument__document_id__document"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["instrument_id"],
            ["instrument.id"],
            name=op.f("fk_document_instrument__instrument_id__instrument"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_document_instrument")),
    )
    op.create_table(
        "document_response",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("response_id", sa.Integer(), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["document_id"],
            ["document.id"],
            name=op.f("fk_document_response__document_id__document"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["response_id"],
            ["response.id"],
            name=op.f("fk_document_response__response_id__response"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_document_response")),
    )
    op.create_table(
        "document_sector",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sector_id", sa.Integer(), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["document_id"],
            ["document.id"],
            name=op.f("fk_document_sector__document_id__document"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["sector_id"],
            ["sector.id"],
            name=op.f("fk_document_sector__sector_id__sector"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_document_sector")),
    )
    op.create_table(
        "event",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column(
            "created_ts",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["document_id"],
            ["document.id"],
            name=op.f("fk_event__document_id__document"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_event")),
    )
    op.create_table(
        "passage",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.Column("page_id", sa.BigInteger(), autoincrement=False, nullable=False),
        sa.Column("passage_type_id", sa.Integer(), nullable=False),
        sa.Column("parent_passage_id", sa.Integer(), nullable=True),
        sa.Column("language_id", sa.SmallInteger(), nullable=True),
        sa.Column("text", sa.TEXT(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["document_id"],
            ["document.id"],
            name=op.f("fk_passage__document_id__document"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["language_id"],
            ["language.id"],
            name=op.f("fk_passage__language_id__language"),
        ),
        sa.ForeignKeyConstraint(
            ["parent_passage_id"],
            ["passage.id"],
            name=op.f("fk_passage__parent_passage_id__passage"),
        ),
        sa.ForeignKeyConstraint(
            ["passage_type_id"],
            ["passage_type.id"],
            name=op.f("fk_passage__passage_type_id__passage_type"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_passage")),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("passage")
    op.drop_table("event")
    op.drop_table("document_sector")
    op.drop_table("document_response")
    op.drop_table("document_instrument")
    op.drop_table("document_hazard")
    op.drop_table("document_framework")
    op.drop_table("association")
    op.drop_table("sector")
    op.drop_table("instrument")
    op.drop_table("document")
    op.drop_table("source")
    op.drop_table("response")
    op.drop_table("passage_type")
    op.drop_table("language")
    op.drop_table("hazard")
    op.drop_table("geography")
    op.drop_table("framework")
    op.drop_table("document_type")
    # ### end Alembic commands ###
