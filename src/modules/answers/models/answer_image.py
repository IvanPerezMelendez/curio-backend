import uuid

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.base_model import BaseModel


class AnswerImageModel(BaseModel):
    __tablename__ = "answers_image"

    answer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("answers.id"), nullable=False, unique=True
    )
    picked_index: Mapped[int] = mapped_column(Integer, nullable=False)
