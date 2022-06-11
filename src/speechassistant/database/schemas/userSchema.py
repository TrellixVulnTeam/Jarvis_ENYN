from sqlalchemy import Column, Integer, String, Time, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class WaitingNotifications(Base):
    __tablename__ = "waiting_notifications"

    text = Column(String)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, sqlite_autoincrement=True)
    alias = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    birthday = Column(DateTime)
    messenger_id = Column(Integer)
    song_name = Column(String)
    waiting_notifications = relationship(WaitingNotifications)
