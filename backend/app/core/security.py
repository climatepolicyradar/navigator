import os
from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/tokens")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
# TODO: revisit/configure access token expiry
ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60  # 24 hours for access token
PASSWORD_RESET_TOKEN_EXPIRE_MINUTES = float(
    os.getenv("PASSWORD_RESET_TOKEN_EXPIRY_MINUTES", "30")
)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(*, data: dict, minutes: Optional[int] = None):
    to_encode = data.copy()
    expiry_minutes = minutes or ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.utcnow() + timedelta(minutes=expiry_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_password_reset_token_expiry_ts(minutes: Optional[int] = None) -> datetime:
    expiry_minutes = minutes or PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
    return datetime.utcnow() + timedelta(minutes=expiry_minutes)
