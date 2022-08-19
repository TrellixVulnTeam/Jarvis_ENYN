from src import log
from src.modules import ModuleWrapper

PRIORITY = 9


def is_valid(text):
    text = text.lower()
    return "abbruch" in text or "abbrechen" in text


def handle(text: str, wrapper: ModuleWrapper) -> None:
    log.action("Command canceled!")
