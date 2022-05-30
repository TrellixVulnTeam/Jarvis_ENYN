from dataclasses import dataclass, field
from datetime import time, datetime


@dataclass
class SpecificDate:
    date: datetime
    sid: int = field(default=None)

    def as_tuple(self) -> tuple[int, datetime]:
        return self.sid, self.date


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


@dataclass
class RoutineClockTime:
    clock_time: time
    ratid: int = field(default=None)

    def as_tuple(self) -> tuple[int, time]:
        return self.ratid, self.clock_time


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


@dataclass
class RoutineRetakes:
    days: RoutineDays = field(default_factory=lambda: RoutineDays())
    times: RoutineTime = field(default_factory=lambda: RoutineTime())

    def as_tuple(self) -> tuple[RoutineDays, RoutineTime]:
        return self.days, self.times


@dataclass
class RoutineCommand:
    module_name: str
    with_text: list[str]
    cid: int = field(default=None)

    def as_tuple(self) -> tuple[int, str, list[str]]:
        return self.cid, self.module_name, self.with_text


@dataclass
class CallingCommand:
    routine_name: str
    command: str
    ocid: int = field(default=None)

    def as_tuple(self) -> tuple[int, str, str]:
        return self.ocid, self.routine_name, self.command


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
