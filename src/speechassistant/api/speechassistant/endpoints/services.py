
from src.speechassistant.api.myapi import api
from flask_restx import Resource

namespace = api.namespace('service', desciption='Get information of services')


# /api/v1/service/
@namespace.route('/lights')
class ApiServices(Resource):

    def get(self):
        pass

    @api.expect()
    def post(self):
        pass