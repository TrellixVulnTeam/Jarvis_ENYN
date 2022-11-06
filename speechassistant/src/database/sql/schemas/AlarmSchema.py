from datetime import time, datetime

from src.database.sql.schemas.AbstractSchema import AbstractSchema, Schema
from src.models import Alarm


class AlarmSchema(AbstractSchema[Alarm, "AlarmSchema"]):

    def __init__(self, _id: int, text: str, alarm_time: time, song_name: str, active: bool, initiated: bool,
                 user_id: int, last_executed: datetime):
        super().__init__()
        self.id = _id
        self.text = text
        self.alarm_time = alarm_time
        self.song_name = song_name
        self.active = active
        self.initiated = initiated
        self.user_id = user_id
        self.last_executed = last_executed

    def to_model(self, repeating: AlarmRepeatingSchema) -> Alarm:
        return Alarm(
            text=self.text,
            alarm_time=self.alarm_time,
            repeating=repeating,
            song_name=self.song_name,
            active=self.active,
            initiated=self.initiated,
            alarm_id=self.id,
            user_id=self.user_id,
            last_executed=self.last_executed
        )

    @staticmethod
    def from_model(model: Alarm) -> Schema:
        return AlarmSchema(
            text=model.text,
            alarm_time=model.alarm_time,
            song_name=model.song_name,
            active=model.active,
            initiated=model.initiated,
            _id=model.alarm_id,
            user_id=model.user_id,
            last_executed=model.last_executed
        )

    def __repr__(self) -> str:
        return f"AlarmSchema(id: {self.id}, user_id: {self.user_id}, text: {self.text}, alarm_time: {self.alarm_time}, song_name: {self.song_name}, active: {self.active}, initiated: {self.initiated}, last_executed: {self.last_executed})"
