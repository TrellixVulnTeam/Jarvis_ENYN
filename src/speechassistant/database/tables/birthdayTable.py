from sqlalchemy import Table, String, DateTime, Column, MetaData
from sqlalchemy.future import Engine

meta = MetaData()

BIRTHDAY_TABLE_NAME = "birthdays"

birthdayTableName = Table(
    BIRTHDAY_TABLE_NAME,
    meta,
    Column("first_name", String),
    Column("last_name", String),
    Column("date", DateTime),
)


def create_tables(engine: Engine):
    meta.create_all(engine)
