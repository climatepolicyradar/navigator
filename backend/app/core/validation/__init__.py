import os
import re

PIPELINE_BUCKET = os.environ["PIPELINE_BUCKET"]
IMPORT_ID_MATCHER = re.compile(r"\w+\.\w+\.\w+\.\w+")
