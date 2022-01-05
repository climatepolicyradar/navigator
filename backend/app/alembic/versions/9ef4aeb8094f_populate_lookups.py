"""Populate lookups

Revision ID: 9ef4aeb8094f
Revises: ab8d144a6e80
Create Date: 2022-01-05 06:00:34.120168-08:00

"""
from alembic import op
from sqlalchemy import Table, MetaData
import pandas as pd


# revision identifiers, used by Alembic.
revision = "9ef4aeb8094f"
down_revision = "ab8d144a6e80"
branch_labels = None
depends_on = None


def upgrade():
    """Populate lookup tables with standard values"""

    # Get database metadata and reflect lookup tables we need to populate
    db_meta = MetaData(bind=op.get_bind())
    db_meta.reflect(
        only=(
            "language",
            "geography",
            "action_type",
            "source",
        )
    )

    # Bulk insert iso-639-3 langyage codes into language lookup table
    # Codes are obtained from: https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab
    lang_tbl = Table("language", db_meta)

    # Make sure that columns part1_code and part2_code are nullable
    op.alter_column("language", "part1_code", nullable=True)
    op.alter_column("language", "part2_code", nullable=True)

    # Get iso-630-3 codes from extracted file
    lang_df = pd.read_csv(
        "app/alembic/versions/lookups/language-iso-639-3.txt",
        sep="\t",
        usecols=["Id", "Part1", "Part2B", "Ref_Name"],
    )
    # Rename columns to match the column names in the database table
    lang_df.rename(
        columns={
            "Id": "language_code",
            "Part2B": "part2_code",
            "Part1": "part1_code",
            "Ref_Name": "name",
        },
        inplace=True,
    )
    lang_df.dropna(subset=["language_code"], inplace=True)

    # Convert dataframe to list of dictionaries and remove keys with null values
    lang_data = [
        {k: v if pd.notnull(v) else None for k, v in lang.items()}
        for lang in lang_df.to_dict(orient="records")
    ]

    # Bulk insert language codes into language table
    op.bulk_insert(lang_tbl, lang_data)

    # Bulk insert geography values into geography lookup table
    geography_tbl = Table("geography", db_meta)

    # Make sure that column french_shortname is nullable
    op.alter_column("geography", "french_shortname", nullable=True)

    # Get iso-3166 country codes. This file contains the standard iso-3166 codes + additional country codes for
    # regions that are missing - e.g. sub-saharan africa
    geography_df = pd.read_csv(
        "app/alembic/versions/lookups/geography-iso-3166.csv", usecols=["Iso", "Name"]
    )
    # Rename columns to match the column names in the database table
    geography_df.rename(
        columns={"Name": "english_shortname", "Iso": "country_code"}, inplace=True
    )

    # Bulk insert language codes into db table
    op.bulk_insert(
        geography_tbl,
        geography_df.to_dict(orient="records"),
    )

    # Insert standard action types into action_type table
    action_type_tbl = Table("action_type", db_meta)
    op.bulk_insert(
        action_type_tbl,
        [
            {"type_name": "Policy"},
            {"type_name": "Law"},
        ],
    )

    # Insert standard sources into source table
    action_type_tbl = Table("source", db_meta)
    op.bulk_insert(
        action_type_tbl,
        [
            {"name": "CCLW"},
        ],
    )


def downgrade():
    """Remove created lookup values"""

    # Delete rows from language table
    op.execute("DELETE FROM language")

    # Delete rows from geography table
    op.execute("DELETE FROM geography")

    # Delete rows from action_type table
    op.execute("DELETE FROM action_type")

    # Delete rows from source table
    op.execute("DELETE FROM source")

    op.alter_column("language", "part1_code", nullable=False)
    op.alter_column("language", "part2_code", nullable=False)
    op.alter_column("geography", "french_shortname", nullable=False)
