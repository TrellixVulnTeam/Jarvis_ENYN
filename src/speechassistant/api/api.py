from flask import Flask, Blueprint
from src.speechassistant.api import settings
from src.speechassistant.api.myapi import api
from src.speechassistant.api.speechassistant.endpoints.audio_files import (
    namespace as audio_namespace,
)
from src.speechassistant.api.speechassistant.endpoints.alarm import (
    namespace as alarm_namespace,
)
from src.speechassistant.api.speechassistant.endpoints.routine import (
    namespace as routine_namespace,
)
from src.speechassistant.api.speechassistant.endpoints.modules import (
    namespace as modules_namespace,
)

import logging

app: Flask = Flask(__name__)


def configure_app(app) -> None:
    logging.info("[ACTION] Configure REST Api")
    app.config["SWAGGER_UI_DOC_EXPANSION"] = settings.RESTPLUS_SWAGGER_EXPANSION
    app.config["RESTPLUS_VALIDATE"] = settings.RESTPLUS_VAL
    app.config["RESTPLUS_MASK_SWAGGER"] = settings.RESTPLUS_MASK_SWAGGER
    logging.info("[SUCCESS] Configure done")


def init_app(app) -> None:
    logging.info("[ACTION] Init REST Api")
    configure_app(app)
    blueprint: Blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
    api.init_app(blueprint)
    api.add_namespace(audio_namespace)
    api.add_namespace(alarm_namespace)
    api.add_namespace(routine_namespace)
    api.add_namespace(modules_namespace)
    app.register_blueprint(blueprint)
    logging.info("[SUCCESS] Init done")


def main() -> None:
    init_app(app)
    app.run(debug=settings.FLASK_DEBUG, threaded=settings.FLASK_THREADED, port=8080)


if __name__ == "__main__":
    main()
