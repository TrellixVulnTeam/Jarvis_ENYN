from api_old import settings
from api_old.myapi import api
from api_old.speechassistant.endpoints.alarm import (
    namespace as alarm_namespace,
)
from api_old.speechassistant.endpoints.audio_files import (
    namespace as audio_namespace,
)
from api_old.speechassistant.endpoints.modules import (
    namespace as modules_namespace,
)
from api_old.speechassistant.endpoints.routine import (
    namespace as routine_namespace,
)
from flask import Flask, Blueprint

from src import log

app: Flask = Flask(__name__)


def configure_app(app) -> None:
    log.action("Configure REST Api...")
    app.config["SWAGGER_UI_DOC_EXPANSION"] = settings.RESTPLUS_SWAGGER_EXPANSION
    app.config["RESTPLUS_VALIDATE"] = settings.RESTPLUS_VAL
    app.config["RESTPLUS_MASK_SWAGGER"] = settings.RESTPLUS_MASK_SWAGGER
    log.info("API configured.")


def init_app(app) -> None:
    log.action("Init REST Api...")
    configure_app(app)
    blueprint: Blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
    api.init_app(blueprint)
    api.add_namespace(audio_namespace)
    api.add_namespace(alarm_namespace)
    api.add_namespace(routine_namespace)
    api.add_namespace(modules_namespace)
    app.register_blueprint(blueprint)
    log.info("API initialized!")


def main() -> None:
    init_app(app)
    app.run(debug=settings.FLASK_DEBUG, threaded=settings.FLASK_THREADED, port=8080)


if __name__ == "__main__":
    main()
