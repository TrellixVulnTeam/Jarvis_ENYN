#!/usr/bin/env python3

import urllib.request

from src.modules import ModuleWrapper

SECURE = True


def is_valid(text: str) -> bool:
    text = text.lower()
    if "qr" in text:
        return True
    else:
        return False


def handle(text: str, wrapper: ModuleWrapper) -> None:
    wrapper.say("Was möchtest du in den qr-code schreiben?")

    # Frage den Nutzer nach Inhalt
    antwort = wrapper.listen()
    if antwort == "TIMEOUT_OR_INVALID":
        wrapper.say("Ich konnte dich leider nicht verstehen")
    else:
        if not wrapper.messenger_call:
            wrapper.say(
                "Alles klar, ich schicke dir den QR-Code über den Messenger. Solltest du diesen nicht eingerichtet haben, Schau bitte auf der Jarvis-Internetseite nach dem letzten QR-Code!"
            )
            wrapper.say("Diese Internetseite ist leider noch in Arbeit.")
            # toDo: Nur sagen, wenn Messenger nicht eingerichtet ist
        url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={urllib.parse.quote(antwort)}"
        wrapper.say(url, output="messenger")
