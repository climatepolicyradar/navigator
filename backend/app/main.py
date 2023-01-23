import logging
import logging.config
import os

import json_logging
import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_health import health
from fastapi_pagination import add_pagination
from slowapi.errors import RateLimitExceeded
from slowapi.extension import _rate_limit_exceeded_handler
from starlette.requests import Request
from alembic.command import upgrade
from alembic.config import Config

from app.api.api_v1.routers.admin import admin_users_router
from app.api.api_v1.routers.auth import auth_router
from app.api.api_v1.routers.documents import documents_router
from app.api.api_v1.routers.lookups import lookups_router
from app.api.api_v1.routers.search import search_router
from app.api.api_v1.routers.unauthenticated import unauthenticated_router
from app.api.api_v1.routers.summaries import summary_router
from app.core import config
from app.core.auth import get_current_active_superuser
from app.core.health import is_database_online
from app.core.ratelimit import limiter
from app.db.session import SessionLocal

os.environ["SKIP_ALEMBIC_LOGGING"] = "1"

# Clear existing log handlers so we always log in structured JSON
root_logger = logging.getLogger()
if root_logger.handlers:
    for handler in root_logger.handlers:
        root_logger.removeHandler(handler)

for _, logger in logging.root.manager.loggerDict.items():
    if isinstance(logger, logging.Logger):
        logger.propagate = True
        if logger.handlers:
            for handler in logger.handlers:
                logger.removeHandler(handler)

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
DEFAULT_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
    },
    "loggers": {},
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,
    },
}
logger = logging.getLogger(__name__)
logging.config.dictConfig(DEFAULT_LOGGING)

ENABLE_API_DOCS = os.getenv("ENABLE_API_DOCS", "False").lower() == "true"
_docs_url = "/api/docs" if ENABLE_API_DOCS else None
_openapi_url = "/api" if ENABLE_API_DOCS else None

app = FastAPI(title=config.PROJECT_NAME, docs_url=_docs_url, openapi_url=_openapi_url)
json_logging.init_fastapi(enable_json=True)
json_logging.init_request_instrument(app)
json_logging.config_root_logger()

_ALLOW_ORIGIN_REGEX = (
    r"http://localhost:3000|"
    r"https://.+\.climatepolicyradar\.org|"
    r"https://.+\.dev.climatepolicyradar\.org|"
    r"https://.+\.sandbox\.climatepolicyradar\.org|"
    r"https://climate-laws\.org|"
    r"https://.+\.climate-laws\.org"
)

# Add CORS middleware to allow cross origin requests from any port
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=_ALLOW_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# add health endpoint
app.add_api_route("/health", health([is_database_online]))


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response


@app.get("/api/v1", include_in_schema=False)
async def root():
    return {"message": "CPR API v1"}


# Routers
app.include_router(
    unauthenticated_router,
    prefix="/api/v1",
    tags=["Unauthenticated"],  # or Public?
)
app.include_router(
    admin_users_router,
    prefix="/api/v1/admin",
    tags=["Admin"],
    dependencies=[Depends(get_current_active_superuser)],
)
app.include_router(auth_router, prefix="/api", tags=["Authentication"])
app.include_router(documents_router, prefix="/api/v1", tags=["Documents"])
app.include_router(lookups_router, prefix="/api/v1", tags=["Lookups"])
app.include_router(search_router, prefix="/api/v1", tags=["Searches"])
app.include_router(summary_router, prefix="/api/v1", tags=["Summaries"])

# add pagination support to all routes that ask for it
add_pagination(app)

# rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.on_event("startup")
async def startup() -> None:
    upgrade(Config("./alembic.ini"), "head")


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8888,
        log_config=DEFAULT_LOGGING,
    )  # type: ignore
