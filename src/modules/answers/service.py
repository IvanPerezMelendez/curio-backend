import uuid
from typing import Any

from src.modules.answers.models.answer import AnswerModel
from src.modules.answers.repository import AnswerRepository
from src.modules.content.models.exercise import ExerciseModel


class AnswerService:
    def __init__(self, repository: AnswerRepository):
        self.repository = repository

    def check_and_save(
        self,
        session_id: uuid.UUID,
        user_id: uuid.UUID,
        exercise: ExerciseModel,
        detail: Any,
        answer: Any,          # typed answer payload from SubmitXAnswerIn.answer
        ms_to_answer: int | None,
    ) -> tuple[AnswerModel, bool]:
        correct = self._check(exercise.type, detail, answer)

        saved = self.repository.save_with_detail(
            answer_data={
                "user_id": user_id,
                "exercise_id": exercise.id,
                "exercise_type": exercise.type,
                "session_id": session_id,
                "correct": correct,
                "ms_to_answer": ms_to_answer,
            },
            detail_data=self._detail_data(exercise.type, answer),
            exercise_type=exercise.type,
        )
        return saved, correct

    def get_session_stats(self, session_id: uuid.UUID) -> tuple[int, int]:
        return self.repository.get_session_stats(session_id)

    def get_user_stats(self, user_id: uuid.UUID) -> tuple[int, int]:
        return self.repository.get_user_stats(user_id)

    # ------------------------------------------------------------------

    def _check(self, exercise_type: str, detail: Any, answer: Any) -> bool:
        if exercise_type in ("multiple-choice", "odd-one-out", "image"):
            return answer.picked_index == detail.correct_index

        if exercise_type == "true-false":
            return answer.picked_value == detail.correct

        if exercise_type == "match":
            n = len(detail)
            paired = dict(zip(answer.left_indices, answer.right_indices))
            return all(paired.get(i) == i for i in range(n))

        if exercise_type == "map-click":
            correct_key = next(
                (h.hotspot_key for h in detail if h.is_correct), None
            )
            return answer.picked_hotspot_key == correct_key

        if exercise_type == "chronological":
            correct_order = [
                item.item_key for item in sorted(detail, key=lambda x: x.year)
            ]
            return answer.submitted_order == correct_order

        if exercise_type == "estimation":
            if detail.correct == 0:
                return answer.submitted_value == 0
            return (
                abs(answer.submitted_value - detail.correct) / abs(detail.correct)
                <= detail.tolerance
            )

        return False

    def _detail_data(self, exercise_type: str, answer: Any) -> dict:
        if exercise_type in ("multiple-choice", "odd-one-out", "image"):
            return {"picked_index": answer.picked_index}
        if exercise_type == "true-false":
            return {"picked_value": answer.picked_value}
        if exercise_type == "match":
            return {
                "left_indices": answer.left_indices,
                "right_indices": answer.right_indices,
            }
        if exercise_type == "map-click":
            return {"picked_hotspot_key": answer.picked_hotspot_key}
        if exercise_type == "chronological":
            return {"submitted_order": answer.submitted_order}
        if exercise_type == "estimation":
            return {"submitted_value": answer.submitted_value}
        return {}
