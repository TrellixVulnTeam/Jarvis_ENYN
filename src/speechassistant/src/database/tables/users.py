from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData
from sqlalchemy.future import Engine

meta = MetaData()

USER_TABLE_NAME = "users"
WAITING_NOTIFICATIONS_TABLE_NAME = "waitingnotifications"

waitingNotificationsTable = Table(
    WAITING_NOTIFICATIONS_TABLE_NAME,
    meta,
    Column("text", String),
    Column("user_id", Integer),
)

userTable = Table(
    USER_TABLE_NAME,
    meta,
    Column("id", Integer),
    Column("alias", String),
    Column("first_name", String),
    Column("last_name", String),
    Column("birthday", DateTime),
    Column("messenger_id", Integer),
    Column("song_name", String),
)


def create_tables(engine: Engine):
    meta.create_all(engine)
