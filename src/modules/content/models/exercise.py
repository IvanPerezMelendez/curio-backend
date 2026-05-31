import uuid
from enum import Enum

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.base_model import BaseModel


class ExerciseType(str, Enum):
    MULTIPLE_CHOICE = "multiple-choice"
    ODD_ONE_OUT     = "odd-one-out"
    TRUE_FALSE      = "true-false"
    IMAGE           = "image"
    MATCH           = "match"
    MAP_CLICK       = "map-click"
    CHRONOLOGICAL   = "chronological"
    ESTIMATION      = "estimation"


class ExerciseModel(BaseModel):
    __tablename__ = "exercises"

    subtopic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("subtopics.id"), nullable=False
    )
    type: Mapped[str] = mapped_column(String(30), nullable=False)
    tag: Mapped[str] = mapped_column(String(100), nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    explanation_title: Mapped[str] = mapped_column(Text, nullable=False)
    explanation_body: Mapped[str] = mapped_column(Text, nullable=False)
    explanation_fact: Mapped[str | None] = mapped_column(Text, nullable=True)
    lang: Mapped[str] = mapped_column(String(5), default="es", nullable=False)
