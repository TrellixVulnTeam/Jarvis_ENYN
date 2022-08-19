from src.modules import ModuleWrapper

SECURE = True


def is_valid(text: str) -> bool:
    return text.lower().startswith("wiederhole")


def handle(text: str, wrapper: ModuleWrapper) -> None:
    wrapper.say(str(" ".join(text.split(" ")[1:])), output="messenger_speech")
