from sqlalchemy import Table, Column, Integer, String, Time, MetaData
from sqlalchemy.future import Engine

meta = MetaData()

TIMER_TABLE_NAME = "timer"

timerTable = Table(
    TIMER_TABLE_NAME,
    meta,
    Column("id", Integer),
    Column("duration", String),
    Column("start_time", Time),
    Column("text", String),
)


def create_tables(engine: Engine):
    meta.create_all(engine)
