from typing import Type

from src.database.connection.abstract_database_connection import (
    AbstractDataBaseConnection,
    Schema,
    Model,
)
from src.database.schemas.birthdays import (
    schema_to_birthday,
    birthday_to_schema,
    BirthdaySchema,
)
from src.models.birthday import Birthday


class BirthdayInterface(AbstractDataBaseConnection[Birthday, BirthdaySchema]):
    @staticmethod
    def _schema_to_model(model_schema: Schema) -> Model:
        return schema_to_birthday(model_schema)

    @staticmethod
    def _model_to_schema(model: Model) -> Schema:
        return birthday_to_schema(model)

    @staticmethod
    def _get_model_id(model: Birthday) -> int:
        return -1

    @staticmethod
    def _get_model_type() -> Type[Model]:
        return Birthday

    @staticmethod
    def _get_schema_type() -> Type[Schema]:
        return BirthdaySchema

    def __int__(self) -> None:
        super().__init__()
