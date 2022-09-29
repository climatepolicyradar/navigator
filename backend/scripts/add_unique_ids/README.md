# Script to add CCLW IDs to existing database rows

This script exists as a one-shot implementation (along with static ID mapping file) to
add unique IDs to document entries. These IDs are generated reproducibly from the
CCLW source data, and are expected to be used to identify documents as we run regular
imports.

When this script has been used, and the new bulk import functionality deployed, we
do not expect this script to be required again, and is left purely for information (and
as an example of implementing a simple script that interacts with the database).

## Files

- `add_unique_keys.py` is the main script
- `ids_map.json` is the mapping from internal db IDs to externally derived &
    recreatable IDs
- `extra` contains scripts, a database table export and import csv used to generate
    the above mapping
