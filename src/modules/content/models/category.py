from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.core.base_model import BaseModel


class CategoryModel(BaseModel):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    lang: Mapped[str] = mapped_column(String(5), default="es", nullable=False)
