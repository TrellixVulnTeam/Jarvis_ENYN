import base64

from pydantic import BaseModel

from src.api.utils.converter import to_camel


class AudioFile(BaseModel):
    id: int
    name: str
    data: bytes

    def __int__(self, name: str, data: str):
        super(name)
        self.data = base64.b64decode(data)

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = (True,)
        validate_assignment = (True,)
        orm_mode = True
        json_encoders = {bytes: lambda b: base64.b64encode(b.read())}

    def to_json(self) -> dict:
        return {"name": self.name, "data": self.data}
