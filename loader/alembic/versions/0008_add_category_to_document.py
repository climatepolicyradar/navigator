"""add category to document

Revision ID: 0008
Revises: 0007
Create Date: 2022-05-03 10:01:13.763546

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0008"
down_revision = "0007"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "document", sa.Column("category_id", sa.SmallInteger(), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("document", "category_id")
    # ### end Alembic commands ###