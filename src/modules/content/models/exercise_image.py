import uuid

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.base_model import BaseModel


class ExerciseImageModel(BaseModel):
    __tablename__ = "exercises_image"

    exercise_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("exercises.id"), nullable=False, unique=True
    )
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    image_label: Mapped[str] = mapped_column(String(300), nullable=False)
    image_color: Mapped[str] = mapped_column(String(20), nullable=False)
    options: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    correct_index: Mapped[int] = mapped_column(Integer, nullable=False)
