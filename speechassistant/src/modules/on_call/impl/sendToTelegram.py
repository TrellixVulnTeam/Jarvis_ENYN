import re

from src.modules import ModuleWrapper

# Beschreibung
"""
Mit diesem Modul kann man sich Nachrichten per Telegram zuschicken lassen.
Dazu sagt man "Sende <text> an mein Smartphone" oder "Smartphone Nachricht <text>".
"""


def is_valid(text: str) -> bool:
    text = text.lower()
    if "smartphone" in text and ("nachricht" in text or "sende" in text):
        return True
    else:
        return False


def handle(text: str, wrapper: ModuleWrapper) -> None:
    text = text.lower()
    length = len(text)

    match = re.search("^smartphone nachricht", text)
    if match is not None:
        end = match.end() + 1
        nachricht = text[end:length]

    else:
        liste = re.split("\s", text)
        elements = len(liste)
        if liste[0] == "sende" and liste[elements - 1] == "smartphone":
            nachricht = ""
            for i in range(1, elements):
                if liste[i] == "an" and liste[i + 1] == "mein":
                    break
                else:
                    nachricht += liste[i]
                    nachricht += " "

    if nachricht:
        if wrapper.messenger_call:
            wrapper.say("Du hast folgende Nachricht an dich selbst geschrieben:")
        else:
            wrapper.say("Ok, ich sende " + nachricht + " an dein Smartphone")
            wrapper.say("Nachricht an dich:", output="messenger")
        wrapper.say(nachricht, output="messenger")
    else:
        wrapper.say("Ich konnte deine Nachricht nicht heraus filtern")
