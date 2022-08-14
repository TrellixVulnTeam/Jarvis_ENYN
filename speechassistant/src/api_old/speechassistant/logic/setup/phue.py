from flask import Response

from src.services import PhilipsWrapper

service = PhilipsWrapper()


def read_device_by_id(_id: int) -> Response:
    pass


def read_phue(data: dict) -> Response:
    pass


def update_phue(data: dict) -> Response:
    pass
