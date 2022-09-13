from flask_restx import Api
from src import log

api: Api = Api(
    version="0.1",
    title="Speech-assistant API",
    description="This API is used to access to modules and routers of the Speech-assistant",
)


@api.errorhandler
def std_handler(e):
    log.warning(e)
    return {"message": "An unexpected error has occurred."}, 500
