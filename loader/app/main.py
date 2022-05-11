import asyncio
import logging.config
import os
from pathlib import Path

import httpx

from app.db.session import get_db
from app.loaders.loader_cclw_v2.extract.main import extract
from app.loaders.loader_cclw_v2.load.main import load
from app.loaders.loader_cclw_v2.transform.main import transform
from app.poster.main import post_all_to_backend_api
from app.service.context import Context
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

# transport retries are for connection errors, not 5XX
transport = httpx.AsyncHTTPTransport(retries=3)


def get_data_dir():
    data_dir = os.environ.get("DATA_DIR")
    if data_dir:
        data_dir = Path(data_dir).resolve()
    else:
        data_dir = Path(__file__).parent.resolve() / ".." / "data"
    return data_dir


async def main():
    """ETL for policy data.

    Extact policy data from known CCLW data source (and later this will be event-driven)
    Transform the policy data into something usable.
    Load the policy data into our backend.

    :return:
    """
    data_dir = get_data_dir()

    # find the un-processed CSV in the provided data folder
    csv_file = None
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file == "cclw_new_format_20220503.csv":
                csv_file = os.path.join(root, file)
                break
    if not csv_file:
        raise Exception(f"CSV not found at path {data_dir}")

    data = extract(csv_file)
    policies = transform(data)  # noqa: F841
    for db in get_db():
        async with httpx.AsyncClient(transport=transport, timeout=10) as client:
            ctx = Context(
                db=db,
                client=client,
            )
            await load(ctx, policies)

            # once all data has been loaded into database, upload files to cloud
            await upload_all_documents(ctx)

            # This will normally be triggered separately, but we're
            # expediting the load for alpha.
            post_all_to_backend_api(ctx)


if __name__ == "__main__":

    if os.getenv("ENV") != "production":
        # for running locally (outside docker)
        from dotenv import load_dotenv

        load_dotenv("../../.env")
        load_dotenv("../../.env.local")

    asyncio.run(main())
