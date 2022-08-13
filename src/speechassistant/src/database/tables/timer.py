from sqlalchemy import Table, Column, Integer, String, Time, MetaData, BigInteger
from sqlalchemy.future import Engine

meta = MetaData()

TIMER_TABLE_NAME = "timer"

timerTable = Table(
    TIMER_TABLE_NAME,
    meta,
    Column("id", Integer),
    Column("duration", BigInteger),
    Column("start_time", Time),
    Column("text", String),
)


def create_tables(engine: Engine):
    meta.create_all(engine)
