import csv
from app.db.models import Language

def populate_language(db):
    """Populate lookup tables with standard values"""

    # Codes are obtained from: https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab

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


