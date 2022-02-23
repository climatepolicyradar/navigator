import os
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.api.api_v1.routers.actions import actions_router
from app.api.api_v1.routers.auth import auth_router
from app.api.api_v1.routers.documents import documents_router
from app.api.api_v1.routers.lookups import lookups_router
from app.api.api_v1.routers.users import users_router
from app.core import config
from app.core.auth import get_current_active_user
from app.db.session import SessionLocal
from app.log import get_logger

logger = get_logger(__name__)

app = FastAPI(title=config.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api")

# Add CORS middleware to allow cross origin requests from any port
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response


@app.get("/api/v1", include_in_schema=False)
async def root():
    return {"message": "Hello World"}


# Routers
app.include_router(
    users_router,
    prefix="/api/v1",
    tags=["Users"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(auth_router, prefix="/api", tags=["Authentication"])
app.include_router(actions_router, prefix="/api/v1", tags=["Actions"])
app.include_router(documents_router, prefix="/api/v1", tags=["Documents"])
app.include_router(lookups_router, prefix="/api/v1", tags=["Lookups"])


class MissingEnvironmentVariableError(Exception):
    """Exception for missing environment variables"""


def assert_environment_variables():
    """Check that all required environment variables exist."""
    required_env_vars = (
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "DATABASE_URL",
        "SUPERUSER_EMAIL",
        "SUPERUSER_PASSWORD",
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_REGION",
    )

    missing_env_vars = [e for e in required_env_vars if not os.getenv(e)]

    if missing_env_vars:
        raise MissingEnvironmentVariableError(
            f"Environment variable(s) {', '.join(missing_env_vars)} do(es) not exist."
        )


@app.exception_handler(IntegrityError)
async def integrityerror_handler(request: Request, exc: Exception):
    """Handle IntegrityError exceptions.

    TODO map specific errors.
    """
    msg = str(exc)
    if hasattr(exc, 'message'):
        msg = exc.message

    status = 500
    if "duplicate key" in msg:
        status = 400
        msg = "Conflict error: item already exists in database"
    else:
        logger.error(exc)

    return JSONResponse({"message": msg}, status_code=status)


if __name__ == "__main__":
    assert_environment_variables()
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
