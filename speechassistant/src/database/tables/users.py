from sqlalchemy import Table, Column, Integer, String, DateTime

from database.database_persistency import DBPersistency

DB_PERSISTENCY = DBPersistency.get_instance()

USER_TABLE_NAME = "users"
WAITING_NOTIFICATIONS_TABLE_NAME = "waitingnotifications"

waitingNotificationsTable = Table(
    WAITING_NOTIFICATIONS_TABLE_NAME,
    DB_PERSISTENCY.meta,
    Column("text", String),
    Column("user_id", Integer),
)

userTable = Table(
    USER_TABLE_NAME,
    DB_PERSISTENCY.meta,
    Column("id", Integer, primary_key=True),
    Column("alias", String),
    Column("first_name", String),
    Column("last_name", String),
    Column("birthday", DateTime),
    Column("messenger_id", Integer),
    Column("song_name", String),
)
