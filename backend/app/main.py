import logging.config

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_health import health
from fastapi_pagination import add_pagination
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.requests import Request

from app.api.api_v1.routers.actions import actions_router
from app.api.api_v1.routers.auth import auth_router
from app.api.api_v1.routers.documents import documents_router
from app.api.api_v1.routers.lookups import lookups_router
from app.api.api_v1.routers.users import users_router
from app.api.api_v1.routers.admin import admin_users_router
from app.api.api_v1.routers.unauthenticated import unauthenticated_router
from app.core import config
from app.core.auth import get_current_active_user, get_current_active_superuser
from app.core.health import is_database_online
from app.core.ratelimit import limiter
from app.db.session import SessionLocal
from navigator.core.log import get_logger

logger = get_logger(__name__)

app = FastAPI(title=config.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api")

# Add CORS middleware to allow cross origin requests from any port
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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
    users_router,
    prefix="/api/v1",
    tags=["Users"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(
    admin_users_router,
    prefix="/api/v1/admin",
    tags=["Admin"],
    dependencies=[Depends(get_current_active_superuser)],
)
app.include_router(auth_router, prefix="/api", tags=["Authentication"])
app.include_router(actions_router, prefix="/api/v1", tags=["Actions"])
app.include_router(documents_router, prefix="/api/v1", tags=["Documents"])
app.include_router(lookups_router, prefix="/api/v1", tags=["Lookups"])

# add pagination support to all routes that ask for it
add_pagination(app)

# rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


def get_log_level() -> str:
    from boto.utils import get_instance_metadata
    import sys

    # if this is being run by a test
    if "pytest" in sys.modules:
        return "INFO"

    try:
        m = get_instance_metadata(timeout=1, num_retries=1)
        if m and len(m.keys()) > 0:
            # not DEBUG level in the cloud
            return "INFO"
    except:  # noqa: E722
        pass
    return "DEBUG"


DEFAULT_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["default"],
            "level": get_log_level(),
        },
        "__main__": {  # if __name__ == '__main__'
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": False,
        },
        # also "uvicorn", "uvicorn.error", "uvicorn.access" etc
    },
}

logging.config.dictConfig(DEFAULT_LOGGING)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
