from database.schemas.userSchema import UserSchema
from models.reminder import Reminder
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ReminderSchema(Base):
    __tablename__ = "reminder"

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    text = Column(String)
    user_id = Column(ForeignKey(UserSchema.id))


def schema_to_reminder(reminder: ReminderSchema) -> Reminder:
    return Reminder(
        time=reminder.time,
        text=reminder.text,
        user_id=reminder.user_id,
        reminder_id=reminder.id,
    )


def reminder_to_schema(reminder: Reminder) -> ReminderSchema:
    return ReminderSchema(
        id=reminder.reminder_id,
        time=reminder.time,
        text=reminder.text,
        user_id=reminder.user_id,
    )
