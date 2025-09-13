from datetime import datetime, timedelta
from typing import Optional

import jwt
from passlib.handlers.django import django_pbkdf2_sha256

from .config import settings

algorithm = "HS256"


def encode_token(payload: dict) -> str:
    expire_time = datetime.now() + timedelta(seconds=settings.TOKEN_DURATION)
    return jwt.encode({**payload, "exp": expire_time}, settings.SECRET_KEY.get_secret_value(), algorithm=algorithm)


def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.SECRET_KEY.get_secret_value(), algorithms=[algorithm])
    except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError, jwt.DecodeError):
        return None


def hash_password(password: str) -> str:
    return str(django_pbkdf2_sha256.hash(password))


def check_password(password: str, hashed_password: str) -> bool:
    return django_pbkdf2_sha256.verify(password, hashed_password)
