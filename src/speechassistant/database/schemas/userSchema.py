from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.speechassistant.database.DataBasePersistency import DBPersistency

Base = DBPersistency.Base


class WaitingNotifications(Base):
    __tablename__ = "waiting_notifications"
    text = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    alias = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    birthday = Column(DateTime)
    messenger_id = Column(Integer)
    song_name = Column(String)
    waiting_notifications = relationship("WaitingNotifications")
