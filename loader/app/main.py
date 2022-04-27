import logging.config
import os
from pathlib import Path

from app.db.session import get_db
from app.loader.extract.main import extract
from app.loader.load.main import load  # noqa: F401
from app.loader.transform.main import transform
from app.poster.main import post_all_to_backend_api
from app.service.document_upload import upload_all_documents

DEFAULT_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["default"],
            "level": "INFO",
        },
        "__main__": {  # if __name__ == '__main__'
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

logging.config.dictConfig(DEFAULT_LOGGING)

logger = logging.getLogger(__file__)


def get_data_dir():
    data_dir = os.environ.get("DATA_DIR")
    if data_dir:
        data_dir = Path(data_dir).resolve()
    else:
        data_dir = Path(__file__).parent.resolve() / ".." / "data"
    return data_dir


def main():
    """ETL for policy data.

    Extact policy data from known CCLW data source (and later this will be event-driven)
    Transform the policy data into something usable.
    Load the policy data into our backend.

    :return:
    """
    data_dir = get_data_dir()

    data = extract(data_dir)
    policies = transform(data)  # noqa: F841
    for db in get_db():
        load(db, policies)

        # once all data has been loaded into database, upload files to cloud
        upload_all_documents(db)

        # This will normally be triggered separately, but we're
        # expediting the load for alpha.
        post_all_to_backend_api(db)


if __name__ == "__main__":

    if os.getenv("ENV") != "production":
        # for running locally (outside docker)
        from dotenv import load_dotenv

        load_dotenv("../../.env")
        load_dotenv("../../.env.local")

    main()
