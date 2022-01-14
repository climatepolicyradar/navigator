import os

from fastapi import FastAPI, Depends
from starlette.requests import Request
import uvicorn

from app.api.api_v1.routers.users import users_router
from app.api.api_v1.routers.auth import auth_router
from app.api.api_v1.routers.documents import documents_router
from app.api.api_v1.routers.actions import actions_router
from app.api.api_v1.routers.lookups import lookups_router
from app.core import config
from app.db.session import SessionLocal
from app.core.auth import get_current_active_user


app = FastAPI(title=config.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api")


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
    pass


def assert_environment_variables():
    """
    Check that all required environment variables exist.
    """
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


if __name__ == "__main__":
    assert_environment_variables()
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
