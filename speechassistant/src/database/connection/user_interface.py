from typing import Type

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from src.database.connection.abstract_database_connection import (
    Schema,
    Model,
    AbstractDataBaseConnection,
)
from src.database.schemas.users import UserSchema, user_to_schema, schema_to_user
from src.models.user import User


class UserInterface(AbstractDataBaseConnection[User, UserSchema]):
    # toDo: load_by_name

    def get_user_by_alias(self, user_name: str) -> User:
        with Session(self.db_persistancy.engine) as session:
            stmt = select(UserSchema).where(UserSchema.alias == user_name)
            return self._schema_to_model(session.execute(stmt).scalars().first())

    @staticmethod
    def _schema_to_model(model_schema: Schema) -> Model:
        return schema_to_user(model_schema)

    @staticmethod
    def _model_to_schema(model: Model) -> Schema:
        return user_to_schema(model)

    @staticmethod
    def _get_model_id(model: User) -> int:
        return model.uid

    @staticmethod
    def _get_model_type() -> Type[Model]:
        return User

    @staticmethod
    def _get_schema_type() -> Type[Schema]:
        return UserSchema

    def __int__(self) -> None:
        super().__init__()
