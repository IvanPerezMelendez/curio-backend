import uuid

from sqlalchemy.orm import Session

from src.core.base_repository import BaseRepository
from src.modules.users.models.user import UserModel


class UserRepository(BaseRepository[UserModel]):
    def __init__(self, db: Session):
        super().__init__(UserModel, db)

    def get_by_email(self, email: str) -> UserModel | None:
        return self.get_by_attributes(email=email)

    def get_by_id(self, user_id: uuid.UUID) -> UserModel | None:
        return super().get_by_id(user_id)
