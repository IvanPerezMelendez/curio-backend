from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.core.security import create_access_token
from src.database import get_db
from src.modules.users.repository import UserRepository
from src.modules.users.schemas import RegisterIn, Token, UserOut
from src.modules.users.service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


def _service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register(
    body: RegisterIn,
    service: UserService = Depends(_service),
) -> UserOut:
    user = service.register(body.email, body.password)
    return UserOut(
        id=user.id,
        email=user.email,
        streak_current=user.streak_current,
        streak_longest=user.streak_longest,
        last_visit=user.last_visit,
        is_active=user.is_active,
    )


@router.post(
    "/token",
    response_model=Token,
    summary="Login — get JWT access token",
    description=(
        "Standard OAuth2 password flow. Send `username` (email) and `password` "
        "as form data. Returns a Bearer JWT token valid for 30 days."
    ),
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: UserService = Depends(_service),
) -> Token:
    user = service.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")

    token = create_access_token(subject=str(user.id))
    return Token(access_token=token)
