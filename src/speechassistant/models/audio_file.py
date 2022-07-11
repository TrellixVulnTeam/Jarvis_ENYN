import base64

from api.utils.converter import CamelModel


class AudioFile(CamelModel):
    name: str
    data: bytes

    def __int__(self, name: str, data: str):
        super(name)
        self.data = base64.b64decode(data)

    class Config:
        json_encoders = {bytes: lambda b: base64.b64encode(b.read())}

    def to_json(self) -> dict:
        return {"name": self.name, "data": self.data}
