from flask import Response
from flask_restx import Resource
from api_old.myapi import api

namespace = api.namespace("phue", desciption="Handle Philips-HUE devices")


@namespace.route("/")
class Phue(Resource):
    def get(self) -> Response:
        pass

    def post(self) -> Response:
        pass

    def put(self) -> Response:
        pass

    def delete(self) -> Response:
        pass


@namespace.route("/lights")
class Phue(Resource):
    def get(self) -> Response:
        pass

    def post(self) -> Response:
        pass

    def put(self) -> Response:
        pass

    def delete(self) -> Response:
        pass


@namespace.route("/lights/<id>")
class Phue(Resource):
    def get(self) -> Response:
        pass

    def post(self) -> Response:
        pass

    def put(self, _id: int) -> Response:
        pass

    def delete(self) -> Response:
        pass
