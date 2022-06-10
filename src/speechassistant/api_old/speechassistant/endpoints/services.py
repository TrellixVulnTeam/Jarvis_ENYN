from flask import Response
from flask_restx import Resource
from src.speechassistant.api_old.myapi import api

namespace = api.namespace("service", desciption="Get information of routers")


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
