from __future__ import annotations

import json

from flask import Response
from src.speechassistant.exceptions.CriticalExceptions import UnsolvableException
from src.speechassistant.database.database_connection import DataBase

database: DataBase = DataBase('C:\\Users\\Jakob\\PycharmProjects\\Jarvis\\src\\speechassistant\\', None)


def create_alarm(data: dict) -> Response:
    if 'user' not in data.keys():
        data['user'] = -1
    if 'sound' not in data.keys() or data['sound'] is None:
        data['sound'] = 'standard.wav'
    result_set: dict = database.alarm_interface.add_alarm(data['time'], data['text'], data['user'], data['repeating'], song=data['sound'])
    return Response(result_set, mimetype='application/json', status=201)


def read_alarm(data: int | None) -> Response:
    if data:
        alarm: dict = database.alarm_interface.get_alarm(data)
        return Response(json.dumps(alarm), mimetype='application/json')
    else:
        alarms: list[dict] = database.alarm_interface.get_alarms(unsorted=True)
        print(alarms)
        return Response(json.dumps(alarms), mimetype='application/json')


def update_alarm(data: dict) -> Response:
    database.alarm_interface.update_alarm(data['aid'],
                                          _time=data['time'],
                                          _text=data['text'],
                                          _active=data['active'],
                                          _sound=data['sound'],
                                          _regular=data['regular'])
    repeating: dict = data['repeating']
    database.alarm_interface.update_repeating(data['aid'],
                                              repeating['monday'],
                                              repeating['tuesday'],
                                              repeating['wednesday'],
                                              repeating['thursday'],
                                              repeating['friday'],
                                              repeating['saturday'],
                                              repeating['sunday']
                                              )
    return Response(status=200)


def delete_alarm(aid: int) -> Response:
    try:
        anz: int = database.alarm_interface.delete_alarm(aid)
        if anz < 1:
            return Response(f'No matching alarm for ID {aid}!', status=404)
        else:
            return Response('Alarm deleted successfully!', status=202)
    except UnsolvableException:
        # toDo
        return Response('Internal Error has occurred!', 500)
