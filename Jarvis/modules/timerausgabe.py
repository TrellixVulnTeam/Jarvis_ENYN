import os
import time


def handle(text, luna, skills):
    duration = text.get('Dauer')
    print("handle - Funktion \n\n\n\n\n\n")
    luna.say("Dein Timer von {} ist abgelaufen!".format(duration))
    if not luna.telegram_call:
        luna.say("Dein Timer von {} ist abgelaufen!".format(duration), output='telegram')


def isValid(text):
    return False
