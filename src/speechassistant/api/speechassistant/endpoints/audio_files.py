from flask import request, Response
from flask_restx import Resource
from flask_restx.reqparse import ParseResult

from src.speechassistant.api.myapi import api
from src.speechassistant.api.speechassistant.parser import audio_file_parser as audio_file
from src.speechassistant.exceptions.CriticalExceptions import UnsolvableException
from src.speechassistant.api.speechassistant.logic.audio import \
    read_audio, \
    create_audio_file, \
    update_audio_file, \
    delete_audio_file

namespace = api.namespace('audio', desciption='Handles audiofiles of the speech-assistant')


@namespace.route('/')
class AudioFiles(Resource):

    def get(self) -> Response:
        args: ParseResult = audio_file.parse_args(request)
        name: str = args.get('name', None)

        return read_audio(name)

    @api.expect(audio_file)
    def post(self):
        args: ParseResult = audio_file.parse_args(request)
        name: str = args.get('name', None)
        try:
            return create_audio_file(name, request)
        except ValueError as e:
            return Response(e.args[0], 400)

    @api.expect(audio_file)
    def put(self):
        try:
            args: ParseResult = audio_file.parse_args(request)
            name: str = args.get('name')
            old_name: str = args.get('old_name')

            new_name: str = update_audio_file((name, old_name))
            return Response(f'Changed name of {old_name} to {new_name}!', 200)
        except ValueError:
            return Response('Given filename does not match!', 404)

    def delete(self) -> Response:
        try:
            args: ParseResult = audio_file.parse_args(request)
            name: str = args.get('name')
            return delete_audio_file(name)

        except UnsolvableException:
            return Response('Internal Server Error', 500)

