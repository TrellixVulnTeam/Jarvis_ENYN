from src.modules import ModuleWrapper
from src.modules.batches import batchMatch

PRIORITY = -1


def is_valid(text: str) -> bool:
    batch = ["[was|wie] ist die antwort"]
    return batchMatch(batch, text.lower())


def handle(text: str, wrapper: ModuleWrapper) -> None:
    wrapper.say("42")
