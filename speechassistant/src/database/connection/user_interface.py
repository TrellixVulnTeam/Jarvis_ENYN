from typing import Type

from src.database.connection.abstract_database_connection import Schema, Model, AbstractDataBaseConnection
from src.database.schemas.users import UserSchema, user_to_schema, schema_to_user
from src.models.user import User


class UserInterface(AbstractDataBaseConnection[User, UserSchema]):
    @staticmethod
    def schema_to_model(model_schema: Schema) -> Model:
        return schema_to_user(model_schema)

    @staticmethod
    def model_to_schema(model: Model) -> Schema:
        return user_to_schema(model)

    @staticmethod
    def get_model_id(model: User) -> int:
        return model.uid

    @staticmethod
    def get_model_type() -> Type[Model]:
        return User

    @staticmethod
    def get_schema_type() -> Type[Schema]:
        return UserSchema

    def __int__(self) -> None:
        super().__init__()
        from src.database.tables.users import create_tables
        create_tables(self.engine)
