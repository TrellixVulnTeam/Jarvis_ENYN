from datetime import datetime

from api.utils.converter import CamelModel
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Reminder(CamelModel):
    time: datetime
    text: str
    user_id: int
    reminder_id: int

    """def to_json(self) -> dict:
        return {
            "reminderId": self.rid,
            "time": self.time.isoformat(),
            "text": self.text,
            "user": self.user.to_json(),
        }"""
