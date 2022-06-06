from pydantic import BaseModel

from src.speechassistant.api.utils.converter import CamelModel


class Module(CamelModel):
    name: str
