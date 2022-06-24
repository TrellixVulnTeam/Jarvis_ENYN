from pydantic import BaseModel

from api.utils.converter import CamelModel


class Module(CamelModel):
    name: str
