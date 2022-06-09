from fastapi import FastAPI, status, Response

from src.speechassistant.api.logic.audioFileLogic import AudioFileLogic
from src.speechassistant.models.audio_file import AudioFile

audio_file_service: FastAPI = FastAPI()


@audio_file_service.post(
    "/", response_model=AudioFile, status_code=status.HTTP_201_CREATED
)
async def create_audio_file(audio_file: AudioFile):
    audio_file: AudioFile = AudioFileLogic.create_audio_file(audio_file)
    return Response(audio_file, status_code=status.HTTP_201_CREATED)


@audio_file_service.get(
    "/", response_model=list[AudioFile], status_code=status.HTTP_200_OK
)
async def get_all_audio_files():
    audio_files: list[AudioFile] = AudioFileLogic.get_all_audio_files()
    return Response(audio_files, status_code=status.HTTP_200_OK)


@audio_file_service.get(
    "/{audio_file_name}", response_model=AudioFile, status_code=status.HTTP_200_OK
)
async def get_audio_file_by_name(audio_file_name: str):
    audio_file: AudioFile = AudioFileLogic.get_audio_file_by_name(audio_file_name)
    return Response(audio_file, status_code=status.HTTP_200_OK)


@audio_file_service.put(
    "/{audio_file_name}", response_model=AudioFile, status_code=status.HTTP_200_OK
)
async def update_audio_file_by_name(audio_file_name: str, audio_file: AudioFile):
    updated_audio_file: AudioFile = AudioFileLogic.update_audio_file_by_name(
        audio_file_name, audio_file
    )
    return Response(updated_audio_file, status_code=status.HTTP_200_OK)


@audio_file_service.delete("/{audio_file_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_audio_file_by_name(audio_file_name: str):
    AudioFileLogic.delete_audio_file_by_name(audio_file_name)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
