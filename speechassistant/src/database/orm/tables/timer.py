from sqlalchemy import Table, Column, Integer, String, Time, BigInteger

from src.database.orm.database_persistency import OrmPersistency

DB_PERSISTENCY = OrmPersistency.get_instance()

TIMER_TABLE_NAME = "timer"

timerTable = Table(
    TIMER_TABLE_NAME,
    DB_PERSISTENCY.meta,
    Column("id", Integer),
    Column("duration", BigInteger),
    Column("start_time", Time),
    Column("text", String),
)
