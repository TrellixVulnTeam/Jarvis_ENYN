from typing import Type

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.connection.abstract_database_connection import Schema, Model, AbstractDataBaseConnection
from src.database.schemas.routines import RoutineSchema, routine_to_schema, schema_to_routine
from src.models.routine import Routine


class RoutineInterface(AbstractDataBaseConnection[Routine, RoutineSchema]):
    @staticmethod
    def _schema_to_model(model_schema: Schema) -> Model:
        return schema_to_routine(model_schema)

    @staticmethod
    def _model_to_schema(model: Model) -> Schema:
        return routine_to_schema(model)

    def get_by_id(self, model_id: int) -> Model:
        raise NotImplemented

    def get_by_name(self, model_name: str) -> Routine:
        model_schema: Schema
        with Session(self.engine) as session:
            stmt = select(self._get_schema_type()).where(self._get_schema_type().name == model_name)
            model_schema = session.execute(stmt).scalars().first()
            return self._schema_to_model(model_schema)

    @staticmethod
    def _get_model_id(model: Model) -> int:
        return -1

    @staticmethod
    def _get_model_type() -> Type[Model]:
        return Routine

    @staticmethod
    def _get_schema_type() -> Type[Schema]:
        return RoutineSchema

    def __int__(self) -> None:
        super().__init__()
        from src.database.tables.routines import create_tables
        create_tables(self.engine)
