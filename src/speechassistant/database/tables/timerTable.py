from sqlalchemy import Table, Column, Integer, String, Time
from sqlalchemy.orm import declarative_base

Base = declarative_base()

TIMER_TABLE_NAME = "timer"

timerTable = Table(
    TIMER_TABLE_NAME,
    Base.metadata,
    Column("id", Integer),
    Column("duration", String),
    Column("start_time", Time),
    Column("text", String)
)
