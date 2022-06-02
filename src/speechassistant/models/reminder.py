from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.speechassistant.models.user import User


@dataclass
class Reminder:
    rid: Optional[int]
    time: datetime
    text: str
    user: User

    def to_json(self) -> dict:
        return {
            "reminderId": self.rid,
            "time": self.time.isoformat(),
            "text": self.text,
            "user": self.user.to_json(),
        }
