from dataclasses import dataclass
from datetime import timedelta, time
from typing import Optional

from src.models.user import User


@dataclass
class Timer:
    tid: Optional[int]
    duration: timedelta
    start_time: time
    text: str
    user: User

    def to_json(self) -> dict:
        return {
            "id": self.tid,
            "duration": self.duration.total_seconds(),
            "startTime": self.start_time.isoformat(),
            "text": self.text,
            "user": self.user.to_json(),
        }
