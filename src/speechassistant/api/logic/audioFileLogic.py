from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.speechassistant.models.audio_file import AudioFile
    from fastapi.responses import StreamingResponse

from src.speechassistant.database.database_connection import DataBase

audio_file_interface: any = DataBase().audio_interface


class AudioFileLogic:
    @staticmethod
    def create_audio_file(audio_file: AudioFile) -> AudioFile:
        new_name: str = audio_file_interface.add_audio(audio_file.name, audio_file.data)
        audio_file.name = new_name
        return audio_file

    @staticmethod
    def get_all_audio_files() -> list[AudioFile]:
        return audio_file_interface.get_all_audio_files()

    @staticmethod
    def get_audio_file_by_name(name: str) -> StreamingResponse:
        with open(audio_file_interface.get_audio_file_by_name(name)) as audio_file:
            yield from audio_file

    @staticmethod
    def update_audio_file_by_name(name: str, audio_file: AudioFile) -> AudioFile:
        return audio_file_interface.update_audio_file(name, audio_file)

    @staticmethod
    def delete_audio_file_by_name(name: str) -> None:
        audio_file_interface.delete_audio(name)
