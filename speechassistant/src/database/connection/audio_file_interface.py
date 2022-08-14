from typing import Type

from src.database.connection.abstract_database_connection import Schema, Model, AbstractDataBaseConnection
from src.database.schemas.audio_files import audio_file_to_schema, AudioFileSchema, schema_to_audio_file
from src.models.audio_file import AudioFile


class AudioFileInterface(AbstractDataBaseConnection[AudioFile, AudioFileSchema]):
    @staticmethod
    def get_model_type() -> Type[Model]:
        return AudioFile

    @staticmethod
    def get_schema_type() -> Type[Schema]:
        return AudioFileSchema

    @staticmethod
    def schema_to_model(model_schema: AudioFileSchema) -> AudioFile:
        return schema_to_audio_file(model_schema)

    @staticmethod
    def model_to_schema(model: AudioFile) -> AudioFileSchema:
        return audio_file_to_schema(model)

    @staticmethod
    def get_model_id(model: AudioFile) -> int:
        return model.id

    def __int__(self) -> None:
        super().__init__()
        from src.database.tables.audiofiles import create_tables
        create_tables(self.engine)
