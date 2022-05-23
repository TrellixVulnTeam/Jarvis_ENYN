from dataclasses import dataclass
from datetime import datetime, time


@dataclass
class AlarmRepeating:
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
    repeating: AlarmRepeating
    song_name: str
    alarm_time: time
    text: str
    active: bool
    initiated: bool
    last_executed: datetime
    user_id: int = -1
