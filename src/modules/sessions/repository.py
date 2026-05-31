import uuid
from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.core.base_repository import BaseRepository
from src.modules.content.models.subtopic import SubtopicModel
from src.modules.content.models.topic import TopicModel
from src.modules.sessions.models.session import SessionModel


class SessionRepository(BaseRepository[SessionModel]):
    def __init__(self, db: Session):
        super().__init__(SessionModel, db)

    def get_today_session(
        self, user_id: uuid.UUID, today: date
    ) -> SessionModel | None:
        return self.get_by_attributes(user_id=user_id, date=today)

    def get_completed_subtopic_ids(self, user_id: uuid.UUID) -> set[uuid.UUID]:
        stmt = select(SessionModel.subtopic_id).where(
            SessionModel.user_id == user_id,
            SessionModel.completed_at.is_not(None),
        )
        return set(self.db.scalars(stmt).all())

    def get_completed_counts_by_category(
        self, user_id: uuid.UUID
    ) -> dict[uuid.UUID, int]:
        stmt = (
            select(TopicModel.category_id, func.count(SessionModel.id).label("cnt"))
            .join(SubtopicModel, SessionModel.subtopic_id == SubtopicModel.id)
            .join(TopicModel, SubtopicModel.topic_id == TopicModel.id)
            .where(
                SessionModel.user_id == user_id,
                SessionModel.completed_at.is_not(None),
            )
            .group_by(TopicModel.category_id)
        )
        return {row.category_id: row.cnt for row in self.db.execute(stmt).all()}

    def get_total_completed(self, user_id: uuid.UUID) -> int:
        return self.db.scalar(
            select(func.count()).where(
                SessionModel.user_id == user_id,
                SessionModel.completed_at.is_not(None),
            )
        ) or 0

    def get_oldest_completed_subtopic_id_in_category(
        self, user_id: uuid.UUID, category_id: uuid.UUID
    ) -> uuid.UUID | None:
        stmt = (
            select(SessionModel.subtopic_id)
            .join(SubtopicModel, SessionModel.subtopic_id == SubtopicModel.id)
            .join(TopicModel, SubtopicModel.topic_id == TopicModel.id)
            .where(
                SessionModel.user_id == user_id,
                TopicModel.category_id == category_id,
                SessionModel.completed_at.is_not(None),
            )
            .order_by(SessionModel.completed_at.asc())
            .limit(1)
        )
        return self.db.scalars(stmt).first()
