import uuid

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.base_model import BaseModel


class ExerciseEstimationModel(BaseModel):
    __tablename__ = "exercises_estimation"

    exercise_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("exercises.id"), nullable=False, unique=True
    )
    unit: Mapped[str] = mapped_column(String(50), nullable=False)
    min_val: Mapped[float] = mapped_column(Float, nullable=False)
    max_val: Mapped[float] = mapped_column(Float, nullable=False)
    step: Mapped[float] = mapped_column(Float, nullable=False)
    default_value: Mapped[float] = mapped_column(Float, nullable=False)
    correct: Mapped[float] = mapped_column(Float, nullable=False)
    tolerance: Mapped[float] = mapped_column(Float, nullable=False)
