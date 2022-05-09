"""add md5sum to document

Revision ID: 0010
Revises: 0009
Create Date: 2022-05-06 09:46:16.476113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0010"
down_revision = "0009"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("document", sa.Column("md5_sum", sa.Text(), nullable=True))
    op.alter_column("document", "source_url", existing_type=sa.TEXT(), nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("document", "source_url", existing_type=sa.TEXT(), nullable=True)
    op.drop_column("document", "md5_sum")
    # ### end Alembic commands ###