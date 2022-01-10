"""fix source table column type

Revision ID: 87634be1fc8a
Revises: 9ef4aeb8094f
Create Date: 2022-01-10 02:47:12.512491-08:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "87634be1fc8a"
down_revision = "9ef4aeb8094f"
branch_labels = None
depends_on = None


def upgrade():
    # Change "name" column in "source" table from CHAR to VARCHAR
    op.alter_column("source", "name", type_=sa.VARCHAR(length=128))


def downgrade():
    pass
