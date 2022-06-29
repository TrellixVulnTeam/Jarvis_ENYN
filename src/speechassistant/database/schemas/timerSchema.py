from sqlalchemy import Column, Integer, String, Time
from sqlalchemy.orm import relationship

from src.speechassistant.database.DataBasePersistency import DBPersistency
from src.speechassistant.database.schemas.userSchema import User

Base = DBPersistency.Base


class Timer(Base):
    __tablename__ = "timer"

    id = Column(Integer, primary_key=True)
    duration = Column(String)
    start_time = Column(Time)
    text = Column(String)
    user = relationship(User, back_populates="timer")
