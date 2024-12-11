from typing import TypeVar, Generic, Type

from sqlalchemy import Sequence
from sqlmodel import SQLModel, Session, select

TModel = TypeVar("TModel", bound=SQLModel)


# TCreateSchema = TypeVar("TCreateSchema", bound=SQLModel)


class BaseRepository(Generic[TModel]):
    def __init__(self, model: Type[TModel]):
        self.model = model

    def list(self, db: Session) -> Sequence[TModel]:
        return db.exec(select(self.model)).all()

    def get(self, db: Session, obj_id: int) -> TModel:
        return db.get(
            self.model,
            obj_id,
        )

    def create(self, db: Session, obj: TModel) -> TModel:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj: TModel) -> TModel:
        db.merge(obj)
        db.commit()
        return obj

    def delete(self, db: Session, obj: TModel) -> None:
        db.delete(obj)
        db.commit()
        db.flush()
