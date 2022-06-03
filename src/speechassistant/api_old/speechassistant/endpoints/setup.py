from flask_restx import Resource

from src.speechassistant.api_old.myapi import api

namespace = api.namespace("setup", description="Endpoint for settings and etc.")


@namespace.route("/")
class Settings(Resource):
    pass


@namespace.route("/system")
class SystemSettings(Resource):
    pass


@namespace.route("/user")
class UserSettings(Resource):
    pass


@namespace.route("/keys")
class KeySettings(Resource):
    pass


@namespace.route("/messenger")
class MessengerSettings(Resource):
    pass


@namespace.route("/phue")
class PhueSettings(Resource):
    pass


@namespace.route("/tv")
class TvSettings(Resource):
    pass
