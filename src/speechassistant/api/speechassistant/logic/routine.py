from __future__ import annotations

import json
from sqlite3 import OperationalError

from flask import Response

from src.speechassistant.database.database_connection import DataBase
from src.speechassistant.exceptions.SQLException import NoMatchingEntry

database: DataBase = DataBase('C:\\Users\\Jakob\\PycharmProjects\\Jarvis\\src\\speechassistant\\', None)


def create_routine(data: dict) -> Response:
    database.routine_interface.add_routine(data)
    return Response('Routine created', status=201)


def read_routine(name: str | None) -> Response:
    print(name)
    if name:
        try:
            routine: dict = database.routine_interface.get_routine(name)
        except NoMatchingEntry:
            routine = {}
        return Response(json.dumps(routine), mimetype='application/json', status=200)
    else:
        routines: list[dict] = database.routine_interface.get_routines()
        print(routines)
        return Response(json.dumps({'routines': routines}), mimetype='application/json', status=200)


def update_routine(data: dict) -> Response:
    database.routine_interface.update_routine(old_name=data["name"], new_routine_dict=data)
    return Response(f'Routine with name {data["rname"]} updated successfully!', status=200)


def delete_routine(name: str) -> Response:
    counter: int = database.routine_interface.delete_routine(name)
    if counter < 1:
        return Response(f'No routine found with name "{name}"!', status=404)
    else:
        return Response(f'Deleted {counter} entries.', status=202)


def create_on_command(rname: str, on_command: str) -> Response:
    ocid: int = database.routine_interface.create_on_command(rname, on_command)
    return Response(json.dumps({"id": ocid}), mimetype='application/json', status=201)


def read_on_command(ocid: int) -> Response:
    result_set: dict = database.routine_interface.get_on_command(ocid)
    return Response(json.dumps(result_set), mimetype='application/json', status=200)


def update_on_command(ocid: int, command: str) -> Response:
    database.routine_interface.update_on_command(ocid, command)
    return Response(f'Command with ID {ocid} updated successfully!', status=200)


def delete_on_command(ocid: int) -> Response:
    database.routine_interface.delete_on_command(ocid)
    return Response(f'On Command with ID {ocid} removed successfully!', status=202)


def create_routine_command(rname: str, module_name: str, commands: list) -> Response:
    rcid: int = database.routine_interface.create_routine_commands(rname, module_name, commands)
    return Response(json.dumps({"id": rcid}), mimetype='application/json', status=201)


def read_routine_command(rcid: int) -> Response:
    result_set: dict = database.routine_interface.get_routine_command(rcid)
    return Response(json.dumps(result_set), mimetype='application/json', status=201)


def update_routine_command(rcid: int, module_name: str, text: list[str]) -> Response:
    database.routine_interface.update_routine_commands(rcid, module_name, text)
    return Response(f'Command with ID {rcid} updated successfully!', status=200)


def delete_routine_command(rcid: int) -> Response:
    database.routine_interface.delete_routine_command(rcid)
    return Response(f'Command with ID {rcid} removed successfully!', status=202)


def create_routine_dates(rname: str, day: int, month: int) -> Response:
    rdid: int = database.routine_interface.create_routine_dates(rname, day, month)
    return Response(json.dumps({"id": rdid}), mimetype='application/json', status=201)


def read_routine_dates(rdid: int) -> Response:
    result_set: dict = database.routine_interface.get_routine_dates(rdid)
    return Response(json.dumps(result_set), mimetype='application/json', status=200)


def update_routine_dates(rdid: int, day: int, month: int) -> Response:
    database.routine_interface.update_date_of_day(rdid, day, month)
    return Response(f'Routine date with ID {rdid} updated successfully!', status=200)


def delete_routine_dates(rdid: int) -> Response:
    database.routine_interface.delete_routine_dates(rdid)
    return Response(f'Date with ID {rdid} removed successfully!', status=202)


def create_routine_time(rname, hour, minute) -> Response:
    ratid: int = database.routine_interface.create_routine_activation_time(rname, hour, minute)
    return Response(json.dumps({"id": ratid}), mimetype='application/json', status=201)


def read_routine_time(ratid: int) -> Response:
    result_set: dict = database.routine_interface.get_routine_activation_time(ratid)
    return Response(json.dumps(result_set), mimetype='application/json', status=200)


def update_routine_time(ratid: int, hour: int, minute: int) -> Response:
    database.routine_interface.update_activation_time(ratid, hour, minute)
    return Response(f'Routine time with ID {ratid} updated successfully!', status=200)


def delete_routine_time(ratid: int) -> Response:
    database.routine_interface.delete_routine_activation_time(ratid)
    return Response(f'Routine Time with ID {ratid} removed successfully!', status=202)


def create_command_text(rname: str, module_name: str) -> Response:
    rcid: int = database.routine_interface.create_routine_commands(rname, module_name)
    return Response(json.dumps({"id": rcid}), mimetype='application/json', status=201)


def read_command_text(rcid: int) -> Response:
    result_set: dict = database.routine_interface.get_routine_command(rcid)
    return Response(json.dumps(result_set), mimetype='application/json', status=200)


def update_command_text(rcid: int, module_name: str, text: list[str]) -> Response:
    database.routine_interface.update_command_text(rcid, module_name, text)
    return Response(f'Command Text with ID {rcid} updated successfully!', status=200)


def delete_command_text(rcid: int) -> Response:
    database.routine_interface.delete_routine_command(rcid)
    return Response(f'Command Text with ID {rcid} removed successfully!', status=202)
