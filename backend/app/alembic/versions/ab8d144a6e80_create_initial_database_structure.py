"""Create initial database structure

Revision ID: ab8d144a6e80
Revises: 91979b40eb38
Create Date: 2021-12-16 10:00:46.986445-08:00

"""
from alembic import op
import sqlalchemy as sa

from app.db.session import Base
from app.db import models

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


def create_table(model: Base, *args):
    """Create a table from an Alembic declarative model and any extra arguments.

    Args:
        model (Base): Alembic declarative model, with the table name stored as property __tablename__,
        and columns stored as instances of sqlalchemy.Column keyed by the column name.
    """

    columns = []

    for k, v in model.__dict__:
        if not k.startswith("_") and isinstance(v, sa.Column):
            column = v
            column.name = k
            columns.append(column)

    op.create_table(
        model.__tablename__,
        *columns,
        *args,
    )


def upgrade():
    create_table(
        models.PassageType,
        postgresql_ignore_search_path=False,
    )

    # Create metadata lookup tables
    create_table(
        models.MetadataType,
        postgresql_ignore_search_path=False,
    )

    create_table(
        models.MetadataValue,
        sa.ForeignKeyConstraint(
            ["metadata_type_id"],
            ["metadata_type.metadata_type_id"],
            name="fk_metadata_type",
        ),
        postgresql_ignore_search_path=False,
    )

    create_table(
        models.MetadataValueKeywords,
        sa.ForeignKeyConstraint(
            ["metadata_value_id"],
            ["metadata_value.metadata_value_id"],
            name="fk_metadata_value",
        ),
    )

    # Create language lookup table
    create_table(
        models.Language,
    )

    # Create geography lookup table
    create_table(
        models.Geography,
        postgresql_ignore_search_path=False,
    )

    # Create source lookup table
    create_table(
        models.Source,
        postgresql_ignore_search_path=False,
    )

    # Create action type lookup table
    create_table(
        models.ActionType,
        postgresql_ignore_search_path=False,
    )

    # Create action table
    create_table(
        models.Action,
        sa.ForeignKeyConstraint(
            ["action_source_id"], ["source.source_id"], name="fk_source"
        ),
        sa.ForeignKeyConstraint(
            ["action_type_id"], ["action_type.action_type_id"], name="fk_action_type"
        ),
        sa.ForeignKeyConstraint(
            ["geography_id"], ["geography.geography_id"], name="fk_geography"
        ),
        postgresql_ignore_search_path=False,
    )

    # Create action metadata link table
    create_table(
        models.ActionMetadata,
        sa.ForeignKeyConstraint(["action_id"], ["action.action_id"], name="fk_action"),
        sa.ForeignKeyConstraint(
            ["metadata_value_id"],
            ["metadata_value.metadata_value_id"],
            name="fk_metadata_value",
        ),
    )

    # Create action source metadata table
    create_table(
        models.ActionSourceMetadata,
        sa.ForeignKeyConstraint(["action_id"], ["action.action_id"], name="fk_action"),
        sa.ForeignKeyConstraint(
            ["metadata_type_id"],
            ["metadata_type.metadata_type_id"],
            name="fk_metadata_type",
        ),
    )

    # Create document table
    create_table(
        models.Document,
        sa.ForeignKeyConstraint(
            ["action_id"], ["action.action_id"], name="fk_action_type"
        ),
        sa.ForeignKeyConstraint(
            ["language_id"], ["language.language_id"], name="fk_language"
        ),
    )

    # Create passage table
    create_table(
        models.Passage,
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
    )

    # Create passage metadata table
    create_table(
        models.PassageMetadata,
        sa.ForeignKeyConstraint(
            ["metadata_value_id"],
            ["metadata_value.metadata_value_id"],
            name="fk_metadata_value",
        ),
        sa.ForeignKeyConstraint(
            ["passage_id"], ["passage.passage_id"], name="fk_passage"
        ),
    )
