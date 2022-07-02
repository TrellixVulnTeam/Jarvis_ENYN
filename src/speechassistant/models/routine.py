from datetime import time, datetime
from typing import Optional

from api.utils.converter import CamelModel
from pydantic import validator, Field


class SpecificDate(CamelModel):
    date: datetime
    sid: Optional[int] = None

    @validator("sid")
    def validate_specific_date_id(cls, v):
        assert v is not None, "ID may not be None!"
        return v

    def as_tuple(self) -> tuple[int, datetime]:
        return self.sid, self.date


class RoutineDays(CamelModel):
    monday: bool = Field(default=False)
    tuesday: bool = Field(default=False)
    wednesday: bool = Field(default=False)
    thursday: bool = Field(default=False)
    friday: bool = Field(default=False)
    saturday: bool = Field(default=False)
    sunday: bool = Field(default=False)
    specific_dates: list[SpecificDate] = Field(default_factory=lambda: [])

    def __post_init__(self):
        self.daily = (
            self.monday
            and self.tuesday
            and self.wednesday
            and self.thursday
            and self.friday
            and self.saturday
            and self.sunday
        )

    def as_tuple(
        self,
    ) -> tuple[bool, bool, bool, bool, bool, bool, bool, list[SpecificDate]]:
        return (
            self.monday,
            self.tuesday,
            self.wednesday,
            self.thursday,
            self.friday,
            self.saturday,
            self.sunday,
            self.specific_dates,
        )


class RoutineClockTime(CamelModel):
    clock_time: time
    ratid: int = Field(default=None)

    def as_tuple(self) -> tuple[int, time]:
        return self.ratid, self.clock_time


class RoutineTime(CamelModel):
    clock_times: list[RoutineClockTime] = Field(default_factory=lambda: [])
    after_alarm: bool = Field(default=False)
    after_sunrise: bool = Field(default=False)
    after_sunset: bool = Field(default=False)
    after_call: bool = Field(default=False)

    def as_tuple(self) -> tuple[list[RoutineClockTime], bool, bool, bool, bool]:
        return (
            self.clock_times,
            self.after_alarm,
            self.after_sunrise,
            self.after_sunset,
            self.after_call,
        )


class RoutineRetakes(CamelModel):
    days: RoutineDays = Field(default_factory=lambda: RoutineDays())
    times: RoutineTime = Field(default_factory=lambda: RoutineTime())

    def as_tuple(self) -> tuple[RoutineDays, RoutineTime]:
        return self.days, self.times


class RoutineCommand(CamelModel):
    module_name: str
    with_text: list[str]
    cid: int = Field(default=None)

    def as_tuple(self) -> tuple[int, str, list[str]]:
        return self.cid, self.module_name, self.with_text


class CallingCommand(CamelModel):
    routine_name: str
    command: str
    ocid: int = Field(default=None)

    def as_tuple(self) -> tuple[int, str, str]:
        return self.ocid, self.routine_name, self.command


class Routine(CamelModel):
    name: str
    description: str
    calling_commands: list[CallingCommand] = Field(default_factory=lambda: [])
    retakes: RoutineRetakes = Field(default_factory=lambda: RoutineRetakes())
    actions: list[RoutineCommand] = Field(default_factory=lambda: [])

    def add_calling_command(self, command: str):
        self.calling_commands.append(
            CallingCommand(routine_name=self.name, command=command)
        )

    def add_routine_command(self, routine_command: RoutineCommand):
        self.actions.append(routine_command)

    def remove_calling_command(self, command: str):
        for index, command in enumerate(self.calling_commands):
            if command.command == command:
                self.calling_commands.remove(self.calling_commands[index])

    def remove_routine_command(self, routine_command: RoutineCommand):
        self.actions.remove(routine_command)

    def as_tuple(
        self,
    ) -> tuple[str, str, list[CallingCommand], RoutineRetakes, list[RoutineCommand]]:
        return (
            self.name,
            self.description,
            self.calling_commands,
            self.retakes,
            self.actions,
        )
