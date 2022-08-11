import logging

PRIORITY = 9


def isValid(text):
    text = text.lower()
    if "abbruch" in text:
        return True
    elif "abbrechen" in text:
        return True


def handle(text, core, skills):
    logging.info("[ACTION] Befehl abgebrochen")
