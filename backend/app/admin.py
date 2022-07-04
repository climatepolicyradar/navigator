from fastapi import FastAPI
from fastapi import Depends, Request

from sqladmin import ModelAdmin

from app.core.auth import get_current_active_superuser
from app.db.models import User


class AuthModelAdmin(ModelAdmin):
    def is_accessible(self, request: Request) -> bool:
        # With Authentication backend you can now access request.user.
        user = Depends(get_current_active_superuser)

        if user.is_superuser:
            return True
        return False

    def is_visible(self, request: Request) -> bool:
        # With Authentication backend you can now access request.user.
        user = Depends(get_current_active_superuser)

        if user.is_superuser:
            return True
        return False


class UserAdmin(ModelAdmin, model=User):  # type: ignore
    column_list = [User.id, User.email, User.names]  # type: ignore
