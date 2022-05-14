from flask import Response
from flask_restx import Resource

from src.speechassistant.api.myapi import api
from src.speechassistant.api.speechassistant.parser import audio_file_parser as audio_file
from src.speechassistant.api.speechassistant.logic.modules import \
    read_module, \
    read_modules, \
    read_module_names

namespace = api.namespace('modules', desciption='Handles modules of the speech-assistant')


@namespace.route('/')
class Modules(Resource):

    def get(self) -> Response:
        return read_modules()

    @api.expect(audio_file)
    def post(self):
        pass

    @api.expect(audio_file)
    def put(self):
        pass

    def delete(self) -> Response:
        pass


@namespace.route('/<module_name>')
class Module(Resource):

    def get(self, module_name) -> Response:
        return read_module(module_name)


@namespace.route('/names')
class ModulesNames(Resource):

    def get(self) -> Response:
        return read_module_names()