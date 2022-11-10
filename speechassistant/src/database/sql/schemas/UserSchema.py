from datetime import date

from database.orm.schemas.users import WaitingNotification
from database.sql.schemas.AbstractSchema import AbstractSchema
from models import User


class UserSchema(AbstractSchema):
    def __init__(
        self,
        _id: int,
        alias: str,
        first_name: str,
        last_name: str,
        birthday: date,
        messenger_id: int,
        default_song_name: str,
    ):
        self.id = _id
        self.alias = alias
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.messenger_id = messenger_id
        self.default_song_name = default_song_name

    def to_model(self, waiting_notifications: list[WaitingNotification]) -> User:
        return User(
            alias=self.alias,
            first_name=self.first_name,
            last_name=self.last_name,
            birthday=self.birthday,
            messenger_id=self.messenger_id,
            song_name=self.default_song_name,
            waiting_notifications=waiting_notifications,
            uid=self.id,
        )

    @staticmethod
    def from_model(model: User, **kwargs) -> "UserSchema":
        return UserSchema(
            _id=model.uid,
            alias=model.alias,
            first_name=model.first_name,
            last_name=model.last_name,
            birthday=model.birthday,
            messenger_id=model.messenger_id,
            default_song_name=model.song_name,
        )

    def __repr__(self) -> str:
        return f"UserSchema(id: {self.id}, alias: {self.alias}, first_name: {self.first_name}, last_name: {self.last_name}, birthday: {self.birthday}, messenger_id: {self.messenger_id}, defualt_song_name: {self.default_song_name}) "
