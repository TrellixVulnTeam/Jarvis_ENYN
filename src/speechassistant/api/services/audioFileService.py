from fastapi import FastAPI, status

from src.speechassistant.models.audio_file import AudioFile

audio_file_service: FastAPI = FastAPI()


@audio_file_service.post(
    "/", response_model=AudioFile, status_code=status.HTTP_201_CREATED
)
async def create_audio_file(audio_file: AudioFile):
    pass


@audio_file_service.get(
    "/", response_model=list[AudioFile], status_code=status.HTTP_200_OK
)
async def get_all_audio_files():
    pass


@audio_file_service.get(
    "/{audio_file_name}", response_model=AudioFile, status_code=status.HTTP_200_OK
)
async def get_audio_file_by_name(audio_file_name: str):
    pass


@audio_file_service.put(
    "/{audio_file_name}", response_model=AudioFile, status_code=status.HTTP_200_OK
)
async def update_audio_file_by_name(audio_file_name: str, audio_file: AudioFile):
    pass


@audio_file_service.delete(
    "/{audio_file_name}", response_model=status.HTTP_204_NO_CONTENT
)
async def delete_audio_file_by_name(audio_file_name: str):
    pass
