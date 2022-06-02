from dataclasses import dataclass, field
from datetime import time, datetime


@dataclass
class SpecificDate:
    date: datetime
    sid: int = field(default=None)

    def as_tuple(self) -> tuple[int, datetime]:
        return self.sid, self.date

    def to_json(self) -> dict:
        return {"id": self.sid, "date": self.date.isoformat()}


@dataclass
class RoutineDays:
    monday: bool = field(default=False)
    tuesday: bool = field(default=False)
    wednesday: bool = field(default=False)
    thursday: bool = field(default=False)
    friday: bool = field(default=False)
    saturday: bool = field(default=False)
    sunday: bool = field(default=False)
    specific_dates: list[SpecificDate] = field(default_factory=lambda: [])

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

    def to_json(self) -> dict:
        return {
            "monday": self.monday,
            "tuesday": self.tuesday,
            "wednesday": self.wednesday,
            "thursday": self.thursday,
            "friday": self.friday,
            "saturday": self.saturday,
            "sunday": self.sunday,
            "specific_dates": [date.to_json() for date in self.specific_dates],
        }


@dataclass
class RoutineClockTime:
    clock_time: time
    ratid: int = field(default=None)

    def as_tuple(self) -> tuple[int, time]:
        return self.ratid, self.clock_time

    def to_dict(self) -> dict:
        return {
            "id": self.ratid,
            "clockTime": self.clock_time.isoformat(),
        }


@dataclass
class RoutineTime:
    clock_times: list[RoutineClockTime] = field(default_factory=lambda: [])
    after_alarm: bool = field(default=False)
    after_sunrise: bool = field(default=False)
    after_sunset: bool = field(default=False)
    after_call: bool = field(default=False)

    def as_tuple(self) -> tuple[list[RoutineClockTime], bool, bool, bool, bool]:
        return (
            self.clock_times,
            self.after_alarm,
            self.after_sunrise,
            self.after_sunset,
            self.after_call,
        )

    def to_json(self) -> dict:
        return {
            "clockTimes": [routine_time.to_json() for routine_time in self.clock_times],
            "afterAlarm": self.after_alarm,
            "afterSunrise": self.after_sunrise,
            "afterSunset": self.after_sunset,
            "afterCall": self.after_call,
        }


@dataclass
class RoutineRetakes:
    days: RoutineDays = field(default_factory=lambda: RoutineDays())
    times: RoutineTime = field(default_factory=lambda: RoutineTime())

    def as_tuple(self) -> tuple[RoutineDays, RoutineTime]:
        return self.days, self.times

    def to_json(self) -> dict:
        return {"days": self.days.to_json(), "times": self.times.to_json()}


@dataclass
class RoutineCommand:
    module_name: str
    with_text: list[str]
    cid: int = field(default=None)

    def as_tuple(self) -> tuple[int, str, list[str]]:
        return self.cid, self.module_name, self.with_text

    def to_json(self) -> dict:
        return {
            "id": self.cid,
            "moduleName": self.module_name,
            "withText": self.with_text,
        }


@dataclass
class CallingCommand:
    routine_name: str
    command: str
    ocid: int = field(default=None)

    def as_tuple(self) -> tuple[int, str, str]:
        return self.ocid, self.routine_name, self.command

    def to_json(self) -> dict:
        return {
            "id": self.ocid,
            "routineName": self.routine_name,
            "command": self.command,
        }


@dataclass
class Routine:
    name: str
    description: str
    calling_commands: list[CallingCommand] = field(default_factory=lambda: [])
    retakes: RoutineRetakes = field(default_factory=lambda: RoutineRetakes())
    actions: list[RoutineCommand] = field(default_factory=lambda: [])

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

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "callingCommands": self.calling_commands,
            "retakes": self.retakes,
        }
