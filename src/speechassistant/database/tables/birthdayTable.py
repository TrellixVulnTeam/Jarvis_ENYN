from sqlalchemy import Table, String, DateTime, Column
from sqlalchemy.orm import declarative_base

Base = declarative_base()

BIRTHDAY_TABLE_NAME = "birthdays"

birthdayTableName = Table(
    BIRTHDAY_TABLE_NAME,
    Base.metadata,
    Column("first_name", String),
    Column("last_name", String),
    Column("date", DateTime)
)
