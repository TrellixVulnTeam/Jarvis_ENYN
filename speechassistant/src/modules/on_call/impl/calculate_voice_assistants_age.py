import datetime

from src.modules import skills, ModuleWrapper


def isValid(text: str) -> bool:
    return skills.match_all(text, "wie", "alt", "du") or skills.match_all(text, "seit", "wann", "dich")


def handle(text: str, wrapper: ModuleWrapper) -> None:
    birthday = datetime.datetime.strptime("6 Mai 2020", "%d %b %Y")
    output: str = skills.get_time_difference(birthday)
    wrapper.say(f"Es sind {output} seit den ersten Tests!")
