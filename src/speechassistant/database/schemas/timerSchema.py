from sqlalchemy import Column, Integer, String, Time
from sqlalchemy.orm import declarative_base, relationship

from database.schemas.userSchema import User

Base = declarative_base()


class Timer(Base):
    __tablename__ = "timer"

    id = Column(Integer, primary_key=True)
    duration = Column(String)
    start_time = Column(Time)
    text = Column(String)
    user = relationship(User, back_populates="timer")
