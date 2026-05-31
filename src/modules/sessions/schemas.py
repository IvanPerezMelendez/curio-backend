import uuid
from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, Field

from src.modules.content.schemas import ExerciseOut  # noqa: F401 (re-exported for router)


# ---------------------------------------------------------------------------
# Session response  (GET /sessions/today)
# ---------------------------------------------------------------------------

class CategoryOut(BaseModel):
    id: uuid.UUID
    name: str


class TopicOut(BaseModel):
    id: uuid.UUID
    name: str


class SubtopicOut(BaseModel):
    id: uuid.UUID
    name: str
    subtitle: str | None = None


class SessionTodayOut(BaseModel):
    already_done: bool
    session_id: uuid.UUID
    streak_current: int
    completed_at: datetime | None = None
    category: CategoryOut
    topic: TopicOut
    subtopic: SubtopicOut
    exercises: list[ExerciseOut]


# ---------------------------------------------------------------------------
# Answer submission  (POST /sessions/{session_id}/answers)
# ---------------------------------------------------------------------------

class MCAnswerIn(BaseModel):
    picked_index: int


class TFAnswerIn(BaseModel):
    picked_value: bool


class MatchAnswerIn(BaseModel):
    left_indices: list[int]
    right_indices: list[int]


class MapAnswerIn(BaseModel):
    picked_hotspot_key: str


class ChronoAnswerIn(BaseModel):
    submitted_order: list[str]


class EstimationAnswerIn(BaseModel):
    submitted_value: float


class SubmitMCAnswerIn(BaseModel):
    exercise_id: uuid.UUID
    exercise_type: Literal["multiple-choice"]
    answer: MCAnswerIn
    ms_to_answer: int | None = None


class SubmitOddOneOutAnswerIn(BaseModel):
    exercise_id: uuid.UUID
    exercise_type: Literal["odd-one-out"]
    answer: MCAnswerIn
    ms_to_answer: int | None = None


class SubmitTFAnswerIn(BaseModel):
    exercise_id: uuid.UUID
    exercise_type: Literal["true-false"]
    answer: TFAnswerIn
    ms_to_answer: int | None = None


class SubmitImageAnswerIn(BaseModel):
    exercise_id: uuid.UUID
    exercise_type: Literal["image"]
    answer: MCAnswerIn
    ms_to_answer: int | None = None


class SubmitMatchAnswerIn(BaseModel):
    exercise_id: uuid.UUID
    exercise_type: Literal["match"]
    answer: MatchAnswerIn
    ms_to_answer: int | None = None


class SubmitMapAnswerIn(BaseModel):
    exercise_id: uuid.UUID
    exercise_type: Literal["map-click"]
    answer: MapAnswerIn
    ms_to_answer: int | None = None


class SubmitChronoAnswerIn(BaseModel):
    exercise_id: uuid.UUID
    exercise_type: Literal["chronological"]
    answer: ChronoAnswerIn
    ms_to_answer: int | None = None


class SubmitEstimationAnswerIn(BaseModel):
    exercise_id: uuid.UUID
    exercise_type: Literal["estimation"]
    answer: EstimationAnswerIn
    ms_to_answer: int | None = None


SubmitAnswerIn = Annotated[
    SubmitMCAnswerIn
    | SubmitOddOneOutAnswerIn
    | SubmitTFAnswerIn
    | SubmitImageAnswerIn
    | SubmitMatchAnswerIn
    | SubmitMapAnswerIn
    | SubmitChronoAnswerIn
    | SubmitEstimationAnswerIn,
    Field(discriminator="exercise_type"),
]


class SubmitAnswerOut(BaseModel):
    correct: bool


# ---------------------------------------------------------------------------
# Complete session  (POST /sessions/{session_id}/complete)
# ---------------------------------------------------------------------------

class CompleteSessionOut(BaseModel):
    streak_current: int
    streak_longest: int
    correct: int
    total: int
    duration_ms: int | None = None
