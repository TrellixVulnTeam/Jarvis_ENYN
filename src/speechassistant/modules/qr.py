#!/usr/bin/env python3

import urllib.request

SECURE = True


def isValid(text):
    text = text.lower()
    if 'qr' in text:
        return True
    else:
        return False


def handle(text, core, skills):
    core.say('Was möchtest du in den qr-code schreiben?')

    # Frage den Nutzer nach Inhalt
    antwort = core.listen()
    if antwort == 'TIMEOUT_OR_INVALID':
        core.say('Ich konnte dich leider nicht verstehen')
    else:
        if not core.messenger_call:
            core.say("Alles klar, ich schicke dir den QR-Code über den Messenger. Solltest du diesen nicht eingerichtet haben, Schau bitte auf der Jarvis-Internetseite nach dem letzten QR-Code!")
            core.say("Diese Internetseite ist leider noch in Arbeit.")
            # toDo: Nur sagen, wenn Messenger nicht eingerichtet ist
        url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={urllib.parse.quote(antwort)}"
        core.say(url, output='messenger')
