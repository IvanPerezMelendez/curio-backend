import uuid
from typing import Annotated, Literal

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Content browsing schemas  (GET /content/*)
# ---------------------------------------------------------------------------

class ContentCategoryOut(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None = None
    lang: str


class ContentTopicOut(BaseModel):
    id: uuid.UUID
    category_id: uuid.UUID
    name: str
    description: str | None = None


class ContentSubtopicOut(BaseModel):
    id: uuid.UUID
    topic_id: uuid.UUID
    name: str
    subtitle: str | None = None
    position: int


class ExplanationOut(BaseModel):
    title: str
    body: str
    fact: str | None = None


class BaseExerciseOut(BaseModel):
    id: uuid.UUID
    tag: str
    question: str
    explanation: ExplanationOut
    is_review: bool = False


class MultipleChoiceOut(BaseExerciseOut):
    type: Literal["multiple-choice"]
    options: list[str]
    correct_index: int | None = None


class OddOneOutOut(BaseExerciseOut):
    type: Literal["odd-one-out"]
    options: list[str]
    correct_index: int | None = None


class TrueFalseOut(BaseExerciseOut):
    type: Literal["true-false"]
    correct_value: bool | None = None


class ImageOut(BaseExerciseOut):
    type: Literal["image"]
    image_url: str | None = None
    image_label: str
    image_color: str
    options: list[str]
    correct_index: int | None = None


class MatchPairOut(BaseModel):
    left: str
    right: str


class MatchOut(BaseExerciseOut):
    type: Literal["match"]
    pairs: list[MatchPairOut]


class MapHotspotOut(BaseModel):
    key: str
    label: str
    longitude: float
    latitude: float
    is_correct: bool | None = None


class MapClickOut(BaseExerciseOut):
    type: Literal["map-click"]
    map_region: str  # e.g. "world", "japan", "europe"
    hotspots: list[MapHotspotOut]


class ChronoItemOut(BaseModel):
    key: str
    label: str
    year: int
    correct_position: int | None = None


class ChronologicalOut(BaseExerciseOut):
    type: Literal["chronological"]
    items: list[ChronoItemOut]


class EstimationOut(BaseExerciseOut):
    type: Literal["estimation"]
    unit: str
    min_val: float
    max_val: float
    step: float
    default_value: float
    correct_value: float | None = None
    tolerance: float | None = None


ExerciseOut = Annotated[
    MultipleChoiceOut
    | OddOneOutOut
    | TrueFalseOut
    | ImageOut
    | MatchOut
    | MapClickOut
    | ChronologicalOut
    | EstimationOut,
    Field(discriminator="type"),
]
