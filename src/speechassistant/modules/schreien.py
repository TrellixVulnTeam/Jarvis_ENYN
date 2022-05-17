import time


def isValid(text: str) -> bool:
    if "kannst" in text and "schreien" in text:
        return True
    return False


def handle(text, core, skills):
    core.say("Bitte trete einen Schritt zurück.")
    time.sleep(0.5)
    core.say("Und noch einen.")
    time.sleep(0.5)
    core.say("Nein.")
