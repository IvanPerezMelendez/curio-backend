import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from src.core.security import decode_token
from src.database import get_db
from src.modules.users.models.user import UserModel
from src.modules.users.repository import UserRepository
from src.modules.users.service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def _user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    service: UserService = Depends(_user_service),
) -> UserModel:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user_id_str = decode_token(token)
        user_id = uuid.UUID(user_id_str)
    except (InvalidTokenError, ValueError):
        raise credentials_exc

    user = service.get_by_id(user_id)
    if not user or not user.is_active:
        raise credentials_exc
    return user


CurrentUser = Annotated[UserModel, Depends(get_current_user)]
