import uuid
from typing import Any

from src.modules.content.models.category import CategoryModel
from src.modules.content.models.exercise import ExerciseModel
from src.modules.content.models.subtopic import SubtopicModel
from src.modules.content.models.topic import TopicModel
from src.modules.content.repository import ContentRepository
from src.modules.content.schemas import (
    ChronoItemOut,
    ChronologicalOut,
    EstimationOut,
    ExerciseOut,
    ExplanationOut,
    ImageOut,
    MapClickOut,
    MapHotspotOut,
    MatchOut,
    MatchPairOut,
    MultipleChoiceOut,
    OddOneOutOut,
    TrueFalseOut,
)


class ContentService:
    def __init__(self, repository: ContentRepository):
        self.repository = repository

    def get_all_categories(self) -> list[CategoryModel]:
        return self.repository.get_all_categories()

    def get_topics_by_category(self, category_id: uuid.UUID) -> list[TopicModel]:
        return self.repository.get_topics_by_category(category_id)

    def get_subtopics_by_topic(self, topic_id: uuid.UUID) -> list[SubtopicModel]:
        return self.repository.get_subtopics_by_topic(topic_id)

    def get_category(self, category_id: uuid.UUID) -> CategoryModel | None:
        return self.repository.get_category_by_id(category_id)

    def get_topic(self, topic_id: uuid.UUID) -> TopicModel | None:
        return self.repository.get_topic_by_id(topic_id)

    def get_subtopic(self, subtopic_id: uuid.UUID) -> SubtopicModel | None:
        return self.repository.get_subtopic_by_id(subtopic_id)

    def get_next_subtopic(
        self, category_id: uuid.UUID, completed_ids: set[uuid.UUID]
    ) -> SubtopicModel | None:
        return self.repository.get_next_subtopic(category_id, completed_ids)

    def get_exercise_with_detail(
        self, exercise_id: uuid.UUID
    ) -> tuple[ExerciseModel, Any] | None:
        return self.repository.get_exercise_with_detail(exercise_id)

    def get_exercises_as_schemas(
        self, subtopic_id: uuid.UUID, reveal_answers: bool
    ) -> list[ExerciseOut]:
        pairs = self.repository.get_exercises_for_subtopic(subtopic_id)
        result = []
        for exercise, detail in pairs:
            schema = self._to_schema(exercise, detail, reveal_answers)
            if schema is not None:
                result.append(schema)
        return result

    def _explanation(self, exercise: ExerciseModel) -> ExplanationOut:
        return ExplanationOut(
            title=exercise.explanation_title,
            body=exercise.explanation_body,
            fact=exercise.explanation_fact,
        )

    def _base(self, exercise: ExerciseModel) -> dict:
        return {
            "id": exercise.id,
            "tag": exercise.tag,
            "question": exercise.question,
            "explanation": self._explanation(exercise),
        }

    def _to_schema(
        self, exercise: ExerciseModel, detail: Any, reveal_answers: bool
    ) -> ExerciseOut | None:
        base = self._base(exercise)
        t = exercise.type

        if t in ("multiple-choice", "odd-one-out"):
            cls = MultipleChoiceOut if t == "multiple-choice" else OddOneOutOut
            return cls(
                **base,
                type=t,
                options=list(detail.options),
                correct_index=detail.correct_index if reveal_answers else None,
            )

        if t == "true-false":
            return TrueFalseOut(
                **base,
                type="true-false",
                correct_value=detail.correct if reveal_answers else None,
            )

        if t == "image":
            return ImageOut(
                **base,
                type="image",
                image_url=detail.image_url,
                image_label=detail.image_label,
                image_color=detail.image_color,
                options=list(detail.options),
                correct_index=detail.correct_index if reveal_answers else None,
            )

        if t == "match":
            pairs = [MatchPairOut(left=p.left_text, right=p.right_text) for p in detail]
            return MatchOut(**base, type="match", pairs=pairs)

        if t == "map-click":
            config = detail["config"]
            hotspots = [
                MapHotspotOut(
                    key=h.hotspot_key,
                    label=h.label,
                    longitude=h.longitude,
                    latitude=h.latitude,
                    is_correct=h.is_correct if reveal_answers else None,
                )
                for h in detail["hotspots"]
            ]
            return MapClickOut(
                **base,
                type="map-click",
                map_region=config.map_region,
                hotspots=hotspots,
            )

        if t == "chronological":
            items = [
                ChronoItemOut(
                    key=i.item_key,
                    label=i.label,
                    year=i.year,
                    correct_position=i.position if reveal_answers else None,
                )
                for i in detail
            ]
            return ChronologicalOut(**base, type="chronological", items=items)

        if t == "estimation":
            return EstimationOut(
                **base,
                type="estimation",
                unit=detail.unit,
                min_val=detail.min_val,
                max_val=detail.max_val,
                step=detail.step,
                default_value=detail.default_value,
                correct_value=detail.correct if reveal_answers else None,
                tolerance=detail.tolerance if reveal_answers else None,
            )

        return None
