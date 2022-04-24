import json
import logging
import os

from flask import Response, request
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from src.speechassistant.api.settings import ALLOWED_AUDIO_EXTENSIONS
from src.speechassistant.exceptions.CriticalExceptions import UnsolvableException
from src.speechassistant.exceptions.SQLException import FileNameAlreadyExists
from src.speechassistant.database.database_connection import DataBase

folder: str = 'C:\\Users\\Jakob\\PycharmProjects\\Jarvis'
database: DataBase = DataBase('C:\\Users\\Jakob\\PycharmProjects\\Jarvis\\src\\speechassistant\\', None)


def create_audio_file(filename: str, data: request) -> Response:
    if 'file' not in data.files:
        raise ValueError('No file was given!')
    file: FileStorage = data.files['file']
    if filename == '':
        raise ValueError('Invalid file name!')
    if allowed_file_name(filename):
        filename: str = secure_filename(filename)
        path: str = os.path.join(folder, filename)
        try:
            database.audio_interface.add_audio(filename, path=path, file_stored=True)
            file.save(path)
        except FileNameAlreadyExists:
            return Response(f'File with filename "{filename}" already exists!', status=400)
        return Response(json.dumps({"new_file_name": filename}), status=201, mimetype='application/json')
    else:
        raise ValueError(f'Given filename ("{filename}") is invalid!')


def read_audio(data: str) -> Response:
    if data:
        name, path = database.audio_interface.get_audio_file(data, as_tuple=True)

        def generate():
            with open(path, 'rb') as fwav:
                data = fwav.read(1024)
                while data:
                    yield data
                    data = fwav.read(1024)

        return Response(generate(), mimetype='audio/x-wav')
    else:
        return Response(status=404)


def read_audio_names() -> Response:
    file_names: list[str] = database.audio_interface.get_file_names()
    return Response(json.dumps({"sound_files": file_names}), mimetype='application/json')


def update_audio_file(data: tuple[str, str]) -> str:
    new_name, old_name = data
    if allowed_file_name(new_name):
        database.audio_interface.update_audio(old_name, new_name)
        # os.rename(os.path.join(folder, old_name), os.path.join(folder, new_name))
        return new_name
    else:
        raise ValueError('Filename invalid!')


def delete_audio_file(data: str) -> Response:
    try:
        anz: int = database.audio_interface.delete_audio(data)
        if anz < 1:
            return Response('No matching audiofile!', status=404)
        else:
            return Response('Audiofile deleted successfully!', status=202)
    except UnsolvableException:
        # toDo
        return Response('Internal Error has occurred!', 500)


def allowed_file_name(filename: str) -> bool:
    return '.' in filename \
           and filename.rsplit('.', 1)[1].lower() in ALLOWED_AUDIO_EXTENSIONS
