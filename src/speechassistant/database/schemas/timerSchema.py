from database.schemas.userSchema import UserSchema
from sqlalchemy import Column, Integer, String, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Timer(Base):
    __tablename__ = "timer"

    id = Column(Integer, primary_key=True)
    duration = Column(String)
    start_time = Column(Time)
    text = Column(String)
    user = relationship(UserSchema, back_populates="timer")
