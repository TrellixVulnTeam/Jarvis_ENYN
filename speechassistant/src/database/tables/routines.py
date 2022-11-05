from sqlalchemy import Table, Column, String, Integer, Boolean, Time

from database.database_persistency import DBPersistency

DB_PERSISTENCY = DBPersistency.get_instance()

ROUTINE_TABLE_NAME = "routines"
ROUTINE_DAYS_TABLE_NAME = "routinedays"
SPECIFIC_DATES_TABLE_NAME = "specificdates"
ROUTINE_TIMES_TABLE_NAME = "routinetimes"
ROUTINE_CLOCK_TIME_TABLE_NAME = "routineclocktimes"
ROUTINE_RETAKES_TABLE_NAME = "routineretakes"
ROUTINE_COMMAND_TABLE_NAME = "routinecommands"
ROUTINE_COMMAND_TEXT_TABLE_NAME = "routinecommandtext"
CALLING_COMMAND_TABLE_NAME = "callingcommands"

routineCallingCommandTable = Table(
    CALLING_COMMAND_TABLE_NAME,
    DB_PERSISTENCY.meta,
    Column("id", Integer),
    Column("routine_name", Integer),
    Column("command", String),
)

routineCommandTextTable = Table(
    ROUTINE_COMMAND_TEXT_TABLE_NAME,
    DB_PERSISTENCY.meta,
    Column("text", String),
    Column("routine_command_id", Integer),
)

routineCommandTable = Table(
    ROUTINE_COMMAND_TABLE_NAME,
    DB_PERSISTENCY.meta,
    Column("id", Integer),
    Column("module_name", String),
    Column("routine_name", Integer),
)

routineRetakesTable = Table(
    ROUTINE_RETAKES_TABLE_NAME,
    DB_PERSISTENCY.meta,
    Column("id", Integer),
    Column("routine_name", Integer),
)

routineClockTimeTable = Table(
    ROUTINE_CLOCK_TIME_TABLE_NAME,
    DB_PERSISTENCY.meta,
    Column("id", Integer),
    Column("clock_time", Time),
    Column("clock_time_id", Integer),
)

routineTimeTable = Table(
    ROUTINE_TIMES_TABLE_NAME,
    DB_PERSISTENCY.meta,
    Column("id", Integer),
    Column("after_alarm", Boolean),
    Column("after_sunrise", Boolean),
    Column("after_sunset", Boolean),
    Column("after_call", Boolean),
    Column("routine_retake_id", Integer),
)

specificDatesTable = Table(
    SPECIFIC_DATES_TABLE_NAME,
    DB_PERSISTENCY.meta,
    Column("id", Integer),
    Column("routine_days_id", Integer),
)

routineDaysTable = Table(
    ROUTINE_DAYS_TABLE_NAME,
    DB_PERSISTENCY.meta,
    Column("routine_day_id", Integer),
    Column("monday", Boolean),
    Column("tuesday", Boolean),
    Column("wednesday", Boolean),
    Column("thursday", Boolean),
    Column("friday", Boolean),
    Column("saturday", Boolean),
    Column("sunday", Boolean),
    Column("routine_retake_id", Integer),
)

routineTable = Table(
    ROUTINE_TABLE_NAME,
    DB_PERSISTENCY.meta,
    Column("name", String),
    Column("description", String),
)
