from dataclasses import dataclass
from datetime import timedelta, datetime

from src.speechassistant.models.user import User


@dataclass
class Timer:
    tid: int
    duration: timedelta
    start_time: datetime
    text: str
    user: User
