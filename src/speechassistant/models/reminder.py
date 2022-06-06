from datetime import datetime
from typing import Optional

from src.speechassistant.api.utils.converter import CamelModel


class Reminder(CamelModel):
    time: datetime
    text: str
    user_id: int
    reminder_id: int = None

    """def to_json(self) -> dict:
        return {
            "reminderId": self.rid,
            "time": self.time.isoformat(),
            "text": self.text,
            "user": self.user.to_json(),
        }"""
