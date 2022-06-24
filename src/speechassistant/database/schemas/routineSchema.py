from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Time, DateTime
from sqlalchemy.orm import declarative_base, relationship

from models.routine import Routine, CallingCommand, RoutineRetakes, RoutineDays, RoutineTime

Base = declarative_base()


class SpecificDateSchema(Base):
    __tablename__ = "specific_date"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)


class RoutineDaysSchema(Base):
    __tablename__ = "routine_days"

    monday = Column(Boolean)
    tuesday = Column(Boolean)
    wednesday = Column(Boolean)
    thursday = Column(Boolean)
    friday = Column(Boolean)
    saturday = Column(Boolean)
    sunday = Column(Boolean)
    specific_dates = relationship(SpecificDateSchema)


class RoutineClockTimeSchema(Base):
    __tablename__ = "routine_clock_time"

    id = Column(Integer, primary_key=True)
    clock_time = Column(Time)


class RoutineTimeSchema(Base):
    __tablename__ = "routine_time"

    clock_times = relationship(RoutineClockTimeSchema)
    after_alarm = Column(Boolean)
    after_sunrise = Column(Boolean)
    after_sunset = Column(Boolean)
    after_call = Column(Boolean)


class RoutineRetakesSchema(Base):
    __tablename__ = "routine_retakes"

    days = relationship(RoutineDaysSchema)
    times = relationship(RoutineTimeSchema)


class RoutineCommandTextSchema(Base):
    __tablename__ = "routine_command_text"

    text = Column(String, primary_key=True)


class RoutineCommandSchema(Base):
    __tablename__ = "routine_command"

    id = Column(Integer, primary_key=True)
    module_name = Column(String, primary_key=True)
    with_text = relationship(RoutineCommandTextSchema)


class CallingCommandSchema(Base):
    __tablename__ = "calling_command"

    id = Column(Integer, primary_key=True)
    routine_name = Column(String)
    command = Column(String)


class RoutineSchema(Base):
    __tablename__ = "routine"

    name = Column(String, primary_key=True)
    description = Column(String)
    calling_commands = relationship(CallingCommandSchema)
    retakes = relationship(RoutineRetakesSchema)
    actions = relationship(RoutineCommandSchema)


def __schema_to_calling_command(schema: CallingCommandSchema) -> CallingCommand:
    return CallingCommand(
        routine_name=schema.routine_name,
        command=schema.command,
        ocid=schema.id
    )


def __calling_command_to_schema(calling_command: CallingCommand) -> CallingCommandSchema:
    return CallingCommandSchema(
        id=calling_command.ocid,
        command=calling_command.command,
        routine_name=calling_command.routine_name
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
    return RoutineRetakes(
        days=schema.days,
        times=schema.times
    )


def __retakes_to_schema(retakes: RoutineRetakes) -> RoutineRetakesSchema:
    return RoutineRetakesSchema(
        days=__days_to_schema(retakes.days),
        times=__times_to_schema(retakes.times)
    )


def schema_to_routine(routine: RoutineSchema) -> Routine:
    return Routine(
        name=routine.name,
        description=routine.description,
        calling_commands=__schema_to_calling_command(routine.calling_commands),
        retakes=__schema_to_retakes(routine.retakes)
    )
