from abc import ABC, abstractmethod
from typing import Generic, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, Session

from src.database.database_persistency import DBPersistency
from src.exceptions import NoMatchingEntry

Model = TypeVar("Model")
Schema = TypeVar("Schema")


class AbstractDataBaseConnection(ABC, Generic[Model, Schema]):
    def __init__(self):
        self.db_persistancy = DBPersistency.get_instance()
        self.Session = sessionmaker(
            autocommit=True, autoflush=True, bind=self.db_persistancy.engine
        )

    def create(self, model: Model) -> Model:
        result_model: Model
        with Session(DBPersistency.get_instance().engine, future=True) as session:
            model_schema: Schema = self._model_to_schema(model)
            session.add(model_schema)
            session.flush()
            result_model = self._schema_to_model(model_schema)
            session.commit()
        return result_model

    def get_by_id(self, model_id: int) -> Model:
        model_schema: Schema
        with Session(self.db_persistancy.engine) as session:
            stmt = select(self._get_schema_type()).where(
                self._get_schema_type().id == model_id
            )
            model_schema = session.scalars(stmt).first()
            if model_schema is None:
                raise NoMatchingEntry()
            return self._schema_to_model(model_schema)

    def get_all(self) -> list[Model]:
        result_models: list[Model]
        with Session(self.db_persistancy.engine) as session:
            stmt = select(self._get_schema_type())
            result_models = [
                self._schema_to_model(a) for a in session.scalars(stmt).all()
            ]
        return result_models

    def update(self, updated_model: Model) -> Model:
        return self.update_by_id(self._get_model_id(updated_model), updated_model)

    def update_by_id(self, model_id: int, model: Model) -> Optional[Model]:
        result_model: Optional[Model]
        with Session(self.db_persistancy.engine) as session:
            model_in_db: Schema = session.get(self._get_schema_type(), model_id)
            model_in_db = self._model_to_schema(model)
            session.flush()
            result_model = self._schema_to_model(model_in_db)
            session.commit()
        return result_model

    def delete_by_id(self, model_id: int) -> None:
        with Session(self.db_persistancy.engine) as session:
            model_in_db = session.get(self._get_schema_type(), model_id)
            if model_in_db is None:
                raise NoMatchingEntry()
            session.delete(model_in_db)
            session.commit()

    @staticmethod
    @abstractmethod
    def _schema_to_model(model_schema: Schema) -> Model:
        ...

    @staticmethod
    @abstractmethod
    def _model_to_schema(model: Model) -> Schema:
        ...

    @staticmethod
    @abstractmethod
    def _get_model_id(model: Model) -> int:
        ...

    @staticmethod
    @abstractmethod
    def _get_model_type() -> Type[Model]:
        ...

    @staticmethod
    @abstractmethod
    def _get_schema_type() -> Type[Schema]:
        ...
