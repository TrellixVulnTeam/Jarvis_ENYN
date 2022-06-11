from sqlalchemy import Column, String, LargeBinary
from sqlalchemy.orm import declarative_base, relationship

from src.speechassistant.models.audio_file import AudioFile

Base = declarative_base()


class AudioFileSchema(Base):
    __tablename__ = "audio_file"

    name = Column(String, primary_key=True)
    data = Column(LargeBinary)


def audio_file_to_schema(audio_file: AudioFile) -> AudioFileSchema:
    return AudioFileSchema(
        name=audio_file.name,
        data=audio_file.data
    )


def schema_to_audio_file(audio_file_schema: AudioFileSchema) -> AudioFile:
    return AudioFile(
        name=audio_file_schema.name,
        data=audio_file_schema.data
    )
