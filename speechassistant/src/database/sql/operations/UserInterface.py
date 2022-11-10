from database.AbstractInterfaces.AbstractUserInterface import AbstractUserInterface
from database.orm.schemas.users import UserSchema
from src.database.sql.operations.AbstractInterface import AbstractInterface
from src.database.sql.operations.AbstractOperations.AbstractLoadAll import (
    AbstractLoadAll,
)
from src.database.sql.operations.AbstractOperations.AbstractLoadById import (
    AbstractLoadById,
)
from src.database.sql.tables.UserTable import UserTable


class UserInterface(
    AbstractInterface,
    AbstractLoadById[UserTable, int, UserSchema],
    AbstractLoadAll[UserTable, UserSchema],
    AbstractUserInterface,
):
    def get_user_by_alias(self, alias: str):
        raise NotImplementedError
