import uuid
from datetime import date, datetime, timezone

from fastapi import HTTPException

from src.modules.answers.service import AnswerService
from src.modules.content.service import ContentService
from src.modules.sessions.models.session import SessionModel
from src.modules.sessions.repository import SessionRepository
from src.modules.sessions.schemas import (
    CategoryOut,
    CompleteSessionOut,
    SessionTodayOut,
    SubtopicOut,
    SubmitAnswerIn,
    SubmitAnswerOut,
    TopicOut,
)
from src.modules.users.service import UserService


class SessionService:
    def __init__(
        self,
        repository: SessionRepository,
        user_service: UserService,
        content_service: ContentService,
        answer_service: AnswerService,
    ):
        self.repository = repository
        self.user_service = user_service
        self.content_service = content_service
        self.answer_service = answer_service

    # ------------------------------------------------------------------
    # GET /sessions/today
    # ------------------------------------------------------------------

    def get_today_session(self, user_id: uuid.UUID) -> SessionTodayOut:
        user = self.user_service.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        today = date.today()
        existing = self.repository.get_today_session(user.id, today)

        if existing and existing.completed_at:
            return self._build_response(existing, user.streak_current, reveal_answers=True)

        subtopic = self._pick_subtopic_for_user(user.id)

        session = existing or self.repository.create({
            "user_id": user.id,
            "subtopic_id": subtopic.id,
            "date": today,
        })

        return self._build_response(session, user.streak_current, reveal_answers=False)

    def _pick_subtopic_for_user(self, user_id: uuid.UUID):
        all_categories = self.content_service.get_all_categories()
        if not all_categories:
            raise HTTPException(status_code=503, detail="No content available")

        counts = self.repository.get_completed_counts_by_category(user_id)
        target = min(all_categories, key=lambda c: (counts.get(c.id, 0), c.name))

        completed_ids = self.repository.get_completed_subtopic_ids(user_id)
        subtopic = self.content_service.get_next_subtopic(target.id, completed_ids)

        if not subtopic:
            oldest_id = self.repository.get_oldest_completed_subtopic_id_in_category(
                user_id, target.id
            )
            subtopic = self.content_service.get_subtopic(oldest_id) if oldest_id else None

        if not subtopic:
            raise HTTPException(status_code=503, detail="No sessions available")

        return subtopic

    def _build_response(
        self, session: SessionModel, streak_current: int, reveal_answers: bool
    ) -> SessionTodayOut:
        subtopic = self.content_service.get_subtopic(session.subtopic_id)
        topic = self.content_service.get_topic(subtopic.topic_id)
        category = self.content_service.get_category(topic.category_id)
        exercises = self.content_service.get_exercises_as_schemas(
            subtopic.id, reveal_answers
        )

        return SessionTodayOut(
            already_done=reveal_answers,
            session_id=session.id,
            streak_current=streak_current,
            completed_at=session.completed_at,
            category=CategoryOut(id=category.id, name=category.name),
            topic=TopicOut(id=topic.id, name=topic.name),
            subtopic=SubtopicOut(
                id=subtopic.id, name=subtopic.name, subtitle=subtopic.subtitle
            ),
            exercises=exercises,
        )

    # ------------------------------------------------------------------
    # POST /sessions/{session_id}/answers
    # ------------------------------------------------------------------

    def submit_answer(
        self,
        session_id: uuid.UUID,
        user_id: uuid.UUID,
        body: SubmitAnswerIn,
    ) -> SubmitAnswerOut:
        user, session = self._resolve(user_id, session_id)

        if session.completed_at:
            raise HTTPException(status_code=409, detail="Session already completed")

        result = self.content_service.get_exercise_with_detail(body.exercise_id)
        if not result:
            raise HTTPException(status_code=404, detail="Exercise not found")
        exercise, detail = result

        _, correct = self.answer_service.check_and_save(
            session_id=session.id,
            user_id=user.id,
            exercise=exercise,
            detail=detail,
            answer=body.answer,
            ms_to_answer=body.ms_to_answer,
        )

        return SubmitAnswerOut(correct=correct)

    # ------------------------------------------------------------------
    # POST /sessions/{session_id}/complete
    # ------------------------------------------------------------------

    def complete_session(
        self, session_id: uuid.UUID, user_id: uuid.UUID
    ) -> CompleteSessionOut:
        user, session = self._resolve(user_id, session_id)

        if session.completed_at:
            raise HTTPException(status_code=409, detail="Session already completed")

        now = datetime.now(timezone.utc)
        duration_ms = (
            int((now - session.created_at).total_seconds() * 1000)
            if session.created_at
            else None
        )

        self.repository.update(session.id, {"completed_at": now, "duration_ms": duration_ms})
        updated_user = self.user_service.update_streak(user, date.today())
        correct, total = self.answer_service.get_session_stats(session.id)

        return CompleteSessionOut(
            streak_current=updated_user.streak_current,
            streak_longest=updated_user.streak_longest,
            correct=correct,
            total=total,
            duration_ms=duration_ms,
        )

    # ------------------------------------------------------------------

    def _resolve(self, user_id: uuid.UUID, session_id: uuid.UUID):
        user = self.user_service.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        session = self.repository.get_by_id(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        if session.user_id != user.id:
            raise HTTPException(status_code=403, detail="Forbidden")

        return user, session
