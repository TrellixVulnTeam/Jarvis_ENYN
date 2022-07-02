from __future__ import annotations

from datetime import datetime, time

from src.speechassistant.api.utils.converter import CamelModel


class AlarmRepeating(CamelModel):
    monday: bool
    tuesday: bool
    wednesday: bool
    thursday: bool
    friday: bool
    saturday: bool
    sunday: bool
    regular: bool


class Alarm(CamelModel):
    text: str
    alarm_time: time
    repeating: AlarmRepeating
    song_name: str
    active: bool = True
    initiated: bool = False
    alarm_id: int = None
    user_id: int = None
    last_executed: datetime | None = None
