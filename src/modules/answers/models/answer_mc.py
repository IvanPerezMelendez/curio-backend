import uuid

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.base_model import BaseModel


class AnswerMCModel(BaseModel):
    """Covers multiple-choice, odd-one-out and image (all pick an index)."""
    __tablename__ = "answers_multiple_choice"

    answer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("answers.id"), nullable=False, unique=True
    )
    picked_index: Mapped[int] = mapped_column(Integer, nullable=False)
