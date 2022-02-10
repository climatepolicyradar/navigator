"""fix source table column type

Revision ID: 0004
Revises: 0003
Create Date: 2022-01-10 02:47:12.512491-08:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade():
    # Change "name" column in "source" table from CHAR to VARCHAR
    op.alter_column("source", "name", type_=sa.VARCHAR(length=128))


def downgrade():
    pass
