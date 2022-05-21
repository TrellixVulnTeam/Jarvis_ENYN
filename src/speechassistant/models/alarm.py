from dataclasses import dataclass
from datetime import datetime


@dataclass
class Time:
    hour: int
    minute: int

    def __after_init__(self):
        self.total_seconds = self.hour * 3600 + self.minute * 60


@dataclass
class Repeating:
    monday: bool
    tuesday: bool
    wednesday: bool
    thursday: bool
    friday: bool
    saturday: bool
    sunday: bool
    regular: bool


@dataclass
class Alarm:
    aid: int
    song_name: str
    time: Time
    text: str
    active: bool
    initiated: bool
    last_executed: datetime
    user_id: int = -1
