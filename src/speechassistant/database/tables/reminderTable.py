from sqlalchemy import Table, Column, Integer, DateTime, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

REMINDER_TABLE_NAME = "reminder"

reminderTable = Table(
    REMINDER_TABLE_NAME,
    Base.metadata,
    Column("id", Integer),
    Column("time", DateTime),
    Column("text", String),
    Column("user_id", Integer)
)