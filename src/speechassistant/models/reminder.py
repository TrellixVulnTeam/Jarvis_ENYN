from datetime import datetime

from sqlalchemy.orm import declarative_base

from src.speechassistant.api.utils.converter import CamelModel

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
