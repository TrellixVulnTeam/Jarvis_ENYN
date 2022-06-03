from flask import request
from flask_restx import Resource
from src.speechassistant.api_old.myapi import api
from src.speechassistant.api_old.speechassistant.logic.routine import *
from src.speechassistant.api_old.speechassistant.parser import routine_parser as parser

from src.speechassistant.models.routine import Routine

namespace = api.namespace("routines")


@namespace.route("/")
class RoutineConnection(Resource):
    @api.marshal_with(Routine)
    def get(self) -> Response:
        data: dict = parser.parse_args(request)
        if "name" not in data.keys():
            data = request.get_json()
        if "name" not in data.keys():
            data["name"] = None
        return read_routine(data.get("name"))

    # @api.marshal_with(routine)
    def post(self) -> Response:
        data: dict = request.get_json()
        return create_routine(data)

    #    @api.expect(parser)
    def put(self) -> Response:
        data: dict = request.get_json()
        return update_routine(data)

    #    @api.expect(parser)
    def delete(self) -> Response:
        data: dict = parser.parse_args(request)
        if "name" not in data.keys():
            data = request.get_json()
        return delete_routine(data.get("name"))


@namespace.route("/<name>")
class RoutineConnection(Resource):
    # @api.marshal_with(routine)
    def get(self, name: str) -> Response:
        return read_routine(name)

    # @api.marshal_with(routine)
    def post(self, name: str) -> Response:
        return create_routine(name)

    #    @api.expect(parser)
    def put(self, name: str) -> Response:
        return update_routine(name)

    #    @api.expect(parser)
    def delete(self, name: str) -> Response:
        return delete_routine(name)


@namespace.route("/onCommand")
class OnCommandConnection(Resource):
    def get(self) -> Response:
        data: dict = parser.parse_args(request)
        if "id" not in data.keys():
            data = request.get_json()
        if "name" not in data.keys():
            return Response('Missing argument "id"', status=500)
        read_on_command(data.get("id"))

    def post(self) -> Response:
        data: dict = request.get_json()
        if "routine_name" not in data.keys() or "on_command" not in data.keys():
            return Response(
                'Missing argument "routine_name" or "on_command"', status=500
            )
        create_on_command(data.get("routine_name"), data.get("on_command"))

    def put(self) -> Response:
        data: dict = parser.parse_args(request)
        if "id" not in data.keys():
            data = request.get_json()
        if "id" not in data.keys():
            return Response('Missing argument "id"', status=500)
        return update_on_command(data.get("id"), data.get("on_command"))

    def delete(self) -> Response:
        data: dict = parser.parse_args(request)
        if "id" not in data.keys():
            data = request.get_json()
        if "id" not in data.keys():
            return Response('Missing argument "id"', status=500)
        return delete_on_command(data.get("id"))


@namespace.route("/commands")
class CommandsConnection(Resource):
    def get(self) -> Response:
        data: dict = parser.parse_args(request)
        if "id" not in data.keys():
            data = request.get_json()
        if "id" not in data.keys():
            data["id"] = None
        return read_routine_command(data.get("id"))

    def post(self) -> Response:
        data: dict = request.get_json()
        if "routine_name" not in data.keys() or "module_name" not in data.keys():
            return Response(
                'Missing argument "routine_name" or "module_name"', status=500
            )
        if "commands" not in data.keys():
            data["commands"] = None
        return create_routine_command(
            data.get("routine_name"), data.get("module_name"), data.get("commands")
        )

    def put(self) -> Response:
        data: dict = request.get_json()
        if "routine_name" not in data.keys():
            return Response("Missing ID", status=500)
        return update_routine_command(data["id"], data["name"], data["commands"])

    def delete(self) -> Response:
        data: dict = parser.parse_args(request)
        if "id" not in data.keys():
            data = request.get_json()
        return delete_routine_dates(data.get("id"))


@namespace.route("/routineDates")
class RoutineDatesConnection(Resource):
    def get(self) -> Response:
        data: dict = parser.parse_args(request)
        if "id" not in data.keys():
            data = request.get_json()
        return read_routine_dates(data.get("id"))

    def post(self) -> Response:
        data: dict = request.get_json()
        return create_routine_dates(data.get("id"), data.get("day"), data.get("year"))

    def put(self) -> Response:
        data: dict = request.get_json()
        return update_routine_dates(data.get("id"), data.get("day"), data.get("month"))

    def delete(self) -> Response:
        data: dict = parser.parse_args(request)
        if "id" not in data.keys():
            data = request.get_json()
        return delete_routine_command(data.get("id"))


@namespace.route("/routineTimes")
class RoutineTimesConnection(Resource):
    def get(self) -> Response:
        data: dict = parser.parse_args(request)
        if "id" not in data.keys():
            data = request.get_json()
        return read_routine_time(data.get("id"))

    def post(self) -> Response:
        data: dict = request.get_json()
        return create_routine_time(
            data.get("routine_name"), data.get("hour"), data.get("minute")
        )

    def put(self) -> Response:
        data: dict = request.get_json()
        return update_routine_time(data.get("id"), data.get("hour"), data.get("minute"))

    def delete(self) -> Response:
        data: dict = parser.parse_args(request)
        if "id" not in data.keys():
            data = request.get_json()
        return delete_routine_time(data.get("id"))
