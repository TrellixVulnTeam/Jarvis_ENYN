from time import sleep

from src.modules import ModuleWrapper


def is_valid(text: str) -> bool:
    if "countdown" in text.lower():
        return True
    elif "zähl" in text.lower() and "runter" in text.lower():
        return True
    return False


def handle(text: str, wrapper: ModuleWrapper) -> None:
    word_bag: list[str] = text.lower().split(" ")
    time_in_seconds = 0
    for index, item in enumerate(word_bag):
        if "sekunde" in item:
            time_in_seconds += word_bag[index - 1]
        elif "minute" in item:
            time_in_seconds += word_bag[index - 1] * 60
        elif "stunde" in item:
            if "nein" in wrapper.listen(text="Ist das nicht ein bisschen zu lang?"):
                time_in_seconds += word_bag[index - 1] * 3600

    if time_in_seconds == 0:
        wrapper.say(
            "Tut mir leid, leider habe ich nicht verstanden, von wo ich herunter zählen soll"
        )
    else:
        while time_in_seconds > 0:
            wrapper.say(str(time_in_seconds))
            time_in_seconds -= 1
            sleep(1)
