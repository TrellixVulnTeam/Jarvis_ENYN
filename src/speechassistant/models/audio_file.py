import base64
import io
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, validator

from src.speechassistant.api.utils.converter import CamelModel


class AudioFile(CamelModel):
    name: str
    data: bytes

    class Config:

        self.data = base64.b64encode(**args.get("base64_data").read())

    def get_data(self):
        pass

    def to_json(self) -> dict:
        return {"name": self.name, "data": self.data}
