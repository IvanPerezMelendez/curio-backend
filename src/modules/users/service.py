import uuid
from datetime import date, timedelta

from fastapi import HTTPException, status

from src.core.security import get_password_hash, verify_password_safe
from src.modules.users.models.user import UserModel
from src.modules.users.repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register(self, email: str, password: str) -> UserModel:
        if self.repository.get_by_email(email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )
        return self.repository.create({
            "email": email,
            "hashed_password": get_password_hash(password),
        })

    def authenticate(self, email: str, password: str) -> UserModel | None:
        user = self.repository.get_by_email(email)
        if not verify_password_safe(password, user.hashed_password if user else None):
            return None
        return user

    def get_by_id(self, user_id: uuid.UUID) -> UserModel | None:
        return self.repository.get_by_id(user_id)

    def get_by_email(self, email: str) -> UserModel | None:
        return self.repository.get_by_email(email)

    def update_streak(self, user: UserModel, today: date) -> UserModel:
        if user.last_visit == today:
            return user

        yesterday = today - timedelta(days=1)
        new_streak = (user.streak_current + 1) if user.last_visit == yesterday else 1
        new_longest = max(user.streak_longest, new_streak)

        return self.repository.update(user.id, {
            "streak_current": new_streak,
            "streak_longest": new_longest,
            "last_visit": today,
        })
