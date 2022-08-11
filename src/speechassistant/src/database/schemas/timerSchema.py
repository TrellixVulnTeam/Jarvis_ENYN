from datetime import timedelta

from sqlalchemy import Column, Integer, String, Time, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from src.database.schemas.userSchema import UserSchema
from src.models.timer import Timer

Base = declarative_base()


class TimerSchema(Base):
    __tablename__ = "timer"

    id = Column(Integer, primary_key=True)
    duration = Column(BigInteger)
    start_time = Column(Time)
    text = Column(String)
    user = relationship(UserSchema, back_populates="timer", cascade="all, delete")


def timer_to_schema(model: Timer) -> TimerSchema:
    return TimerSchema(
        id=model.tid,
        duration=int(model.duration.total_seconds()),
        start_time=model.start_time,
        text=model.text,
        user=model.user
    )


def schema_to_timer(schema: TimerSchema) -> Timer:
    return Timer(
        tid=schema.id,
        duration=timedelta(seconds=schema.duration),
        start_time=schema.start_time,
        text=schema.text,
        user=schema.user
    )
