from datetime import date

from sqlalchemy import Boolean, Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.base_model import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_visit: Mapped[date | None] = mapped_column(Date, nullable=True)
    streak_current: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    streak_longest: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
