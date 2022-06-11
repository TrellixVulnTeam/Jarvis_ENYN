from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Time, DateTime
from sqlalchemy.orm import declarative_base, relationship

from src.speechassistant.database.schemas.userSchema import User

Base = declarative_base()


class Reminder(Base):
    __tablename__ = "reminder"

    id = Column(Integer, primary_key=True, sqlite_autoincrement=True)
    time = Column(DateTime)
    text = Column(String)
    user_id = Column(ForeignKey(User.uid))
