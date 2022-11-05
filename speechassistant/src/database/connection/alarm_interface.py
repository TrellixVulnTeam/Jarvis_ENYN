from typing import Type

from src.database.connection.abstract_database_connection import (
    Model,
    Schema,
    AbstractDataBaseConnection,
)
from src.database.schemas.alarms import alarm_to_schema, AlarmSchema, schema_to_alarm
from src.models.alarm import Alarm


class AlarmInterface(AbstractDataBaseConnection[Alarm, AlarmSchema]):
    @staticmethod
    def _get_schema_type() -> Type[Schema]:
        return AlarmSchema

    @staticmethod
    def _get_model_type() -> Type[Model]:
        return Alarm

    @staticmethod
    def _schema_to_model(model_schema: AlarmSchema) -> Alarm:
        return schema_to_alarm(model_schema)

    @staticmethod
    def _model_to_schema(model: Alarm) -> AlarmSchema:
        return alarm_to_schema(model)

    @staticmethod
    def _get_model_id(model: Alarm) -> int:
        return model.alarm_id

    def __init__(self):
        super().__init__()
