"""remove superfluous lookup tables

Revision ID: 0007
Revises: 0006
Create Date: 2022-04-27 17:15:19.112319

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0007"
down_revision = "0006"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "document_language",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("language_id", sa.Integer(), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["document_id"],
            ["document.id"],
            name=op.f("fk_document_language__document_id__document"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_document_language")),
    )
    op.drop_constraint(
        "fk_document__type_id__document_type", "document", type_="foreignkey"
    )
    op.drop_constraint("fk_document__source_id__source", "document", type_="foreignkey")
    op.drop_constraint(
        "fk_document__geography_id__geography", "document", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_instrument__source_id__source", "instrument", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_passage__language_id__language", "passage", type_="foreignkey"
    )
    op.drop_constraint("fk_sector__source_id__source", "sector", type_="foreignkey")
    op.drop_table("geography")
    op.drop_table("language")
    op.drop_table("document_type")
    op.drop_table("source")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "source",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("name", sa.VARCHAR(length=128), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_source"),
    )
    op.create_table(
        "document_type",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("name", sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column("description", sa.TEXT(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_document_type"),
    )
    op.create_table(
        "language",
        sa.Column(
            "id",
            sa.SMALLINT(),
            server_default=sa.text("nextval('language_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "language_code", sa.CHAR(length=3), autoincrement=False, nullable=False
        ),
        sa.Column("part1_code", sa.CHAR(length=2), autoincrement=False, nullable=True),
        sa.Column("part2_code", sa.CHAR(length=3), autoincrement=False, nullable=True),
        sa.Column("name", sa.TEXT(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="pk_language"),
        sa.UniqueConstraint("language_code", name="uq_language__language_code"),
    )
    op.create_table(
        "geography",
        sa.Column(
            "id",
            sa.SMALLINT(),
            server_default=sa.text("nextval('geography_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("display_value", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column("value", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column("type", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column("parent_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["parent_id"], ["geography.id"], name="fk_geography__parent_id__geography"
        ),
        sa.PrimaryKeyConstraint("id", name="pk_geography"),
        sa.UniqueConstraint("display_value", name="uq_geography__display_value"),
    )
    op.drop_table("document_language")
    op.create_foreign_key(
        "fk_sector__source_id__source", "sector", "source", ["source_id"], ["id"]
    )
    op.create_foreign_key(
        "fk_passage__language_id__language",
        "passage",
        "language",
        ["language_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_instrument__source_id__source",
        "instrument",
        "source",
        ["source_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_document__geography_id__geography",
        "document",
        "geography",
        ["geography_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_document__source_id__source", "document", "source", ["source_id"], ["id"]
    )
    op.create_foreign_key(
        "fk_document__type_id__document_type",
        "document",
        "document_type",
        ["type_id"],
        ["id"],
    )
    # ### end Alembic commands ###
