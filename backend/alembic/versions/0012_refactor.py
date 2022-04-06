"""refactor

Revision ID: 0012
Revises: 0011
Create Date: 2022-04-06 10:16:29.258415

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0012"
down_revision = "0011"
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
        "hazard",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_hazard")),
    )
    op.create_table(
        "response",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_response")),
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
        ),
        sa.ForeignKeyConstraint(
            ["document_id_to"],
            ["document.id"],
            name=op.f("fk_association__document_id_to__document"),
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
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_event")),
    )
    op.drop_table("metadata_value_keywords")
    op.drop_table("metadata_value")
    op.drop_table("action_type")
    op.drop_table("metadata_type")
    op.drop_table("passage_metadata")
    op.drop_table("action_source_metadata")
    op.drop_table("action_metadata")
    op.drop_table("action")
    op.add_column(
        "document",
        sa.Column(
            "created_ts",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )
    op.add_column(
        "document", sa.Column("updated_ts", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column("document", sa.Column("id", sa.Integer(), nullable=False))
    op.add_column("document", sa.Column("created_by", sa.Integer(), nullable=True))
    op.add_column("document", sa.Column("updated_by", sa.Integer(), nullable=True))
    op.add_column(
        "document", sa.Column("loaded_ts", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column("document", sa.Column("source_id", sa.Integer(), nullable=False))
    op.add_column("document", sa.Column("url", sa.Text(), nullable=True))
    op.add_column(
        "document", sa.Column("geography_id", sa.SmallInteger(), nullable=False)
    )
    op.add_column("document", sa.Column("type_id", sa.Integer(), nullable=False))
    op.drop_constraint("fk_document__action_id__action", "document", type_="foreignkey")
    op.drop_constraint(
        "fk_document__language_id__language", "document", type_="foreignkey"
    )
    op.create_foreign_key(
        op.f("fk_document__type_id__document_type"),
        "document",
        "document_type",
        ["type_id"],
        ["id"],
    )
    op.create_foreign_key(
        op.f("fk_document__source_id__source"),
        "document",
        "source",
        ["source_id"],
        ["id"],
    )
    op.create_foreign_key(
        op.f("fk_document__created_by__user"),
        "document",
        "user",
        ["created_by"],
        ["id"],
    )
    op.create_foreign_key(
        op.f("fk_document__geography_id__geography"),
        "document",
        "geography",
        ["geography_id"],
        ["id"],
    )
    op.create_foreign_key(
        op.f("fk_document__updated_by__user"),
        "document",
        "user",
        ["updated_by"],
        ["id"],
    )
    op.drop_column("document", "s3_url")
    op.drop_column("document", "document_date")
    op.drop_column("document", "language_id")
    op.drop_column("document", "document_mod_date")
    op.drop_column("document", "document_id")
    op.drop_column("document", "action_id")
    op.drop_column("document", "is_valid")
    op.drop_column("document", "invalid_reason")
    op.add_column("geography", sa.Column("id", sa.SmallInteger(), nullable=False))
    op.add_column("geography", sa.Column("value", sa.Text(), nullable=True))
    op.add_column("geography", sa.Column("official_value", sa.Text(), nullable=True))
    op.add_column("geography", sa.Column("type", sa.Text(), nullable=True))
    op.add_column("geography", sa.Column("parent_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        op.f("fk_geography__parent_id__geography"),
        "geography",
        "geography",
        ["parent_id"],
        ["id"],
    )
    op.drop_column("geography", "english_shortname")
    op.drop_column("geography", "country_code")
    op.drop_column("geography", "french_shortname")
    op.drop_column("geography", "geography_id")
    op.add_column("language", sa.Column("id", sa.SmallInteger(), nullable=False))
    op.drop_column("language", "language_id")
    op.add_column("passage", sa.Column("id", sa.BigInteger(), nullable=False))
    op.drop_constraint(
        "fk_passage__document_id__document", "passage", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_passage__language_id__language", "passage", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_passage__passage_type_id__passage_type", "passage", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_passage__parent_passage_id__passage", "passage", type_="foreignkey"
    )
    op.create_foreign_key(
        op.f("fk_passage__passage_type_id__passage_type"),
        "passage",
        "passage_type",
        ["passage_type_id"],
        ["id"],
    )
    op.create_foreign_key(
        op.f("fk_passage__document_id__document"),
        "passage",
        "document",
        ["document_id"],
        ["id"],
    )
    op.create_foreign_key(
        op.f("fk_passage__parent_passage_id__passage"),
        "passage",
        "passage",
        ["parent_passage_id"],
        ["id"],
    )
    op.create_foreign_key(
        op.f("fk_passage__language_id__language"),
        "passage",
        "language",
        ["language_id"],
        ["id"],
    )
    op.drop_column("passage", "passage_id")
    op.add_column("passage_type", sa.Column("id", sa.Integer(), nullable=False))
    op.drop_column("passage_type", "passage_type_id")
    op.add_column("source", sa.Column("id", sa.Integer(), nullable=False))
    op.drop_column("source", "source_id")
    op.add_column(
        "user",
        sa.Column(
            "created_ts",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
    )
    op.add_column(
        "user", sa.Column("updated_ts", sa.DateTime(timezone=True), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "updated_ts")
    op.drop_column("user", "created_ts")
    op.add_column(
        "source",
        sa.Column(
            "source_id",
            sa.INTEGER(),
            server_default=sa.text("nextval('source_source_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
    )
    op.drop_column("source", "id")
    op.add_column(
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
    )
    op.drop_column("passage_type", "id")
    op.add_column(
        "passage",
        sa.Column("passage_id", sa.BIGINT(), autoincrement=True, nullable=False),
    )
    op.drop_constraint(
        op.f("fk_passage__language_id__language"), "passage", type_="foreignkey"
    )
    op.drop_constraint(
        op.f("fk_passage__parent_passage_id__passage"), "passage", type_="foreignkey"
    )
    op.drop_constraint(
        op.f("fk_passage__document_id__document"), "passage", type_="foreignkey"
    )
    op.drop_constraint(
        op.f("fk_passage__passage_type_id__passage_type"), "passage", type_="foreignkey"
    )
    op.create_foreign_key(
        "fk_passage__parent_passage_id__passage",
        "passage",
        "passage",
        ["parent_passage_id"],
        ["passage_id"],
    )
    op.create_foreign_key(
        "fk_passage__passage_type_id__passage_type",
        "passage",
        "passage_type",
        ["passage_type_id"],
        ["passage_type_id"],
    )
    op.create_foreign_key(
        "fk_passage__language_id__language",
        "passage",
        "language",
        ["language_id"],
        ["language_id"],
    )
    op.create_foreign_key(
        "fk_passage__document_id__document",
        "passage",
        "document",
        ["document_id"],
        ["document_id"],
    )
    op.drop_column("passage", "id")
    op.add_column(
        "language",
        sa.Column(
            "language_id",
            sa.SMALLINT(),
            server_default=sa.text("nextval('language_language_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
    )
    op.drop_column("language", "id")
    op.add_column(
        "geography",
        sa.Column(
            "geography_id",
            sa.SMALLINT(),
            server_default=sa.text("nextval('geography_geography_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
    )
    op.add_column(
        "geography",
        sa.Column(
            "french_shortname",
            sa.VARCHAR(length=128),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "geography",
        sa.Column(
            "country_code", sa.CHAR(length=3), autoincrement=False, nullable=False
        ),
    )
    op.add_column(
        "geography",
        sa.Column(
            "english_shortname",
            sa.VARCHAR(length=128),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_constraint(
        op.f("fk_geography__parent_id__geography"), "geography", type_="foreignkey"
    )
    op.drop_column("geography", "parent_id")
    op.drop_column("geography", "type")
    op.drop_column("geography", "official_value")
    op.drop_column("geography", "value")
    op.drop_column("geography", "id")
    op.add_column(
        "document",
        sa.Column(
            "invalid_reason",
            postgresql.ENUM(
                "unsupported_content_type",
                "net_ssl_error",
                "net_read_error",
                "net_connection_error",
                "net_too_many_redirects",
                name="documentinvalidreason",
            ),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "document",
        sa.Column("is_valid", sa.BOOLEAN(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "document",
        sa.Column("action_id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "document",
        sa.Column("document_id", sa.INTEGER(), autoincrement=True, nullable=False),
    )
    op.add_column(
        "document",
        sa.Column(
            "document_mod_date",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "document",
        sa.Column("language_id", sa.SMALLINT(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "document",
        sa.Column(
            "document_date", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
    )
    op.add_column(
        "document",
        sa.Column(
            "s3_url", sa.VARCHAR(length=1024), autoincrement=False, nullable=True
        ),
    )
    op.drop_constraint(
        op.f("fk_document__updated_by__user"), "document", type_="foreignkey"
    )
    op.drop_constraint(
        op.f("fk_document__geography_id__geography"), "document", type_="foreignkey"
    )
    op.drop_constraint(
        op.f("fk_document__created_by__user"), "document", type_="foreignkey"
    )
    op.drop_constraint(
        op.f("fk_document__source_id__source"), "document", type_="foreignkey"
    )
    op.drop_constraint(
        op.f("fk_document__type_id__document_type"), "document", type_="foreignkey"
    )
    op.create_foreign_key(
        "fk_document__language_id__language",
        "document",
        "language",
        ["language_id"],
        ["language_id"],
    )
    op.create_foreign_key(
        "fk_document__action_id__action",
        "document",
        "action",
        ["action_id"],
        ["action_id"],
    )
    op.drop_column("document", "type_id")
    op.drop_column("document", "geography_id")
    op.drop_column("document", "url")
    op.drop_column("document", "source_id")
    op.drop_column("document", "loaded_ts")
    op.drop_column("document", "updated_by")
    op.drop_column("document", "created_by")
    op.drop_column("document", "id")
    op.drop_column("document", "updated_ts")
    op.drop_column("document", "created_ts")
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
        sa.Column("name", sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column("description", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column("action_date", sa.DATE(), autoincrement=False, nullable=False),
        sa.Column("geography_id", sa.SMALLINT(), autoincrement=False, nullable=False),
        sa.Column("action_type_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "action_mod_date",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("action_source_id", sa.BIGINT(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["action_source_id"],
            ["source.source_id"],
            name="fk_action__action_source_id__source",
        ),
        sa.ForeignKeyConstraint(
            ["action_type_id"],
            ["action_type.action_type_id"],
            name="fk_action__action_type_id__action_type",
        ),
        sa.ForeignKeyConstraint(
            ["geography_id"],
            ["geography.geography_id"],
            name="fk_action__geography_id__geography",
        ),
        sa.PrimaryKeyConstraint("action_id", name="pk_action"),
        sa.UniqueConstraint(
            "name",
            "action_date",
            "geography_id",
            "action_type_id",
            "action_source_id",
            name="uq_action__name",
        ),
        postgresql_ignore_search_path=False,
    )
    op.create_table(
        "action_metadata",
        sa.Column("action_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "action_metadata_id", sa.INTEGER(), autoincrement=True, nullable=False
        ),
        sa.Column(
            "metadata_value_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["action_id"],
            ["action.action_id"],
            name="fk_action_metadata__action_id__action",
        ),
        sa.ForeignKeyConstraint(
            ["metadata_value_id"],
            ["metadata_value.metadata_value_id"],
            name="fk_action_metadata__metadata_value_id__metadata_value",
        ),
        sa.PrimaryKeyConstraint("action_metadata_id", name="pk_action_metadata"),
    )
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
        sa.ForeignKeyConstraint(
            ["action_id"],
            ["action.action_id"],
            name="fk_action_source_metadata__action_id__action",
        ),
        sa.ForeignKeyConstraint(
            ["metadata_type_id"],
            ["metadata_type.metadata_type_id"],
            name="fk_action_source_metadata__metadata_type_id__metadata_type",
        ),
        sa.PrimaryKeyConstraint(
            "action_source_metadata_id", name="pk_action_source_metadata"
        ),
    )
    op.create_table(
        "passage_metadata",
        sa.Column("passage_id", sa.BIGINT(), autoincrement=False, nullable=False),
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
            name="fk_passage_metadata__metadata_value_id__metadata_value",
        ),
        sa.ForeignKeyConstraint(
            ["source"], ["source.source_id"], name="fk_passage_metadata__source__source"
        ),
        sa.PrimaryKeyConstraint(
            "passage_id", "metadata_value_id", name="pk_passage_metadata"
        ),
    )
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
        sa.PrimaryKeyConstraint("metadata_type_id", name="pk_metadata_type"),
        postgresql_ignore_search_path=False,
    )
    op.create_table(
        "action_type",
        sa.Column("action_type_id", sa.INTEGER(), autoincrement=True, nullable=False),
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
        sa.PrimaryKeyConstraint("action_type_id", name="pk_action_type"),
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
            name="fk_metadata_value__metadata_type_id__metadata_type",
        ),
        sa.PrimaryKeyConstraint("metadata_value_id", name="pk_metadata_value"),
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
            name="fk_metadata_value_keywords__metadata_value_id__metadata_value",
        ),
        sa.PrimaryKeyConstraint(
            "metadata_keyword_id", name="pk_metadata_value_keywords"
        ),
    )
    op.drop_table("event")
    op.drop_table("document_sector")
    op.drop_table("document_response")
    op.drop_table("document_instrument")
    op.drop_table("document_hazard")
    op.drop_table("document_framework")
    op.drop_table("association")
    op.drop_table("sector")
    op.drop_table("instrument")
    op.drop_table("response")
    op.drop_table("hazard")
    op.drop_table("framework")
    op.drop_table("document_type")
    # ### end Alembic commands ###
