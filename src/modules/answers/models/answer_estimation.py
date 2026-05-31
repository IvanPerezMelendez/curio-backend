import uuid

from sqlalchemy import Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.base_model import BaseModel


class AnswerEstimationModel(BaseModel):
    __tablename__ = "answers_estimation"

    answer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("answers.id"), nullable=False, unique=True
    )
    submitted_value: Mapped[float] = mapped_column(Float, nullable=False)
