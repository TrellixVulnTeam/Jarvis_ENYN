from src.speechassistant.database.database_connection import DataBase
from src.speechassistant.models.user import User


class Users:
    def __init__(self) -> None:
        self.user_interface = DataBase.get_instance().user_interface

    def get_user_list(self) -> list[User]:
        return self.user_interface.get_users()

    def add_user(
        self,
        alias: str,
        first_name: str,
        last_name: str,
        birthday: dict,
        messenger_id: int,
        song_id: int = 1,
    ) -> None:
        self.user_interface.add_user(
            alias, first_name, last_name, birthday, messenger_id, song_id
        )

    def get_user_by_name(self, name: str) -> User:
        return self.user_interface.get_user(name)

    def get_user_by_id(self, user_id: int) -> User:
        return self.user_interface.get_user(user_id)

    def get_user_by_messenger_id(self, messenger_id: int) -> User:
        return self.user_interface.get_user_by_messenger_id(messenger_id)
