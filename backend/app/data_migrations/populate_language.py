import csv
from app.db.models import Language
from app.db.session import SessionLocal
from .utils import has_rows


# Create a new dialect - as its a bit wierd
class iso_csv(csv.Dialect):
    """Class to define the dialect of CSV that is used for the languages."""

    delimiter = "\t"
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = "\r\n"
    quoting = csv.QUOTE_NONE


csv.register_dialect("iso_csv", iso_csv)


def populate_language(db: SessionLocal) -> None:
    """Populate languages from CSV file."""

    if has_rows(db, Language):
        return

    # Codes are obtained from: https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab
    # Get iso-630-3 codes from extracted file
    with open("app/data_migrations/data/language-iso-639-3.txt", mode="r") as file:
        # reading the CSV file
        csvFile = csv.DictReader(file, dialect=iso_csv)

        for row in csvFile:
            lang = {}
            lang["language_code"] = row.pop("Id")
            lang["part1_code"] = row.pop("Part1")
            lang["part2_code"] = row.pop("Part2B")
            lang["name"] = row.pop("Ref_Name")

            db.add(Language(**lang))
