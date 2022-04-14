"""add constraint to documents

Revision ID: 0003
Revises: 0002
Create Date: 2022-04-14 16:04:44.896800

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(
        op.f("uq_document__name"),
        "document",
        ["name", "geography_id", "type_id", "source_id"],
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f("uq_document__name"), "document", type_="unique")
    # ### end Alembic commands ###
