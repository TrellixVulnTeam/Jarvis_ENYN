import base64
import io
from dataclasses import dataclass


@dataclass
class AudioFile:
    name: str
    data: bytes

    def __init__(self, name: str, data: io.BytesIO) -> None:
        self.name = name
        self.data = base64.b64encode(data.read())

    def get_data(self) -> base64:
        return base64.b64decode(self.data)
