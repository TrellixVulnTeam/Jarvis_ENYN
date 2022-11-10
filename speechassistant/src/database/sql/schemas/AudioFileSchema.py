from database.sql.schemas.AbstractSchema import AbstractSchema
from models import AudioFile


class AudioFileSchema(AbstractSchema):
    def __init__(self, _id: int, name: str, data: bytes):
        self.id = _id
        self.name = name
        self.data = data

    def to_model(self, **kwargs) -> AudioFile:
        return AudioFile(id=self.id, name=self.name, data=self.data)

    @staticmethod
    def from_model(model: AudioFile, **kwargs) -> "AudioFileSchema":
        return AudioFileSchema(_id=model.id, name=model.name, data=model.data)

    def __repr__(self) -> str:
        return f"AudioFileSchema(id: {self.id}, name: {self.name}, data: {self.data[0:37]}...)"
