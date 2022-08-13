from sqlalchemy import Table, Column, Integer, DateTime, String, MetaData
from sqlalchemy.future import Engine

meta = MetaData()

REMINDER_TABLE_NAME = "reminder"

reminderTable = Table(
    REMINDER_TABLE_NAME,
    meta,
    Column("id", Integer),
    Column("time", DateTime),
    Column("text", String),
    Column("user_id", Integer),
)


def create_tables(engine: Engine):
    meta.create_all(engine)
