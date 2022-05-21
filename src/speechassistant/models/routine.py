from dataclasses import dataclass


@dataclass
class SpecificDate:
    sid: int
    day: int
    month: int


@dataclass
class Days:
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
class ClockTimes:
    cid: int
    hour: int
    minute: int
    after_alarm: bool
    after_sunrise: bool
    after_sunset: bool
    after_call: bool


@dataclass
class Retakes:
    days: Days
    clock_times: list[ClockTimes]


@dataclass
class Command:
    cid: int
    module_name: str
    with_text: list[str]


@dataclass
class Routine:
    name: str
    description: str
    calling_commands: list[str]
    retakes: Retakes
    actions: list[Command]

    def add_calling_command(self, command: str):
        self.calling_commands.append(command)

    def add_action(self, command: Command):
        self.actions.append(command)

    def remove_calling_command(self, command: str):
        self.calling_commands.remove(command)

    def remove_action(self, command: Command):
        self.actions.remove(command)
