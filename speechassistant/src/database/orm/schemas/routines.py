from sqlalchemy import Column, Integer, String, Boolean, Time, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

from src.models.routine import (
    Routine,
    CallingCommand,
    RoutineRetakes,
    RoutineDays,
    RoutineTime,
)
from ..tables import (
    ROUTINE_TABLE_NAME,
    ROUTINE_DAYS_TABLE_NAME,
    SPECIFIC_DATES_TABLE_NAME,
    ROUTINE_TIMES_TABLE_NAME,
    ROUTINE_CLOCK_TIME_TABLE_NAME,
    ROUTINE_RETAKES_TABLE_NAME,
    ROUTINE_COMMAND_TABLE_NAME,
    ROUTINE_COMMAND_TEXT_TABLE_NAME,
    CALLING_COMMAND_TABLE_NAME,
)

Base = declarative_base()


class RoutineSchema(Base):
    __tablename__ = ROUTINE_TABLE_NAME

    name = Column(String, primary_key=True)
    description = Column(String)
    calling_commands = relationship("CallingCommandSchema", cascade="all, delete")
    retakes = relationship("RoutineRetakesSchema", cascade="all, delete")
    actions = relationship("RoutineCommandSchema", cascade="all, delete")


class RoutineDaysSchema(Base):
    __tablename__ = ROUTINE_DAYS_TABLE_NAME

    routine_day_id = Column(Integer, primary_key=True)
    monday = Column(Boolean)
    tuesday = Column(Boolean)
    wednesday = Column(Boolean)
    thursday = Column(Boolean)
    friday = Column(Boolean)
    saturday = Column(Boolean)
    sunday = Column(Boolean)
    specific_dates = relationship("SpecificDateSchema", cascade="all, delete")
    routine_retake_id = Column(Integer, ForeignKey("routineclocktime.id"))


class SpecificDateSchema(Base):
    __tablename__ = SPECIFIC_DATES_TABLE_NAME

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    routine_days_id = Column(Integer, ForeignKey(RoutineDaysSchema.routine_day_id))


class RoutineTimeSchema(Base):
    __tablename__ = ROUTINE_TIMES_TABLE_NAME

    id = Column(Integer, primary_key=True)
    clock_times = relationship("RoutineClockTimeSchema", cascade="all, delete")
    after_alarm = Column(Boolean)
    after_sunrise = Column(Boolean)
    after_sunset = Column(Boolean)
    after_call = Column(Boolean)
    routine_retake_id = Column(Integer, ForeignKey("routineretakes.id"))


class RoutineClockTimeSchema(Base):
    __tablename__ = ROUTINE_CLOCK_TIME_TABLE_NAME

    id = Column(Integer, primary_key=True)
    clock_time = Column(Time)
    clock_time_id = Column(Integer, ForeignKey(RoutineTimeSchema.id))


class RoutineRetakesSchema(Base):
    __tablename__ = ROUTINE_RETAKES_TABLE_NAME

    id = Column(Integer, primary_key=True)
    days = relationship("RoutineDaysSchema", cascade="all, delete")
    times = relationship("RoutineTimeSchema", cascade="all, delete")
    routine_name = Column(Integer, ForeignKey(RoutineSchema.name))


class RoutineCommandSchema(Base):
    __tablename__ = ROUTINE_COMMAND_TABLE_NAME

    id = Column(Integer, primary_key=True)
    module_name = Column(String, primary_key=True)
    with_text = relationship("RoutineCommandTextSchema", cascade="all, delete")
    routine_name = Column(Integer, ForeignKey("routines.name"))


class RoutineCommandTextSchema(Base):
    __tablename__ = ROUTINE_COMMAND_TEXT_TABLE_NAME

    text = Column(String, primary_key=True)
    routine_command_id = Column(Integer, ForeignKey(RoutineCommandSchema.id))


class CallingCommandSchema(Base):
    __tablename__ = CALLING_COMMAND_TABLE_NAME

    id = Column(Integer, primary_key=True)
    routine_name = Column(String, ForeignKey(RoutineSchema.name))
    command = Column(String)


def __schema_to_calling_command(schema: CallingCommandSchema) -> CallingCommand:
    return CallingCommand(
        routine_name=schema.routine_name, command=schema.command, ocid=schema.id
    )


def __calling_command_to_schema(
    calling_command: CallingCommand,
) -> CallingCommandSchema:
    return CallingCommandSchema(
        id=calling_command.ocid,
        command=calling_command.command,
        routine_name=calling_command.routine_name,
    )


# toDo


def __schema_to_days(schema: RoutineDaysSchema) -> RoutineDays:
    pass


def __days_to_schema(days: RoutineDays) -> RoutineDaysSchema:
    pass


def __schema_to_times(schema: RoutineTimeSchema) -> RoutineTime:
    pass


def __times_to_schema(times: RoutineTime) -> RoutineTimeSchema:
    return RoutineTimeSchema(
        # toDo
    )


def __schema_to_retakes(schema: RoutineRetakesSchema) -> RoutineRetakes:
    return RoutineRetakes(days=schema.days, times=schema.times)


def __retakes_to_schema(retakes: RoutineRetakes) -> RoutineRetakesSchema:
    return RoutineRetakesSchema(
        days=__days_to_schema(retakes.days), times=__times_to_schema(retakes.times)
    )


def schema_to_routine(schema: RoutineSchema) -> Routine:
    return Routine(
        name=schema.name,
        description=schema.description,
        calling_commands=__schema_to_calling_command(schema.calling_commands),
        retakes=__schema_to_retakes(schema.retakes),
    )


def routine_to_schema(model: Routine) -> RoutineSchema:
    return RoutineSchema(
        name=model.name,
        description=model.description,
        calling_commands=None,
        retakes=None,
    )
