from src import log

PRIORITY = 9


def isValid(text):
    text = text.lower()
    if "abbruch" in text:
        return True
    elif "abbrechen" in text:
        return True


def handle(text, core, skills):
    log.action("Command canceled!")
