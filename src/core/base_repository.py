from __future__ import annotations

from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.base_model import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, id: UUID) -> ModelType | None:
        return self.db.get(self.model, id)

    def get_by_id_or_raise(self, id: UUID) -> ModelType:
        instance = self.get_by_id(id)
        if not instance:
            raise ValueError(f"{self.model.__name__} {id} not found")
        return instance

    def get_by_attributes(self, **filters) -> ModelType | None:
        stmt = select(self.model).filter_by(**filters)
        return self.db.scalars(stmt).first()

    def get_all_by_attributes(self, **filters) -> list[ModelType]:
        stmt = select(self.model).filter_by(**filters)
        return list(self.db.scalars(stmt).all())

    def get_all(self) -> list[ModelType]:
        stmt = select(self.model)
        return list(self.db.scalars(stmt).all())

    def create(self, data: dict) -> ModelType:
        instance = self.model(**data)
        self.db.add(instance)
        self.db.flush()
        self.db.refresh(instance)
        return instance

    def create_bulk(self, data_list: list[dict]) -> list[ModelType]:
        instances = [self.model(**data) for data in data_list]
        self.db.add_all(instances)
        self.db.flush()
        return instances

    def update(self, id: UUID, data: dict) -> ModelType:
        instance = self.get_by_id_or_raise(id)
        for key, value in data.items():
            setattr(instance, key, value)
        self.db.flush()
        self.db.refresh(instance)
        return instance

    def delete(self, id: UUID) -> None:
        instance = self.get_by_id_or_raise(id)
        self.db.delete(instance)
        self.db.flush()

    def delete_bulk(self, ids: list[UUID]) -> None:
        for id in ids:
            self.delete(id)

    def upsert(self, lookup_fields: dict, create_data: dict) -> ModelType:
        instance = self.get_by_attributes(**lookup_fields)
        if instance:
            return self.update(instance.id, create_data)
        return self.create({**lookup_fields, **create_data})
