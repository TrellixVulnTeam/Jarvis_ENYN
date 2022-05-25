from dataclasses import dataclass
from datetime import timedelta, time
from typing import Optional

from src.speechassistant.models.user import User


@dataclass
class Timer:
    tid: Optional[int]
    duration: timedelta
    start_time: time
    text: str
    user: User
