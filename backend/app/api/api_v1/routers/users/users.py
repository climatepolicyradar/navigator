from fastapi import APIRouter, Depends

from app.core.auth import get_current_active_user
from app.db.schemas.user import User

users_router = r = APIRouter()


@r.get("/users/me", response_model=User, response_model_exclude_none=True)
async def user_me(current_user=Depends(get_current_active_user)):
    """Gets own user"""
    return current_user
