from typing import Type

from src.database.orm.connection.abstract_database_connection import (
    Schema,
    Model,
    AbstractDataBaseConnection,
)
from src.database.orm.schemas.timer import TimerSchema, timer_to_schema, schema_to_timer
from src.models.timer import Timer


class TimerInterface(AbstractDataBaseConnection[Timer, TimerSchema]):
    @staticmethod
    def _schema_to_model(model_schema: Schema) -> Model:
        return schema_to_timer(model_schema)

    @staticmethod
    def _model_to_schema(model: Model) -> Schema:
        return timer_to_schema(model)

    @staticmethod
    def _get_model_id(model: Timer) -> int:
        return Timer.tid

    @staticmethod
    def _get_model_type() -> Type[Model]:
        return Timer

    @staticmethod
    def _get_schema_type() -> Type[Schema]:
        return TimerSchema

    def __int__(self) -> None:
        super().__init__()
