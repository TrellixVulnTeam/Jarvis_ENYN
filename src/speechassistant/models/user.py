from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    uid: int
    alias: str
    first_name: str
    last_name: str
    birthday: datetime
    messenger_id: int
    song_name: str
