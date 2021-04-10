import os
import time


def handle(text, core, skills):
    duration = text.get('Dauer')
    core.say("Dein Timer von {} ist abgelaufen!".format(duration))
    if not core.messenger_call:
        core.say("Dein Timer von {} ist abgelaufen!".format(duration), output='messenger')


def isValid(text):
    return False
