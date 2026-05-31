import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.core.base_repository import BaseRepository
from src.modules.answers.models.answer import AnswerModel
from src.modules.answers.models.answer_chrono import AnswerChronoModel
from src.modules.answers.models.answer_estimation import AnswerEstimationModel
from src.modules.answers.models.answer_image import AnswerImageModel
from src.modules.answers.models.answer_map import AnswerMapModel
from src.modules.answers.models.answer_match import AnswerMatchModel
from src.modules.answers.models.answer_mc import AnswerMCModel
from src.modules.answers.models.answer_tf import AnswerTFModel


_DETAIL_MODEL_MAP = {
    "multiple-choice": AnswerMCModel,
    "odd-one-out": AnswerMCModel,
    "true-false": AnswerTFModel,
    "image": AnswerImageModel,
    "match": AnswerMatchModel,
    "map-click": AnswerMapModel,
    "chronological": AnswerChronoModel,
    "estimation": AnswerEstimationModel,
}


class AnswerRepository(BaseRepository[AnswerModel]):
    def __init__(self, db: Session):
        super().__init__(AnswerModel, db)

    def save_with_detail(
        self, answer_data: dict, detail_data: dict, exercise_type: str
    ) -> AnswerModel:
        answer = self.create(answer_data)
        detail_model = _DETAIL_MODEL_MAP[exercise_type]
        self.db.add(detail_model(answer_id=answer.id, **detail_data))
        self.db.flush()
        return answer

    def get_user_stats(self, user_id: uuid.UUID) -> tuple[int, int]:
        """Returns (correct, total) answers for a user across all sessions."""
        total = self.db.scalar(
            select(func.count()).where(AnswerModel.user_id == user_id)
        ) or 0
        correct = self.db.scalar(
            select(func.count()).where(
                AnswerModel.user_id == user_id,
                AnswerModel.correct == True,  # noqa: E712
            )
        ) or 0
        return correct, total

    def get_session_stats(self, session_id: uuid.UUID) -> tuple[int, int]:
        total = self.db.scalar(
            select(func.count()).where(AnswerModel.session_id == session_id)
        ) or 0
        correct = self.db.scalar(
            select(func.count()).where(
                AnswerModel.session_id == session_id,
                AnswerModel.correct == True,  # noqa: E712
            )
        ) or 0
        return correct, total
