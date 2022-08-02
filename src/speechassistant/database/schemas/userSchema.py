from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class WaitingNotifications(Base):
    __tablename__ = "waitingnotifications"
    text = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))


class UserSchema(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    alias = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    birthday = Column(DateTime)
    messenger_id = Column(Integer)
    song_name = Column(String)
    waiting_notifications = relationship("WaitingNotifications", cascade="all, delete")
