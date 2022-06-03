from __future__ import annotations

from dataclasses import dataclass, fields, field
from datetime import datetime, time
from typing import Optional

from dataclasses_json import dataclass_json, LetterCase, config
from pydantic import BaseModel


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class AlarmRepeating(BaseModel):
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
    # def from_json(json_data: dict) -> AlarmRepeating:
    #     return AlarmRepeating(
    #         json_data.get("monday"),
    #         json_data.get("tuesday"),
    #         json_data.get("wednesday"),
    #         json_data.get("thursday"),
    #         json_data.get("friday"),
    #         json_data.get("saturday"),
    #         json_data.get("sunday"),
    #         json_data.get("regular"),
    #     )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Alarm(BaseModel):
    repeating: AlarmRepeating
    song_name: str
    text: str
    active: bool
    initiated: bool
    alarm_time: time = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )
    __last_executed: Optional[str] = None
    user_id: int = -1
    aid: Optional[int] = None

    def get_last_executed(self) -> datetime:
        return datetime.fromisoformat(self.__last_executed)

    def set_last_executed(self, last_executed: datetime) -> None:
        self.__last_executed = last_executed.isoformat()

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
    # def from_json(json_data: dict) -> Alarm:
    #     return Alarm(
    #         AlarmRepeating.from_json(json_data.get("repeating")),
    #         json_data.get("songName"),
    #         json_data.get("alarmTime"),
    #         json_data.get("text"),
    #         json_data.get("active"),
    #         json_data.get("initiated"),
    #         json_data.get("lastExecuted"),
    #         json_data.get("userId"),
    #     )
