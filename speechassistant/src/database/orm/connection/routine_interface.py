from typing import Type

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.orm.connection.abstract_database_connection import (
    Schema,
    Model,
    AbstractDataBaseConnection,
)
from src.database.orm.schemas.routines import (
    RoutineSchema,
    routine_to_schema,
    schema_to_routine,
    CallingCommandSchema,
)
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
        with Session(self.db_persistancy.engine) as session:
            stmt = select(RoutineSchema).where(RoutineSchema.name == model_name)
            model_schema = session.scalars(stmt).first()
            return self._schema_to_model(model_schema)

    def get_all_after_alarm(self) -> list[Routine]:
        with Session(self.db_persistancy.engine) as session:
            stmt = select(RoutineSchema).where(RoutineSchema.retakes.times.after_alarm)
            return [
                self._schema_to_model(a) for a in session.execute(stmt).scalars().all()
            ]

    def get_all_on_command(self, text: str) -> list[Routine]:
        with Session(self.db_persistancy.engine) as session:
            stmt = (
                select(RoutineSchema)
                .join(RoutineSchema.calling_commands)
                .where(CallingCommandSchema.command == text)
            )
            return [
                self._schema_to_model(a) for a in session.execute(stmt).scalars().all()
            ]

    def get_by_attribute(self, attribute: str, value: any) -> list[Routine]:
        with Session(self.db_persistancy.engine) as session:
            stmt = select(self._get_schema_type()).where(
                RoutineSchema.__getattribute__(attribute) == value
            )
            return [
                self._schema_to_model(a) for a in session.execute(stmt).scalars().all()
            ]

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
