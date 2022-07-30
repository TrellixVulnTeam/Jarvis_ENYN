from sqlalchemy import Table, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

USER_TABLE_NAME = "users"
WAITING_NOTIFICATIONS_TABLE_NAME = "waitingnotifications"

waitingNotificationsTable = Table(
    WAITING_NOTIFICATIONS_TABLE_NAME,
    Base.metadata,
    Column("text", String),
    Column("user_id", Integer)
)

userTable = Table(
    USER_TABLE_NAME,
    Base.metadata,
    Column("id", Integer),
    Column("alias", String),
    Column("first_name", String),
    Column("last_name", String),
    Column("birthday", DateTime),
    Column("messenger_id", Integer),
    Column("song_name", String)
)
