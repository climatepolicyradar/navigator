import csv
from app.db.models import Geography

def populate_geography(db):
    # Bulk insert geography values into geography lookup table

    geographies = []
    # Get iso-3166 country codes. This file contains the standard iso-3166 codes + additional country codes for
    # regions that are missing - e.g. sub-saharan africa
    with open('alembic/versions/lookups/geography-iso-3166.csv', mode ='r') as file:
        # reading the CSV file
        csvFile = csv.DictReader(file)
        geographies = [ l for l in csvFile ]

    # Insert language codes into db table
    for record in geographies:
        print(record)
        # print(dir(record))
        # first instead the parent geo
        # op.execute(
            # insert(geography_tbl)
            # .values(
                # display_value=record["World Bank Region"],
                # value=record["World Bank Region"],
                # type="World Bank Region",
            # )
            # .on_conflict_do_nothing()
        # )

        # get the parent's id
        # parent_id = (
            # geography_tbl.select()
            # .with_only_columns(geography_tbl.columns["id"])
            # .where(
                # geography_tbl.columns["value"] == record["World Bank Region"]
            # )
            # .scalar_subquery()
        # )

        # now insert the child
        # op.execute(
            # geography_tbl.insert().values(
                # display_value=record["Name"],
                # value=record["Iso"],
                # type="ISO-3166",
                # parent_id=parent_id,
            # )
        # )
