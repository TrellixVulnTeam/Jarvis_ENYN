from backup.database_connection import DataBase
from src.models.user import User


class Users:
    def __init__(self) -> None:
        self.user_interface = DataBase().user_interface

    def get_user_list(self) -> list[User]:
        return self.user_interface.get_users()

    def add_user(self, new_user: User) -> None:
        self.user_interface.add_user(new_user)

    def get_user_by_name(self, name: str) -> User:
        return self.user_interface.get_user(name)

    def get_user_by_id(self, user_id: int) -> User:
        return self.user_interface.get_user(user_id)

    def get_user_by_messenger_id(self, messenger_id: int) -> User:
        return self.user_interface.get_user_by_messenger_id(messenger_id)
