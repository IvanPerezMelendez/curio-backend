import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.deps import CurrentUser
from src.database import get_db
from src.modules.content.repository import ContentRepository
from src.modules.content.service import ContentService
from src.modules.content.schemas import ContentCategoryOut, ContentTopicOut, ContentSubtopicOut

router = APIRouter(prefix="/content", tags=["content"])


def _service(db: Session = Depends(get_db)) -> ContentService:
    return ContentService(ContentRepository(db))


@router.get(
    "/categories",
    response_model=list[ContentCategoryOut],
    summary="List all categories",
)
async def list_categories(
    _: CurrentUser,
    service: ContentService = Depends(_service),
) -> list[ContentCategoryOut]:
    cats = service.get_all_categories()
    return [ContentCategoryOut(id=c.id, name=c.name, description=c.description, lang=c.lang) for c in cats]


@router.get(
    "/categories/{category_id}/topics",
    response_model=list[ContentTopicOut],
    summary="List topics in a category",
)
async def list_topics(
    category_id: uuid.UUID,
    _: CurrentUser,
    service: ContentService = Depends(_service),
) -> list[ContentTopicOut]:
    cat = service.get_category(category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    topics = service.get_topics_by_category(category_id)
    return [ContentTopicOut(id=t.id, category_id=t.category_id, name=t.name, description=t.description) for t in topics]


@router.get(
    "/topics/{topic_id}/subtopics",
    response_model=list[ContentSubtopicOut],
    summary="List subtopics in a topic",
)
async def list_subtopics(
    topic_id: uuid.UUID,
    _: CurrentUser,
    service: ContentService = Depends(_service),
) -> list[ContentSubtopicOut]:
    topic = service.get_topic(topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    subtopics = service.get_subtopics_by_topic(topic_id)
    return [
        ContentSubtopicOut(id=s.id, topic_id=s.topic_id, name=s.name, subtitle=s.subtitle, position=s.position)
        for s in subtopics
    ]
