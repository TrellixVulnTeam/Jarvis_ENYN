import json
import os


def is_Valid(text):
    text = text.lower()
    if 'lad' in text and 'routine' in text:
        return True


def handle(text, core, skills):
    routines = []
    for file in os.listdir(core.path):
        with open(file) as routine_file:
            routine = json.load(routine_file)
        routines.append(routine)

    for routine in routines:
        if routine["retakes"]["time"]["after_alarm"]:
            core.local_storage["alarm_routines"].append(routine)
            routines.remove(routine)
    core.local_storage["routines"] = routines
    core.say('Die Routinen wurden aktualisiert.')
