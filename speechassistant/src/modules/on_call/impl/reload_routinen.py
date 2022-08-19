import json
import os

from src.modules import ModuleWrapper


# toDo: refactor

def isValid(text: str) -> bool:
    text = text.lower()
    if "lad" in text and "routine" in text:
        return True


def handle(text: str, wrapper: ModuleWrapper) -> None:
    routines = []
    for file in os.listdir(wrapper.path + "/resources/routine/"):
        with open(wrapper.path + "/resources/routine/" + file) as routine_file:
            routine = json.load(routine_file)
        routines.append(routine)

    for routine in routines:
        if routine["retakes"]["activation"]["after_alarm"]:
            wrapper.local_storage["alarm_routines"].append(routine)
            routines.remove(routine)
    wrapper.local_storage["routines"] = routines
    if text is not "":
        wrapper.say("Die Routinen wurden aktualisiert.")
