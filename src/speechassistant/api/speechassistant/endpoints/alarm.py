from flask import request, Response
from flask_restx import Resource
from flask_restx.reqparse import ParseResult

from src.speechassistant.api.myapi import api
from src.speechassistant.api.speechassistant.parser import alarm_parser as alarm
from src.speechassistant.api.speechassistant.api_definition import alarm_file
from src.speechassistant.api.speechassistant.logic.alarm import \
    create_alarm, \
    read_alarm, \
    update_alarm, \
    delete_alarm

namespace = api.namespace('alarm')


@namespace.route('/')
class AlarmConnection(Resource):

    def get(self) -> Response:
        args = request.args

        return read_alarm(args.get('id'))

    @api.expect(alarm_file)
    def post(self) -> Response:
        data: dict = request.get_json()

        return create_alarm(data)

    @api.expect(alarm_file)
    def put(self) -> Response:
        args: ParseResult = alarm.parse_args(request)
        if 'id' not in args.keys():
            return Response('No ID was given!', status=400)
        return update_alarm(args)

    @api.expect(alarm_file)
    def delete(self) -> Response:
        args: ParseResult = alarm.parse_args(request)
        if 'id' not in args.keys():
            return Response('No ID was given!', status=400)
        aid: int = args['id']
        return delete_alarm(aid)
