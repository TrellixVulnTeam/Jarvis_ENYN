import time

from src.modules import ModuleWrapper


def isValid(text: str) -> bool:
    return "kannst" in text and "schreien" in text


def handle(text: str, wrapper: ModuleWrapper) -> None:
    wrapper.say("Bitte trete einen Schritt zurück.")
    time.sleep(0.5)
    wrapper.say("Und noch einen.")
    time.sleep(0.5)
    wrapper.say("Nein.")
