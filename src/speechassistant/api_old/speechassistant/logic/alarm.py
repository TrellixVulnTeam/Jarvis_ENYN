from __future__ import annotations

import json
import logging

from database.database_connection import DataBase
from exceptions.CriticalExceptions import UnsolvableException
from fastapi import status
from fastapi.responses import JSONResponse
from flask import Response
from models.alarm import Alarm

database: DataBase = DataBase()


def create_alarm(data: dict) -> JSONResponse:
    if "user" not in data.keys():
        data["user"] = -1
    if "sound" not in data.keys() or data["sound"] is None:
        data["sound"] = "standard.wav"
    result_set: Alarm = database.alarm_interface.add_alarm(
        data["time"], data["text"], data["user"], data["repeating"], song=data["sound"]
    )
    result_set["sound"] = "standard"
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=result_set,
        headers={"location": f'/alarms/{result_set["id"]}'},
    )


def read_alarm(data: int | None) -> Response:
    if data:
        alarm: dict = database.alarm_interface.get_alarm(data)
        alarm["sound"] = "standard"
        logging.info(alarm)
        return Response(json.dumps(alarm), mimetype="application/json")
    else:
        alarms: list[dict] = database.alarm_interface.get_alarms(unfiltered=True)
        if not alarms:
            return Response([], mimetype="application/json")
        for alarm in alarms:
            alarm["sound"] = "standard"
        logging.info(alarms)
        return Response(json.dumps(alarms), mimetype="application/json")


def update_alarm(data: dict) -> Response:
    if type(data["active"]) is int:
        data["active"] = data["active"] == 1

    repeating: dict = data["repeating"]
    for day in [
        "regular",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]:
        if type(repeating[day]) is int:
            repeating[day] = repeating[day] == 1
    database.alarm_interface.update_alarm(
        data["id"],
        _time=data["time"],
        _text=data["text"],
        _active=data["active"],
        _sound=data["sound"],
        _regular=repeating["regular"],
    )

    database.alarm_interface.update_repeating(
        data["id"],
        repeating["monday"],
        repeating["tuesday"],
        repeating["wednesday"],
        repeating["thursday"],
        repeating["friday"],
        repeating["saturday"],
        repeating["sunday"],
    )
    return Response(status=200)


def delete_alarm(aid: int) -> Response:
    try:
        anz: int = database.alarm_interface.delete_alarm(aid)
        if anz < 1:
            return Response(f"No matching alarm for ID {aid}!", status=404)
        else:
            return Response("AlarmSchema deleted successfully!", status=202)
    except UnsolvableException:
        # toDo
        return Response("Internal Error has occurred!", 500)
