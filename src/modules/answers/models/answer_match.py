import uuid

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.base_model import BaseModel


class AnswerMatchModel(BaseModel):
    __tablename__ = "answers_match"

    answer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("answers.id"), nullable=False, unique=True
    )
    left_indices: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)
    right_indices: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)
