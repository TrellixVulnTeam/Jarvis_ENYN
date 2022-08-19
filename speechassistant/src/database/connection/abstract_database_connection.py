from abc import ABC, abstractmethod
from typing import Generic, Optional, Type, TypeVar

from sqlalchemy import create_engine, select, MetaData
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from src.database.database_persistency import DBPersistency

Model = TypeVar("Model")
Schema = TypeVar("Schema")


class AbstractDataBaseConnection(ABC, Generic[Model, Schema]):
    # Model == model
    # Schema == schema

    # typing maybe with typevar

    def __init__(self):
        self.meta = MetaData()
        self.engine = create_engine(
            DBPersistency.DATABASE_URL,
            echo=False,
            future=True,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )

        self.Session = sessionmaker(autocommit=True, autoflush=True, bind=self.engine)

    def create(self, model: Model) -> Model:
        result_model: Model
        with Session(self.engine, future=True) as session:
            model_schema: Schema = self.model_to_schema(model)
            session.add(model_schema)
            session.flush()
            result_model = self.schema_to_model(model_schema)
            session.commit()
        return result_model

    def get_by_id(self, model_id: int) -> Model:
        model_schema: Schema
        with Session(self.engine) as session:
            stmt = select(self.get_schema_type()).where(
                self.get_schema_type().id == model_id
            )
            model_schema = session.execute(stmt).scalars().first()
            return self.schema_to_model(model_schema)

    def get_all(self) -> list[Model]:
        with Session(self.engine) as session:
            stmt = select(self.get_schema_type())
            return [self.schema_to_model(a) for a in session.execute(stmt).scalars().all()]

    def update(self, updated_model: Model) -> Model:
        return self.update_by_id(self.get_model_id(updated_model), updated_model)

    def update_by_id(self, model_id: int, model: Model) -> Optional[Model]:
        result_model: Optional[Model]
        with Session(self.engine) as session:
            model_in_db: Schema = session.get(self.get_schema_type(), model_id)
            model_in_db = self.model_to_schema(model)
            session.flush()
            result_model = self.schema_to_model(model_in_db)
            session.commit()
        return result_model

    def delete_by_id(self, model_id: int) -> None:
        # todo: return count of deleted items
        with Session(self.engine) as session:
            model_in_db = session.get(self.get_schema_type(), model_id)
            session.delete(model_in_db)
            session.commit()

    @staticmethod
    @abstractmethod
    def schema_to_model(model_schema: Schema) -> Model:
        ...

    @staticmethod
    @abstractmethod
    def model_to_schema(model: Model) -> Schema:
        ...

    @staticmethod
    @abstractmethod
    def get_model_id(model: Model) -> int:
        ...

    @staticmethod
    @abstractmethod
    def get_model_type() -> Type[Model]:
        ...

    @staticmethod
    @abstractmethod
    def get_schema_type() -> Type[Schema]:
        ...
