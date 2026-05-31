from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from src.settings import settings

password_hash = PasswordHash.recommended()
_DUMMY_HASH = password_hash.hash("dummy")


def get_password_hash(plain: str) -> str:
    return password_hash.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)


def verify_password_safe(plain: str, hashed: str | None) -> bool:
    """Always runs a hash comparison to prevent timing attacks."""
    if not hashed:
        password_hash.verify(plain, _DUMMY_HASH)
        return False
    return password_hash.verify(plain, hashed)


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> str:
    """Returns the `sub` claim (user id string) or raises InvalidTokenError."""
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    sub: str | None = payload.get("sub")
    if sub is None:
        raise InvalidTokenError("Missing sub claim")
    return sub
