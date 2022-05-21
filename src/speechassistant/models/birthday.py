from dataclasses import dataclass


@dataclass
class Birthday:
    first_name: str
    last_name: str
    day: int
    month: int
    year: int
