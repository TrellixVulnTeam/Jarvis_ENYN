from typing import Type

from src.database.connection.abstract_database_connection import Schema, Model, AbstractDataBaseConnection
from src.database.schemas.timer import TimerSchema, timer_to_schema, schema_to_timer
from src.models.timer import Timer


class TimerInterface(AbstractDataBaseConnection[Timer, TimerSchema]):
    @staticmethod
    def schema_to_model(model_schema: Schema) -> Model:
        return schema_to_timer(model_schema)

    @staticmethod
    def model_to_schema(model: Model) -> Schema:
        return timer_to_schema(model)

    @staticmethod
    def get_model_id(model: Timer) -> int:
        return Timer.tid

    @staticmethod
    def get_model_type() -> Type[Model]:
        return Timer

    @staticmethod
    def get_schema_type() -> Type[Schema]:
        return TimerSchema

    def __int__(self) -> None:
        super().__init__()
        from src.database.tables.timer import create_tables
        create_tables(self.engine)
