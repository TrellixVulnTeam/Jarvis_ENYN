from sqlalchemy import Table, Column, Integer, String, Time, BigInteger

from database.database_persistency import DBPersistency

DB_PERSISTENCY = DBPersistency.get_instance()

TIMER_TABLE_NAME = "timer"

timerTable = Table(
    TIMER_TABLE_NAME,
    DB_PERSISTENCY.meta,
    Column("id", Integer),
    Column("duration", BigInteger),
    Column("start_time", Time),
    Column("text", String),
)
