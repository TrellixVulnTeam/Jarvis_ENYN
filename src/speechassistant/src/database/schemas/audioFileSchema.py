from sqlalchemy import Column, String, LargeBinary, Integer
from sqlalchemy.ext.declarative import declarative_base

from src.models.audio_file import AudioFile

Base = declarative_base()


class AudioFileSchema(Base):
    __tablename__ = "audiofiles"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    data = Column(LargeBinary)


def audio_file_to_schema(audio_file: AudioFile) -> AudioFileSchema:
    return AudioFileSchema(id=audio_file.id, name=audio_file.name, data=audio_file.data)


def schema_to_audio_file(audio_file_schema: AudioFileSchema) -> AudioFile:
    return AudioFile(id=audio_file_schema.id, name=audio_file_schema.name, data=audio_file_schema.data)
