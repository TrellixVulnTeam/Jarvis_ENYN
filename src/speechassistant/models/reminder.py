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
