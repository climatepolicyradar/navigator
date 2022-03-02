"""From https://github.com/climatepolicyradar/cpr/blob/master/nbs/policy-etl.ipynb

This module assumes the presence of CCLW CSVs in a known local location.

The CSVs contain hints (URLs) where actions and documents can be found.
These hints would normally

"""

from app.transform.main import transform
