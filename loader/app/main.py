import logging.config
import os
from pathlib import Path

from app.extract import extract
from app.load import load
from app.transform import transform

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default'],
            'level': 'INFO',
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}

logging.config.dictConfig(DEFAULT_LOGGING)


def get_data_dir():
    data_dir = os.environ.get('DATA_DIR')
    if data_dir:
        data_dir = Path(data_dir).resolve()
    else:
        data_dir = Path(__file__).parent.resolve() / '..' / 'data'
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
    policies = transform(data)
    load(policies)


if __name__ == "__main__":

    if os.getenv("ENV") != "production":
        # for running locally (outside docker)
        from dotenv import load_dotenv

        load_dotenv("../../.env")
        load_dotenv("../../.env.local")

    main()
    # lang = None
    # x = get_language_id((lang or "eng").lower())
    # print(x)
