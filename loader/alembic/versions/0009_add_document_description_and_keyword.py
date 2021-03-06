"""add document description and keyword metadata

Revision ID: 0009
Revises: 0008
Create Date: 2022-05-05 14:02:14.834644

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0009"
down_revision = "0008"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "keyword",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_keyword")),
    )
    op.create_table(
        "document_keyword",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("keyword_id", sa.Integer(), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["document_id"],
            ["document.id"],
            name=op.f("fk_document_keyword__document_id__document"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["keyword_id"],
            ["keyword.id"],
            name=op.f("fk_document_keyword__keyword_id__keyword"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_document_keyword")),
    )
    op.drop_table("document_category")
    op.drop_table("category")
    op.add_column("document", sa.Column("description", sa.Text(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("document", "description")
    op.create_table(
        "category",
        sa.Column(
            "id",
            sa.INTEGER(),
            server_default=sa.text("nextval('category_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("name", sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column("description", sa.TEXT(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_category"),
        postgresql_ignore_search_path=False,
    )
    op.create_table(
        "document_category",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("type_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("document_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["document_id"],
            ["document.id"],
            name="fk_document_category__document_id__document",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["type_id"], ["category.id"], name="fk_document_category__type_id__category"
        ),
        sa.PrimaryKeyConstraint("id", name="pk_document_category"),
    )
    op.drop_table("document_keyword")
    op.drop_table("keyword")
    # ### end Alembic commands ###
