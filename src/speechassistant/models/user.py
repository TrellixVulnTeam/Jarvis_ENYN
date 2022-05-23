from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    uid: int
    alias: str
    first_name: str
    last_name: str
    birthday: datetime
    messenger_id: int
    song_name: str
    waiting_notifications: list[str] = field(default_factory=list)
