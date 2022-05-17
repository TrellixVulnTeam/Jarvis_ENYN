from flask import Response

from src.speechassistant.api.myapi import api
from flask_restx import Resource

namespace = api.namespace("service", desciption="Get information of services")


@namespace.route("/")
class Service(Resource):
    pass


@namespace.route("/phue")
class Phue(Resource):
    def get(self) -> Response:
        pass

    def post(self) -> Response:
        pass

    def put(self) -> Response:
        pass

    def delete(self) -> Response:
        pass


@namespace.route("/tv")
class Tv(Resource):
    pass


@namespace.route("/weather")
class Weather(Resource):
    pass
