from dataclasses import dataclass
from datetime import time


@dataclass
class SpecificDate:
    sid: int
    day: int
    month: int


@dataclass
class RoutineDays:
    monday: bool
    tuesday: bool
    wednesday: bool
    thursday: bool
    friday: bool
    saturday: bool
    sunday: bool
    specific_dates: list[SpecificDate]

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


@dataclass
class RoutineClockTime:
    rctid: int
    clock_time: time


@dataclass
class RoutineTimes:
    times: list[RoutineClockTime]
    after_alarm: bool
    after_sunrise: bool
    after_sunset: bool
    after_call: bool


@dataclass
class RoutineRetakes:
    days: RoutineDays
    clock_times: RoutineTimes


@dataclass
class RoutineCommand:
    cid: int
    module_name: str
    with_text: list[str]


@dataclass
class Routine:
    name: str
    description: str
    calling_commands: list[str]
    retakes: RoutineRetakes
    actions: list[RoutineCommand]

    def add_calling_command(self, command: str):
        self.calling_commands.append(command)

    def add_action(self, command: RoutineCommand):
        self.actions.append(command)

    def remove_calling_command(self, command: str):
        self.calling_commands.remove(command)

    def remove_action(self, command: RoutineCommand):
        self.actions.remove(command)
