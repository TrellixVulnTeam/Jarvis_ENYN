from datetime import datetime

from database.sql.schemas.AbstractSchema import AbstractSchema
from models import Reminder


class ReminderSchema(AbstractSchema):
    def __init__(self, _id: int, _time: datetime, text: str, user_id: int):
        self.id = _id
        self.time = datetime
        self.text = text
        self.user_id = user_id

    def to_model(self, **kwargs) -> Reminder:
        return Reminder(
            time=self.time, text=self.text, user_id=self.user_id, reminder_id=self.id
        )

    @staticmethod
    def from_model(model: Reminder, **kwargs) -> "ReminderSchema":
        return ReminderSchema(
            _id=model.reminder_id,
            text=model.text,
            user_id=model.user_id,
            time=model.time,
        )

    def __repr__(self) -> str:
        return f"ReminderSchema(id: {self.id}, time: {self.time}, text: {self.text}, user_id: {self.user_id}) "
