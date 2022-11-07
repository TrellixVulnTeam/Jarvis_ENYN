from sqlalchemy import Table, Column, Integer, String, DateTime, Time, Boolean

from src.database.orm.database_persistency import OrmPersistency

DB_PERSISTENCY = OrmPersistency.get_instance()

ALARM_TABLE_NAME = "alarms"
ALARM_REPEATING_TABLE_NAME = "alarm_repeatings"

alarmTable = Table(
    ALARM_TABLE_NAME,
    DB_PERSISTENCY.meta,
    Column("id", Integer, primary_key=True),
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
    DB_PERSISTENCY.meta,
    Column("alarm_id", Integer, primary_key=True),
    Column("monday", Boolean),
    Column("tuesday", Boolean),
    Column("wednesday", Boolean),
    Column("thursday", Boolean),
    Column("friday", Boolean),
    Column("saturday", Boolean),
    Column("sunday", Boolean),
    Column("regular", Boolean),
)
