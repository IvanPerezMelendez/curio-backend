import uuid

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.base_model import BaseModel


class ExerciseMatchPairModel(BaseModel):
    __tablename__ = "exercises_match_pairs"

    exercise_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("exercises.id"), nullable=False
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    left_text: Mapped[str] = mapped_column(String(300), nullable=False)
    right_text: Mapped[str] = mapped_column(String(300), nullable=False)
