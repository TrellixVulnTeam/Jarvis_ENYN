from dataclasses import dataclass
from datetime import datetime


@dataclass
class Birthday:
    first_name: str
    last_name: str
    date: datetime

    def to_json(self) -> dict:
        return {
            "firstName": self.first_name,
            "lastName": self.last_name,
            "date": self.date.isoformat(),
        }
