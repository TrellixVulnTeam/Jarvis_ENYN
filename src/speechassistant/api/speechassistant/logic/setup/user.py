from flask import Response

from src.speechassistant.database.database_connection import DataBase

database: DataBase = DataBase(
    "C:\\Users\\Jakob\\PycharmProjects\\Jarvis\\src\\speechassistant\\", None
)


def create_user(data: dict) -> Response:
    uid: int = database.user_interface.add_user(
        data["alias"],
        data["firstname"],
        data["lastname"],
        data["birthday"],
        data["messenger_id"],
        data["song_id"],
    )
    return Response(uid, status=201)


def read_user(data: int | None) -> Response:
    pass


def update_user(data: dict) -> Response:
    pass


def delete_user(uid: int) -> Response:
    pass
