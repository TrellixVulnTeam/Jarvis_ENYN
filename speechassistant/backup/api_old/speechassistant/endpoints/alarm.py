from src import log

from flask import request, Response
from flask_restx import Resource
from flask_restx.reqparse import ParseResult

from src.api_old.myapi import api
from src.api_old.speechassistant.api_definition import alarm_file
from src.api_old.speechassistant.logic.alarm import (
    create_alarm,
    read_alarm,
    update_alarm,
    delete_alarm,
)
from src.api_old.speechassistant.parser import alarm_parser as alarm
from src.models.alarm import Alarm

namespace = api.namespace("alarms")


@namespace.route("/")
class AlarmConnection(Resource):
    def get(self) -> Response:
        args = request.args
        aid: int = None
        if args:
            aid = args.get("id")
        return read_alarm(aid)

    @api.expect(Alarm)
    def post(self) -> Response:
        data: dict = request.get_json()
        return create_alarm(data)

    def put(self) -> Response:
        args: ParseResult = alarm.parse_args(request)
        if "id" not in args.keys():
            return Response("No ID was given!", status=400)
        return update_alarm(args)

    @api.expect(alarm_file)
    def delete(self) -> Response:
        args: ParseResult = alarm.parse_args(request)
        if "id" not in args.keys():
            return Response("No ID was given!", status=400)
        aid: int = args["id"]
        return delete_alarm(aid)


@namespace.route("/<alarm_id>")
class AlarmConnectionById(Resource):
    def get(self, alarm_id) -> Response:
        return read_alarm(alarm_id)

    @api.expect(alarm_file)
    def put(self, alarm_id) -> Response:
        # args: ParseResult = alarm.parse_args(request)
        args: dict = request.get_json()
        log.info(args)
        if "id" not in args.keys():
            args["id"] = alarm_id
        return update_alarm(args)

    @api.expect(alarm_file)
    def delete(self, alarm_id) -> Response:
        return delete_alarm(alarm_id)
