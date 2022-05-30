from dataclasses import dataclass
from datetime import datetime


@dataclass
class Birthday:
    first_name: str
    last_name: str
    date: datetime
