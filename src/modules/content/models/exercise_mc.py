import uuid

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.base_model import BaseModel


class ExerciseMCModel(BaseModel):
    """Covers both multiple-choice and odd-one-out (same structure)."""
    __tablename__ = "exercises_multiple_choice"

    exercise_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("exercises.id"), nullable=False, unique=True
    )
    options: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    correct_index: Mapped[int] = mapped_column(Integer, nullable=False)
