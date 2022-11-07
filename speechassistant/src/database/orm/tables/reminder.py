from sqlalchemy import Table, Column, Integer, DateTime, String
from sqlalchemy.future import Engine

from src.database.orm.database_persistency import OrmPersistency

DB_PERSISTENCY = OrmPersistency.get_instance()

REMINDER_TABLE_NAME = "reminder"

reminderTable = Table(
    REMINDER_TABLE_NAME,
    DB_PERSISTENCY.meta,
    Column("id", Integer),
    Column("time", DateTime),
    Column("text", String),
    Column("user_id", Integer),
)


def create_tables(engine: Engine):
    DB_PERSISTENCY.meta.create_all(engine)
