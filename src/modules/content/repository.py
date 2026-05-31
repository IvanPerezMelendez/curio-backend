import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.modules.content.models.category import CategoryModel
from src.modules.content.models.exercise import ExerciseModel
from src.modules.content.models.exercise_chrono import ExerciseChronoItemModel
from src.modules.content.models.exercise_estimation import ExerciseEstimationModel
from src.modules.content.models.exercise_image import ExerciseImageModel
from src.modules.content.models.exercise_map import ExerciseMapConfigModel, ExerciseMapHotspotModel
from src.modules.content.models.exercise_match import ExerciseMatchPairModel
from src.modules.content.models.exercise_mc import ExerciseMCModel
from src.modules.content.models.exercise_tf import ExerciseTFModel
from src.modules.content.models.subtopic import SubtopicModel
from src.modules.content.models.topic import TopicModel


class ContentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_categories(self) -> list[CategoryModel]:
        return list(self.db.scalars(select(CategoryModel).order_by(CategoryModel.name)).all())

    def get_topics_by_category(self, category_id: uuid.UUID) -> list[TopicModel]:
        return list(
            self.db.scalars(
                select(TopicModel)
                .where(TopicModel.category_id == category_id)
                .order_by(TopicModel.name)
            ).all()
        )

    def get_subtopics_by_topic(self, topic_id: uuid.UUID) -> list[SubtopicModel]:
        return list(
            self.db.scalars(
                select(SubtopicModel)
                .where(SubtopicModel.topic_id == topic_id)
                .order_by(SubtopicModel.position)
            ).all()
        )

    def get_category_by_id(self, category_id: uuid.UUID) -> CategoryModel | None:
        return self.db.get(CategoryModel, category_id)

    def get_topic_by_id(self, topic_id: uuid.UUID) -> TopicModel | None:
        return self.db.get(TopicModel, topic_id)

    def get_subtopic_by_id(self, subtopic_id: uuid.UUID) -> SubtopicModel | None:
        return self.db.get(SubtopicModel, subtopic_id)

    def get_next_subtopic(
        self, category_id: uuid.UUID, completed_ids: set[uuid.UUID]
    ) -> SubtopicModel | None:
        stmt = (
            select(SubtopicModel)
            .join(TopicModel, SubtopicModel.topic_id == TopicModel.id)
            .where(TopicModel.category_id == category_id)
            .order_by(TopicModel.id, SubtopicModel.position)
            .limit(1)
        )
        if completed_ids:
            stmt = stmt.where(SubtopicModel.id.not_in(completed_ids))
        return self.db.scalars(stmt).first()

    def get_exercises_for_subtopic(
        self, subtopic_id: uuid.UUID
    ) -> list[tuple[ExerciseModel, Any]]:
        exercises = list(
            self.db.scalars(
                select(ExerciseModel).where(ExerciseModel.subtopic_id == subtopic_id)
            ).all()
        )
        return [(ex, self._load_detail(ex)) for ex in exercises]

    def get_exercise_with_detail(
        self, exercise_id: uuid.UUID
    ) -> tuple[ExerciseModel, Any] | None:
        exercise = self.db.get(ExerciseModel, exercise_id)
        if not exercise:
            return None
        return exercise, self._load_detail(exercise)

    def _load_detail(self, exercise: ExerciseModel) -> Any:
        eid = exercise.id
        t = exercise.type

        if t in ("multiple-choice", "odd-one-out"):
            return self.db.scalars(
                select(ExerciseMCModel).where(ExerciseMCModel.exercise_id == eid)
            ).first()
        if t == "true-false":
            return self.db.scalars(
                select(ExerciseTFModel).where(ExerciseTFModel.exercise_id == eid)
            ).first()
        if t == "image":
            return self.db.scalars(
                select(ExerciseImageModel).where(ExerciseImageModel.exercise_id == eid)
            ).first()
        if t == "estimation":
            return self.db.scalars(
                select(ExerciseEstimationModel).where(
                    ExerciseEstimationModel.exercise_id == eid
                )
            ).first()
        if t == "match":
            return list(
                self.db.scalars(
                    select(ExerciseMatchPairModel)
                    .where(ExerciseMatchPairModel.exercise_id == eid)
                    .order_by(ExerciseMatchPairModel.position)
                ).all()
            )
        if t == "map-click":
            config = self.db.scalars(
                select(ExerciseMapConfigModel).where(
                    ExerciseMapConfigModel.exercise_id == eid
                )
            ).first()
            hotspots = list(
                self.db.scalars(
                    select(ExerciseMapHotspotModel).where(
                        ExerciseMapHotspotModel.exercise_id == eid
                    )
                ).all()
            )
            return {"config": config, "hotspots": hotspots}
        if t == "chronological":
            return list(
                self.db.scalars(
                    select(ExerciseChronoItemModel)
                    .where(ExerciseChronoItemModel.exercise_id == eid)
                    .order_by(ExerciseChronoItemModel.position)
                ).all()
            )
        return None
