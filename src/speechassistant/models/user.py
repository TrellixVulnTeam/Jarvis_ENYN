from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class User:
    uid: Optional[int]
    alias: str
    first_name: str
    last_name: str
    birthday: datetime
    messenger_id: int
    song_name: str
    waiting_notifications: list[str] = field(default_factory=list)
