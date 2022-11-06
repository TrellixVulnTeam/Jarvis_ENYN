from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from src.models.user import User

Base = declarative_base()


class WaitingNotification(Base):
    __tablename__ = "waitingnotifications"
    text = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))


class UserSchema(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    alias = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    birthday = Column(Date)
    messenger_id = Column(Integer)
    song_name = Column(String)
    waiting_notifications = relationship(WaitingNotification, cascade="all, delete")


def __schema_to_waiting_notification_list(
    schema: list[WaitingNotification],
) -> list[str]:
    return [w.text for w in schema]


def __waiting_notification_list_to_schema(
    user_id: int, models: list[str]
) -> list[WaitingNotification]:
    return [WaitingNotification(user_id=user_id, text=w) for w in models]


def schema_to_user(schema: UserSchema) -> User | None:
    if not schema:
        return None
    return User(
        uid=schema.id,
        alias=schema.alias,
        first_name=schema.first_name,
        last_name=schema.last_name,
        birthday=schema.birthday,
        messenger_id=schema.messenger_id,
        song_name=schema.song_name,
        waiting_notifications=__schema_to_waiting_notification_list(
            schema.waiting_notifications
        ),
    )


def user_to_schema(model: User) -> UserSchema:
    return UserSchema(
        id=model.uid,
        alias=model.alias,
        first_name=model.first_name,
        last_name=model.last_name,
        birthday=model.birthday,
        messenger_id=model.messenger_id,
        song_name=model.song_name,
        waiting_notifications=__waiting_notification_list_to_schema(
            model.uid, model.waiting_notifications
        ),
    )
