"""init

Revision ID: 0002
Revises: 0001
Create Date: 2022-04-07 11:55:34.455411

"""

import pandas as pd
from alembic import op
from sqlalchemy import String, Integer, SmallInteger, CHAR
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import table, column, TableClause

# revision identifiers, used by Alembic.
revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    """Populate lookup tables with standard values"""

    # Bulk insert iso-639-3 language codes into language lookup table
    # Codes are obtained from: https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab
    lang_tbl: TableClause = table(
        "language",
        column("id", SmallInteger),
        column("language_code", CHAR(3)),
        column("part1_code", CHAR(2)),
        column("part2_code", CHAR(3)),
        column("name", String),
    )

    # Get iso-630-3 codes from extracted file
    lang_df = pd.read_csv(
        "alembic/versions/lookups/language-iso-639-3.txt",
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
    geography_tbl: TableClause = table(
        "geography",
        column("id", SmallInteger),
        column("display_value", String),
        column("value", String),
        column("type", String),
        column("parent_id", Integer),
    )

    # Get iso-3166 country codes. This file contains the standard iso-3166 codes + additional country codes for
    # regions that are missing - e.g. sub-saharan africa
    geography_df = pd.read_csv(
        "alembic/versions/lookups/geography-iso-3166.csv"
    )

    # Insert language codes into db table
    for record in geography_df.to_dict(orient="records"):
        # print(record)
        # print(dir(record))
        # first instead the parent geo
        op.execute(
            insert(geography_tbl)
            .values(
                display_value=record["World Bank Region"],
                value=record["World Bank Region"],
                type="World Bank Region",
            )
            .on_conflict_do_nothing()
        )

        # get the parent's id
        parent_id = (
            geography_tbl.select()
            .with_only_columns(geography_tbl.columns["id"])
            .where(
                geography_tbl.columns["value"] == record["World Bank Region"]
            )
            .scalar_subquery()
        )

        # now insert the child
        op.execute(
            geography_tbl.insert().values(
                display_value=record["Name"],
                value=record["Iso"],
                type="ISO-3166",
                parent_id=parent_id,
            )
        )

    # Insert standard document types into document_type table
    document_type_tbl: TableClause = table(
        "document_type",
        column("id", SmallInteger),
        column("name", String),
        column("description", String),
    )

    op.bulk_insert(
        document_type_tbl,
        [
            {"name": "Policy", "description": "Policy"},
            {"name": "Law", "description": "Law"},
        ],
    )

    # Insert standard sources into source table
    source_tbl: TableClause = table(
        "source",
        column("id", SmallInteger),
        column("name", String),
    )

    op.bulk_insert(
        source_tbl,
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

    # Delete rows from document_type table
    op.execute("DELETE FROM document_type")

    # Delete rows from source table
    op.execute("DELETE FROM source")
