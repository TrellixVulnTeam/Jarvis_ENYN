from src.modules import ModuleWrapper


def is_valid(text: str) -> bool:
    return False


def handle(text: str, wrapper: ModuleWrapper) -> None:
    wrapper.say(text)
