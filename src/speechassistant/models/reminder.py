from dataclasses import dataclass
from datetime import datetime

from src.speechassistant.models.user import User


@dataclass
class Reminder:
    rid: int
    time: datetime
    text: str
    user: User
