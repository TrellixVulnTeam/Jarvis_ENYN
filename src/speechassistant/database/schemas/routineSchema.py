from sqlalchemy import Column, Integer, String, Boolean, Time, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

from src.speechassistant.models.routine import (
    Routine,
    CallingCommand,
    RoutineRetakes,
    RoutineDays,
    RoutineTime,
)

Base = declarative_base()


class RoutineSchema(Base):
    __tablename__ = "routines"

    name = Column(String, primary_key=True)
    description = Column(String)
    calling_commands = relationship("CallingCommandSchema")
    retakes = relationship("RoutineRetakesSchema")
    actions = relationship("RoutineCommandSchema")


class RoutineDaysSchema(Base):
    __tablename__ = "routinedays"

    routine_day_id = Column(Integer, primary_key=True)
    monday = Column(Boolean)
    tuesday = Column(Boolean)
    wednesday = Column(Boolean)
    thursday = Column(Boolean)
    friday = Column(Boolean)
    saturday = Column(Boolean)
    sunday = Column(Boolean)
    specific_dates = relationship("SpecificDateSchema")
    routine_retake_id = Column(Integer, ForeignKey("routineclocktime.id"))


class SpecificDateSchema(Base):
    __tablename__ = "specificdates"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    routine_days_id = Column(Integer, ForeignKey(RoutineDaysSchema.routine_day_id))


class RoutineTimeSchema(Base):
    __tablename__ = "routinetimes"

    id = Column(Integer, primary_key=True)
    clock_times = relationship("RoutineClockTimeSchema")
    after_alarm = Column(Boolean)
    after_sunrise = Column(Boolean)
    after_sunset = Column(Boolean)
    after_call = Column(Boolean)
    routine_retake_id = Column(Integer, ForeignKey("routineretakes.id"))


class RoutineClockTimeSchema(Base):
    __tablename__ = "routineclocktimes"

    id = Column(Integer, primary_key=True)
    clock_time = Column(Time)
    clock_time_id = Column(Integer, ForeignKey(RoutineTimeSchema.id))


class RoutineRetakesSchema(Base):
    __tablename__ = "routineretakes"

    id = Column(Integer, primary_key=True)
    days = relationship("RoutineDaysSchema")
    times = relationship("RoutineTimeSchema")
    routine_name = Column(Integer, ForeignKey(RoutineSchema.name))


class RoutineCommandSchema(Base):
    __tablename__ = "routinecommands"

    id = Column(Integer, primary_key=True)
    module_name = Column(String, primary_key=True)
    with_text = relationship("RoutineCommandTextSchema")
    routine_name = Column(Integer, ForeignKey("routines.name"))


class RoutineCommandTextSchema(Base):
    __tablename__ = "routinecommandtext"

    text = Column(String, primary_key=True)
    routine_command_id = Column(Integer, ForeignKey(RoutineCommandSchema.id))


class CallingCommandSchema(Base):
    __tablename__ = "callingcommands"

    id = Column(Integer, primary_key=True)
    routine_name = Column(Integer, ForeignKey(RoutineSchema.name))
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


def schema_to_routine(routine: RoutineSchema) -> Routine:
    return Routine(
        name=routine.name,
        description=routine.description,
        calling_commands=__schema_to_calling_command(routine.calling_commands),
        retakes=__schema_to_retakes(routine.retakes),
    )
