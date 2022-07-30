from sqlalchemy import Table, Column, Integer, String, DateTime, Time, Boolean, MetaData
from sqlalchemy.future import Engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

ALARM_TABLE_NAME = "alarms"
ALARM_REPEATING_TABLE_NAME = "alarm_repeatings"

alarmTable = Table(
    ALARM_TABLE_NAME,
    Base.metadata,
    Column("id", Integer),
    Column("text", String),
    Column("alarm_time", Time),
    Column("song_name", String),
    Column("active", Boolean),
    Column("initiated", Boolean),
    Column("user_id", Integer),
    Column("last_executed", DateTime),
)

alarmRepeatingTable = Table(
    ALARM_REPEATING_TABLE_NAME,
    Base.metadata,
    Column("alarm_id", Integer),
    Column("monday", Boolean),
    Column("tuesday", Boolean),
    Column("wednesday", Boolean),
    Column("thursday", Boolean),
    Column("friday", Boolean),
    Column("saturday", Boolean),
    Column("sunday", Boolean),
    Column("regular", Boolean),
)


def create_alarm_tables(engine: Engine):
    meta = MetaData()
    meta.create_all(engine)
