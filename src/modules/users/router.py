from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.deps import CurrentUser
from src.database import get_db
from src.modules.answers.repository import AnswerRepository
from src.modules.answers.service import AnswerService
from src.modules.content.repository import ContentRepository
from src.modules.content.service import ContentService
from src.modules.sessions.repository import SessionRepository
from src.modules.users.schemas import CategoryProgressOut, UserOut, UserStatsOut

router = APIRouter(prefix="/users", tags=["users"])


def _deps(db: Session = Depends(get_db)):
    return (
        SessionRepository(db),
        AnswerService(AnswerRepository(db)),
        ContentService(ContentRepository(db)),
    )


@router.get("/me", response_model=UserOut, summary="Get current user")
async def get_me(current_user: CurrentUser) -> UserOut:
    return UserOut(
        id=current_user.id,
        email=current_user.email,
        streak_current=current_user.streak_current,
        streak_longest=current_user.streak_longest,
        last_visit=current_user.last_visit,
        is_active=current_user.is_active,
    )


@router.get(
    "/me/stats",
    response_model=UserStatsOut,
    summary="Get current user statistics",
    description="Returns session counts, accuracy and per-category progress.",
)
async def get_me_stats(
    current_user: CurrentUser,
    deps=Depends(_deps),
) -> UserStatsOut:
    session_repo, answer_service, content_service = deps

    total_sessions = session_repo.get_total_completed(current_user.id)
    correct, total_exercises = answer_service.get_user_stats(current_user.id)
    accuracy = round(correct / total_exercises, 4) if total_exercises else 0.0

    counts_by_cat = session_repo.get_completed_counts_by_category(current_user.id)
    categories = content_service.get_all_categories()
    category_progress = [
        CategoryProgressOut(
            category_id=cat.id,
            category_name=cat.name,
            sessions_completed=counts_by_cat.get(cat.id, 0),
        )
        for cat in categories
    ]

    return UserStatsOut(
        total_sessions=total_sessions,
        total_exercises=total_exercises,
        correct_answers=correct,
        accuracy=accuracy,
        category_progress=category_progress,
    )
