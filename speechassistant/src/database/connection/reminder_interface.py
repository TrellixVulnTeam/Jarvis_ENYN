from datetime import datetime
from typing import Type

from sqlalchemy.orm import Session

from src.database.connection.abstract_database_connection import Schema, Model, AbstractDataBaseConnection
from src.database.schemas.reminder import ReminderSchema, reminder_to_schema, schema_to_reminder
from src.exceptions import NoMatchingEntry
from src.models.reminder import Reminder


class ReminderInterface(AbstractDataBaseConnection[Reminder, ReminderSchema]):
    def delete_by_datetime(self, alarm_datetime: datetime) -> int:
        with Session(self.engine) as session:
            models_in_db: list[ReminderSchema] = session.load(self._get_schema_type()).where(
                ReminderSchema.time == alarm_datetime)
            if models_in_db is None:
                raise NoMatchingEntry()
            session.delete(models_in_db)
            session.commit()
        return len(models_in_db)

    @staticmethod
    def _schema_to_model(model_schema: Schema) -> Model:
        return schema_to_reminder(model_schema)

    @staticmethod
    def _model_to_schema(model: Model) -> Schema:
        return reminder_to_schema(model)

    @staticmethod
    def _get_model_id(model: Reminder) -> int:
        return model.reminder_id

    @staticmethod
    def _get_model_type() -> Type[Model]:
        return Reminder

    @staticmethod
    def _get_schema_type() -> Type[Schema]:
        return ReminderSchema

    def __int__(self) -> None:
        super().__init__()
        from src.database.tables.reminder import create_tables
        create_tables(self.engine)
