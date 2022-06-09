from flask import Response

from src.speechassistant.database.database_connection import DataBase
from src.speechassistant.models.User import User

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

    return Response({"id": uid}, status=201)


def read_user(data: int | None) -> Response:
    user_set: dict = database.user_interface.get_user(data)
    return Response(user_set, status=200)


def update_user(data: dict) -> Response:
    updated_user: User = database.user_interface.update_user(
        data["uid"],
        _new_alias=data["alias"],
        _new_first_name=data["firstname"],
        _new_last_name=data["lastname"],
        _birthday=data["birthday"],
        _song_name=data["song"],
        _messenger_id=data["messenger_id"],
    )
    return Response(updated_user, status=204)


def delete_user(uid: int) -> Response:
    database.user_interface.delete_user(uid)
    return Response(status=201)
