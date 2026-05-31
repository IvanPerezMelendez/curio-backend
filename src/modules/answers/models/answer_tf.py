import uuid

from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.base_model import BaseModel


class AnswerTFModel(BaseModel):
    __tablename__ = "answers_true_false"

    answer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("answers.id"), nullable=False, unique=True
    )
    picked_value: Mapped[bool] = mapped_column(Boolean, nullable=False)
