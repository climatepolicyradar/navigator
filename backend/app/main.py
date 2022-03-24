import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_health import health
from fastapi_pagination import add_pagination
from starlette.requests import Request

from app.api.api_v1.routers.actions import actions_router
from app.api.api_v1.routers.auth import auth_router
from app.api.api_v1.routers.documents import documents_router
from app.api.api_v1.routers.lookups import lookups_router
from app.api.api_v1.routers.users import users_router
from app.core import config
from app.core.auth import get_current_active_user
from app.core.health import is_database_online
from app.db.session import SessionLocal
from navigator.core.log import get_logger

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
    return {"message": "CPR API"}


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

# add pagination support to all routes that ask for it
add_pagination(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
