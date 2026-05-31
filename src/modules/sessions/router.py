import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.deps import CurrentUser
from src.database import get_db
from src.modules.answers.repository import AnswerRepository
from src.modules.answers.service import AnswerService
from src.modules.content.repository import ContentRepository
from src.modules.content.service import ContentService
from src.modules.sessions.repository import SessionRepository
from src.modules.sessions.schemas import (
    CompleteSessionOut,
    SessionTodayOut,
    SubmitAnswerIn,
    SubmitAnswerOut,
)
from src.modules.sessions.service import SessionService
from src.modules.users.repository import UserRepository
from src.modules.users.service import UserService

router = APIRouter(prefix="/sessions", tags=["sessions"])


def _service(db: Session = Depends(get_db)) -> SessionService:
    return SessionService(
        repository=SessionRepository(db),
        user_service=UserService(UserRepository(db)),
        content_service=ContentService(ContentRepository(db)),
        answer_service=AnswerService(AnswerRepository(db)),
    )


@router.get(
    "/today",
    response_model=SessionTodayOut,
    summary="Get today's session",
    description=(
        "Returns the session assigned for today based on category rotation. "
        "If the user already completed today's session, returns `already_done: true` "
        "with correct answers revealed for review."
    ),
)
async def get_today_session(
    current_user: CurrentUser,
    service: SessionService = Depends(_service),
) -> SessionTodayOut:
    return service.get_today_session(current_user.id)


@router.post(
    "/{session_id}/answers",
    response_model=SubmitAnswerOut,
    summary="Submit an answer",
    description=(
        "Called once per exercise after the user picks their answer. "
        "The `exercise_type` field discriminates the answer payload shape."
    ),
)
async def submit_answer(
    session_id: uuid.UUID,
    body: SubmitAnswerIn,
    current_user: CurrentUser,
    service: SessionService = Depends(_service),
) -> SubmitAnswerOut:
    return service.submit_answer(session_id, current_user.id, body)


@router.post(
    "/{session_id}/complete",
    response_model=CompleteSessionOut,
    summary="Complete session",
    description=(
        "Marks the session as done, updates the streak, and returns final stats. "
        "Call this after all exercises are answered."
    ),
)
async def complete_session(
    session_id: uuid.UUID,
    current_user: CurrentUser,
    service: SessionService = Depends(_service),
) -> CompleteSessionOut:
    return service.complete_session(session_id, current_user.id)
