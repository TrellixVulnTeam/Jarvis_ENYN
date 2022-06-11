from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Time, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class SpecificDate(Base):
    __tablename__ = "specific_date"

    id = Column(Integer, primary_key=True, sqlite_autoincrement=True)
    date = Column(DateTime)


class RoutineDays(Base):
    __tablename__ = "routine_days"

    monday = Column(Boolean)
    tuesday = Column(Boolean)
    wednesday = Column(Boolean)
    thursday = Column(Boolean)
    friday = Column(Boolean)
    saturday = Column(Boolean)
    sunday = Column(Boolean)
    specific_dates = relationship(SpecificDate)


class RoutineClockTime(Base):
    __tablename__ = "routine_clock_time"

    id = Column(Integer, primary_key=True, sqlite_autoincrement=True)
    clock_time = Column(Time)


class RoutineTime(Base):
    __tablename__ = "routine_time"

    clock_times = relationship(RoutineClockTime)
    after_alarm = Column(Boolean)
    after_sunrise = Column(Boolean)
    after_sunset = Column(Boolean)
    after_call = Column(Boolean)


class RoutineRetakes(Base):
    __tablename__ = "routine_retakes"

    days = relationship(RoutineDays)
    times = relationship(RoutineTime)


class RoutineCommandText(Base):
    __tablename__ = "routine_command_text"

    text = Column(String, primary_key=True)


class RoutineCommand(Base):
    __tablename__ = "routine_command"

    id = Column(Integer, primary_key=True, sqlite_autoincrement=True)
    module_name = Column(String, primary_key=True)
    with_text = relationship(RoutineCommandText)


class CallingCommand(Base):
    __tablename__ = "calling_command"

    id = Column(Integer, primary_key=True, sqlite_autoincrement=True)
    routine_name = Column(String)
    command = Column(String)


class Routine(Base):
    __tablename__ = "routine"

    name = Column(String, primary_key=True)
    description = Column(String)
    calling_commands = relationship(CallingCommand)
    retakes = relationship(RoutineRetakes)
    actions = relationship(RoutineCommand)
