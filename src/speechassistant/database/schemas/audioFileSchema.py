from sqlalchemy import Column, String, LargeBinary

from src.speechassistant.database.DataBasePersistency import DBPersistency
from src.speechassistant.models.audio_file import AudioFile

Base = DBPersistency.Base


class AudioFileSchema(Base):
    __tablename__ = "audiofiles"

    name = Column(String, primary_key=True)
    data = Column(LargeBinary)


def audio_file_to_schema(audio_file: AudioFile) -> AudioFileSchema:
    return AudioFileSchema(name=audio_file.name, data=audio_file.data)


def schema_to_audio_file(audio_file_schema: AudioFileSchema) -> AudioFile:
    return AudioFile(name=audio_file_schema.name, data=audio_file_schema.data)
