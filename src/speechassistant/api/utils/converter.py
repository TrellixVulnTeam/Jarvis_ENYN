from datetime import time

from humps import camel
from pydantic import BaseModel


def to_camel(string: str) -> str:
    return camel.case(string)


class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = (True,)
        validate_assignment = (True,)
        orm_mode = True


class CamelModelConfig:
    alias_generator = to_camel
    allow_population_by_field_name = True
