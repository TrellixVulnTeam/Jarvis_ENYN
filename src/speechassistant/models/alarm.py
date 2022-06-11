from __future__ import annotations

from pydantic.dataclasses import dataclass, Field
from datetime import datetime, time

from src.speechassistant.api.utils.converter import (
    CamelModelConfig,
    CamelModel,
    to_camel,
)


class AlarmRepeating(CamelModel):
    monday: bool
    tuesday: bool
    wednesday: bool
    thursday: bool
    friday: bool
    saturday: bool
    sunday: bool
    regular: bool

    # def to_json(self) -> dict:
    #     return {
    #         "monday": self.monday,
    #         "tuesday": self.tuesday,
    #         "wednesday": self.wednesday,
    #         "thursday": self.thursday,
    #         "friday": self.friday,
    #         "saturday": self.saturday,
    #         "sunday": self.sunday,
    #         "regular": self.regular,
    #     }
    #
    # @staticmethod
    # def from_json(json_data: dict) -> AlarmRepeatingSchema:
    #     return AlarmRepeatingSchema(
    #         json_data.get("monday"),
    #         json_data.get("tuesday"),
    #         json_data.get("wednesday"),
    #         json_data.get("thursday"),
    #         json_data.get("friday"),
    #         json_data.get("saturday"),
    #         json_data.get("sunday"),
    #         json_data.get("regular"),
    #     )


class Alarm(CamelModel):
    text: str
    alarm_time: time
    repeating: AlarmRepeating
    song_name: str
    active: bool = True
    initiated: bool = False
    user_id: int = None
    alarm_id: int = None
    last_executed: datetime | None = None

    # def to_json(self) -> dict:
    #     return {
    #         "id": self.aid,
    #         "repeating": self.repeating.to_json(),
    #         "songName": self.song_name,
    #         "alarmTime": self.__alarm_time,
    #         "text": self.text,
    #         "active": self.active,
    #         "initiated": self.initiated,
    #         "lastExecuted": self.__last_executed,
    #         "userId": self.user_id,
    #     }
    #
    # @staticmethod
    # def from_json(json_data: dict) -> AlarmSchema:
    #     return AlarmSchema(
    #         AlarmRepeatingSchema.from_json(json_data.get("repeating")),
    #         json_data.get("songName"),
    #         json_data.get("alarmTime"),
    #         json_data.get("text"),
    #         json_data.get("active"),
    #         json_data.get("initiated"),
    #         json_data.get("lastExecuted"),
    #         json_data.get("userId"),
    #     )
