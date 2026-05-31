from __future__ import annotations

from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel

from src.core.base_model import BaseModel as DBModel
from src.core.base_repository import BaseRepository

ModelType      = TypeVar("ModelType", bound=DBModel)
RepositoryType = TypeVar("RepositoryType", bound=BaseRepository)
CreateSchType  = TypeVar("CreateSchType", bound=BaseModel)
UpdateSchType  = TypeVar("UpdateSchType", bound=BaseModel)


class BaseService(Generic[ModelType, RepositoryType, CreateSchType, UpdateSchType]):
    def __init__(self, repository: RepositoryType):
        self.repository = repository

    def get_by_id(self, id: UUID) -> ModelType | None:
        return self.repository.get_by_id(id)

    def get_by_id_or_raise(self, id: UUID) -> ModelType:
        return self.repository.get_by_id_or_raise(id)

    def get_by_attributes(self, **filters) -> ModelType | None:
        return self.repository.get_by_attributes(**filters)

    def get_all_by_attributes(self, **filters) -> list[ModelType]:
        return self.repository.get_all_by_attributes(**filters)

    def get_all(self) -> list[ModelType]:
        return self.repository.get_all()

    def create(self, schema: CreateSchType) -> ModelType:
        return self.repository.create(schema.model_dump())

    def create_bulk(self, schemas: list[CreateSchType]) -> list[ModelType]:
        return self.repository.create_bulk([s.model_dump() for s in schemas])

    def update(self, id: UUID, schema: UpdateSchType) -> ModelType:
        return self.repository.update(id, schema.model_dump(exclude_unset=True))

    def delete(self, id: UUID) -> None:
        self.repository.delete(id)

    def delete_bulk(self, ids: list[UUID]) -> None:
        self.repository.delete_bulk(ids)

    def upsert(self, lookup_fields: dict, create_schema: CreateSchType) -> ModelType:
        return self.repository.upsert(lookup_fields, create_schema.model_dump())
