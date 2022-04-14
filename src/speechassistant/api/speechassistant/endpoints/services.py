
from src.speechassistant.api.myapi import api
from flask_restx import Resource

namespace = api.namespace('service', desciption='Get information of services')


@namespace.route('/')
class Service(Resource):
    pass


@namespace.route('/phue')
class Phue(Resource):
    pass


@namespace.route('/tv')
class Tv(Resource):
    pass


@namespace.route('/weather')
class Weather(Resource):
    pass