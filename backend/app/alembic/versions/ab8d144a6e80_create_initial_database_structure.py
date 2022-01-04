"""Create initial database structure

Revision ID: ab8d144a6e80
Revises: 91979b40eb38
Create Date: 2021-12-16 10:00:46.986445-08:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "ab8d144a6e80"
down_revision = "91979b40eb38"
branch_labels = None
depends_on = None


def downgrade():
    op.drop_table("action_source_metadata")
    op.drop_table("action_type")
    op.drop_table("metadata_type")
    op.drop_table("geography")
    op.drop_table("action")
    op.drop_table("action_metadata")
    op.drop_table("language")
    op.drop_table("document")
    op.drop_table("source")
    op.drop_table("metadata_value")
    op.drop_table("passage")
    op.drop_table("metadata_value_keywords")
    op.drop_table("passage_metadata")
    op.drop_table("passage_type")


def upgrade():
    op.create_table(
        "passage_type",
        sa.Column(
            "passage_type_id",
            sa.INTEGER(),
            server_default=sa.text(
                "nextval('passage_type_passage_type_id_seq'::regclass)"
            ),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("name", sa.VARCHAR(length=255), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint(
            "passage_type_id", name="pk_passage_type_passage_type_id"
        ),
        postgresql_ignore_search_path=False,
    )

    # Create metadata lookup tables

    op.create_table(
        "metadata_type",
        sa.Column(
            "metadata_type_id",
            sa.INTEGER(),
            server_default=sa.text(
                "nextval('metadata_type_metadata_type_id_seq'::regclass)"
            ),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "type_name", sa.VARCHAR(length=128), autoincrement=False, nullable=False
        ),
        sa.Column(
            "type_description",
            sa.VARCHAR(length=2048),
            autoincrement=False,
            nullable=True,
        ),
        sa.PrimaryKeyConstraint(
            "metadata_type_id", name="pk_metadata_type_metadata_type_id"
        ),
        postgresql_ignore_search_path=False,
    )
    op.create_table(
        "metadata_value",
        sa.Column(
            "metadata_value_id",
            sa.INTEGER(),
            server_default=sa.text(
                "nextval('metadata_value_metadata_value_id_seq'::regclass)"
            ),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "metadata_type_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "value_name", sa.VARCHAR(length=255), autoincrement=False, nullable=False
        ),
        sa.Column(
            "value_description",
            sa.VARCHAR(length=2048),
            autoincrement=False,
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["metadata_type_id"],
            ["metadata_type.metadata_type_id"],
            name="fk_metadata_type",
        ),
        sa.PrimaryKeyConstraint(
            "metadata_value_id", name="pk_metadata_value_metadata_value_id"
        ),
        postgresql_ignore_search_path=False,
    )
    op.create_table(
        "metadata_value_keywords",
        sa.Column(
            "metadata_keyword_id", sa.INTEGER(), autoincrement=True, nullable=False
        ),
        sa.Column(
            "metadata_value_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "keyword", sa.VARCHAR(length=255), autoincrement=False, nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["metadata_value_id"],
            ["metadata_value.metadata_value_id"],
            name="fk_metadata_value",
        ),
        sa.PrimaryKeyConstraint(
            "metadata_keyword_id", name="pk_metadata_value_keywords_metadata_keyword_id"
        ),
    )

    # Create language lookup table

    op.create_table(
        "language",
        sa.Column(
            "language_code", sa.CHAR(length=3), autoincrement=False, nullable=False
        ),
        sa.Column("part1_code", sa.CHAR(length=2), autoincrement=False, nullable=False),
        sa.Column("part2_code", sa.CHAR(length=3), autoincrement=False, nullable=False),
        sa.Column("name", sa.VARCHAR(length=128), autoincrement=False, nullable=True),
        sa.Column("language_id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("language_id", name="pk_language_language_id"),
    )

    # Create geography lookup table

    op.create_table(
        "geography",
        sa.Column(
            "country_code", sa.CHAR(length=3), autoincrement=False, nullable=False
        ),
        sa.Column(
            "english_shortname",
            sa.VARCHAR(length=128),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "french_shortname",
            sa.VARCHAR(length=128),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "geography_id",
            sa.INTEGER(),
            server_default=sa.text("nextval('geography_geography_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("geography_id", name="pk_geography_country_id"),
        postgresql_ignore_search_path=False,
    )

    # Create source lookup table

    op.create_table(
        "source",
        sa.Column(
            "source_id",
            sa.INTEGER(),
            server_default=sa.text("nextval('source_source_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("name", sa.CHAR(length=1024), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("source_id", name="source_pkey"),
        postgresql_ignore_search_path=False,
    )

    # Create action type lookup table

    op.create_table(
        "action_type",
        sa.Column(
            "action_type_id",
            sa.INTEGER(),
            server_default=sa.text(
                "nextval('action_type_action_type_id_seq'::regclass)"
            ),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "action_parent_type_id", sa.INTEGER(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "type_name", sa.VARCHAR(length=255), autoincrement=False, nullable=False
        ),
        sa.Column(
            "type_description",
            sa.VARCHAR(length=2048),
            autoincrement=False,
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("action_type_id", name="action_type_pkey"),
        postgresql_ignore_search_path=False,
    )

    # Create action table

    op.create_table(
        "action",
        sa.Column(
            "action_id",
            sa.INTEGER(),
            server_default=sa.text("nextval('action_action_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "action_source_json",
            postgresql.JSONB(astext_type=sa.Text()),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("name", sa.VARCHAR(length=255), autoincrement=False, nullable=False),
        sa.Column(
            "description", sa.VARCHAR(length=2048), autoincrement=False, nullable=True
        ),
        sa.Column("action_date", sa.DATE(), autoincrement=False, nullable=False),
        sa.Column("geography_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("action_type_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "action_mod_date",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "action_source_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["action_source_id"], ["source.source_id"], name="fk_source"
        ),
        sa.ForeignKeyConstraint(
            ["action_type_id"], ["action_type.action_type_id"], name="fk_action_type"
        ),
        sa.ForeignKeyConstraint(
            ["geography_id"], ["geography.geography_id"], name="fk_geography"
        ),
        sa.PrimaryKeyConstraint("action_id", name="pk_action_action_id"),
        postgresql_ignore_search_path=False,
    )

    # Create action metadata link table

    op.create_table(
        "action_metadata",
        sa.Column("action_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "action_metadata_id", sa.INTEGER(), autoincrement=True, nullable=False
        ),
        sa.Column(
            "metadata_value_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.ForeignKeyConstraint(["action_id"], ["action.action_id"], name="fk_action"),
        sa.ForeignKeyConstraint(
            ["metadata_value_id"],
            ["metadata_value.metadata_value_id"],
            name="fk_metadata_value",
        ),
        sa.PrimaryKeyConstraint(
            "action_metadata_id", name="pk_action_metadata_action_metadata_id"
        ),
    )

    # Create action source metadata table

    op.create_table(
        "action_source_metadata",
        sa.Column(
            "action_source_metadata_id",
            sa.INTEGER(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "metadata_type_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "value", sa.VARCHAR(length=1024), autoincrement=False, nullable=False
        ),
        sa.Column("action_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(["action_id"], ["action.action_id"], name="fk_action"),
        sa.ForeignKeyConstraint(
            ["metadata_type_id"],
            ["metadata_type.metadata_type_id"],
            name="fk_metadata_type",
        ),
        sa.PrimaryKeyConstraint(
            "action_source_metadata_id",
            name="pk_action_source_metadata_action_source_metadata_id",
        ),
    )

    # Create document table

    op.create_table(
        "document",
        sa.Column("document_id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("action_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "document_date", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.Column("name", sa.VARCHAR(length=255), autoincrement=False, nullable=False),
        sa.Column(
            "source_url", sa.VARCHAR(length=1024), autoincrement=False, nullable=True
        ),
        sa.Column(
            "s3_url", sa.VARCHAR(length=1024), autoincrement=False, nullable=True
        ),
        sa.Column("language_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column(
            "document_mod_date",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["action_id"], ["action.action_id"], name="fk_action_type"
        ),
        sa.ForeignKeyConstraint(
            ["language_id"], ["language.language_id"], name="fk_language"
        ),
        sa.PrimaryKeyConstraint("document_id", name="pk_document_document_id"),
    )

    # Create passage table

    op.create_table(
        "passage",
        sa.Column("passage_id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("document_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("page_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("passage_type_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "parent_passage_id", sa.INTEGER(), autoincrement=False, nullable=True
        ),
        sa.Column("language_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("text", sa.TEXT(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["document_id"], ["document.document_id"], name="fk_document"
        ),
        sa.ForeignKeyConstraint(
            ["language_id"], ["language.language_id"], name="fk_language"
        ),
        sa.ForeignKeyConstraint(
            ["passage_type_id"],
            ["passage_type.passage_type_id"],
            name="fk_passage_type",
        ),
        sa.PrimaryKeyConstraint("passage_id", name="pk_passage_passage_id"),
    )

    # Create passage metadata table

    op.create_table(
        "passage_metadata",
        sa.Column("passage_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "metadata_value_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column("span_start_pos", sa.SMALLINT(), autoincrement=False, nullable=True),
        sa.Column("span_end_pos", sa.SMALLINT(), autoincrement=False, nullable=True),
        sa.Column("source", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("confidence", sa.REAL(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["metadata_value_id"],
            ["metadata_value.metadata_value_id"],
            name="fk_metadata_value",
        ),
        sa.ForeignKeyConstraint(
            ["passage_id"], ["passage.passage_id"], name="fk_passage"
        ),
        sa.PrimaryKeyConstraint(
            "passage_id",
            "metadata_value_id",
            name="pk_passage_metadata_passage_id_metadata_value_id",
        ),
    )
