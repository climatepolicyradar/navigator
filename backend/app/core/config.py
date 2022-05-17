import os

# TODO is this module really needed?

PROJECT_NAME = "navigator"

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

API_V1_STR = "/api/v1"

# OpenSearch Config
OPENSEARCH_URL = os.environ["OPENSEARCH_URL"]
OPENSEARCH_USERNAME = os.environ["OPENSEARCH_USER"]
OPENSEARCH_PASSWORD = os.environ["OPENSEARCH_PASSWORD"]
OPENSEARCH_INDEX = os.environ["OPENSEARCH_INDEX"]
OPENSEARCH_REQUEST_TIMEOUT: int = int(os.getenv("OPENSEARCH_REQUEST_TIMEOUT", "30"))
OPENSEARCH_USE_SSL: bool = os.getenv("OPENSEARCH_USE_SSL", "False").lower() == "true"
OPENSEARCH_VERIFY_CERTS: bool = (
    os.getenv("OPENSEARCH_VERIFY_CERTS", "False").lower() == "true"
)
OPENSEARCH_SSL_WARNINGS: bool = (
    os.getenv("OPENSEARCH_SSL_WARNINGS", "False").lower() == "true"
)

# OpenSearch Index Config
OPENSEARCH_INDEX_INNER_PRODUCT_THRESHOLD: float = float(
    os.getenv("OPENSEARCH_INDEX_INNER_PRODUCT_THRESHOLD", "70.0")
)
OPENSEARCH_INDEX_MAX_DOC_COUNT: int = int(
    os.getenv("OPENSEARCH_INDEX_MAX_DOC_COUNT", "100")
)
OPENSEARCH_INDEX_MAX_PASSAGES_PER_DOC: int = int(
    os.getenv("OPENSEARCH_INDEX_MAX_PASSAGES_PER_DOC", "10")
)
OPENSEARCH_INDEX_KNN_K_VALUE = int(os.getenv("OPENSEARCH_INDEX_KNN_K_VALUE", "10000"))
OPENSEARCH_INDEX_N_PASSAGES_TO_SAMPLE_PER_SHARD: int = int(
    os.getenv("OPENSEARCH_INDEX_N_PASSAGES_TO_SAMPLE_PER_SHARD", "5000")
)
OPENSEARCH_INDEX_NAME_BOOST: int = int(os.getenv("OPENSEARCH_INDEX_NAME_BOOST", "100"))
OPENSEARCH_INDEX_DESCRIPTION_BOOST: int = int(
    os.getenv("OPENSEARCH_INDEX_DESCRIPTION_BOOST", "10")
)
OPENSEARCH_INDEX_NAME_KEY: str = os.getenv(
    "OPENSEARCH_INDEX_NAME_KEY", "for_search_document_name"
)
OPENSEARCH_INDEX_DESCRIPTION_KEY: str = os.getenv(
    "OPENSEARCH_INDEX_DESCRIPTION_KEY", "for_search_document_description"
)
OPENSEARCH_INDEX_DESCRIPTION_EMBEDDING_KEY: str = os.getenv(
    "OPENSEARCH_INDEX_DESCRIPTION_EMBEDDING_KEY", "document_description_embedding"
)
OPENSEARCH_INDEX_INDEX_KEY: str = os.getenv(
    "OPENSEARCH_INDEX_INDEX_KEY", "document_name_and_id"
)
OPENSEARCH_INDEX_TEXT_BLOCK_KEY: str = os.getenv(
    "OPENSEARCH_INDEX_TEXT_BLOCK_KEY", "text_block_id"
)
OPENSEARCH_INDEX_ENCODER: str = os.getenv(
    "OPENSEARCH_INDEX_ENCODER", "sentence-transformers/msmarco-distilbert-dot-v5"
)
