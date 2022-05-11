"""add publication date to document

Revision ID: 0012
Revises: 0011
Create Date: 2022-05-11 12:00:33.538285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0012"
down_revision = "0011"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "document", sa.Column("publication_ts", sa.DateTime(), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("document", "publication_ts")
    # ### end Alembic commands ###
