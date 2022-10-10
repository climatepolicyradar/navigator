from fastapi import Depends, Request

from app.api.api_v1.schemas.metadata import Config
from app.db.session import get_db
from .router import lookups_router
from .util import get_metadata


@lookups_router.get("/config", response_model=Config)
def lookup_config(
    request: Request,
    db=Depends(get_db),
):
    """Get the config for the metadata."""
    return get_metadata(db)
