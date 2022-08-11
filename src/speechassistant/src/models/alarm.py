from __future__ import annotations

from datetime import datetime

from pydantic import datetime_parse

from src.api.utils.converter import CamelModel


class AlarmRepeating(CamelModel):
    monday: bool
    tuesday: bool
    wednesday: bool
    thursday: bool
    friday: bool
    saturday: bool
    sunday: bool
    regular: bool

    def __repr__(self):
        return f"monday: {self.monday}, tuesday: {self.tuesday}, wednesday: {self.wednesday}, thursday: {self.thursday}, friday: {self.friday}, saturday: {self.saturday}, sunday: {self.sunday}"


class Alarm(CamelModel):
    text: str
    alarm_time: datetime_parse.time
    repeating: AlarmRepeating
    song_name: str
    active: bool = True
    initiated: bool = False
    alarm_id: int = None
    user_id: int = None
    last_executed: datetime | None = None

    def __repr__(self):
        return f"Alarm(alarm_id: {self.alarm_id}, user_id: {self.user_id}, text: {self.text}, alarm_time: {self.alarm_time}, repeating: {self.repeating}, song_name: {self.song_name}, active: {self.active}, initiated: {self.initiated}, last_executed: {self.last_executed})"
