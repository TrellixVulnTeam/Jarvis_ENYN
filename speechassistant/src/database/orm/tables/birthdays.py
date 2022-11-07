from sqlalchemy import Table, String, DateTime, Column

from src.database.orm.database_persistency import OrmPersistency

DB_PERSISTENCY = OrmPersistency.get_instance()

BIRTHDAY_TABLE_NAME = "birthdays"

birthdayTableName = Table(
    BIRTHDAY_TABLE_NAME,
    DB_PERSISTENCY.meta,
    Column("first_name", String),
    Column("last_name", String),
    Column("date", DateTime),
)
