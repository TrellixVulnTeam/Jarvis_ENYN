from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    alias: str
    first_name: str
    last_name: str
    birthday: datetime
    messenger_id: int
    song_name: str
    waiting_notifications: list[str]
    uid: Optional[int] = None

    def __post_init__(self):
        pass

    def to_json(self) -> dict:
        return {
            "id": self.uid,
            "alias": self.alias,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "birthday": self.birthday.isoformat(),
            "messengerId": self.messenger_id,
            "songName": self.song_name,
            "waitingNotifications": self.waiting_notifications,
        }
