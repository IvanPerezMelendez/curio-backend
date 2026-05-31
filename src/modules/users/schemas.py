import uuid
from datetime import date

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegisterIn(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: uuid.UUID
    email: str
    streak_current: int
    streak_longest: int
    last_visit: date | None = None
    is_active: bool


class CategoryProgressOut(BaseModel):
    category_id: uuid.UUID
    category_name: str
    sessions_completed: int


class UserStatsOut(BaseModel):
    total_sessions: int
    total_exercises: int
    correct_answers: int
    accuracy: float
    category_progress: list[CategoryProgressOut]
