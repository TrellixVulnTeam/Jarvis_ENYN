import datetime

from src.modules import ModuleWrapper, skills


def is_valid(text: str) -> bool:
    if "wie" in text and ("uhr" in text or "spät" in text):
        return True
    elif "weche" in text and ("tag" in text or "datum" in text or "uhrzeit" in text):
        return True
    elif (
            "welchen tag" in text
            or "welcher tag" in text
            or "wochentag" in text
            or "datum" in text
            or "den wievielten haben wir heute" in text
            or "der wievielte ist es" in text
    ):
        return True
    elif "den wievielten haben wir heute" in text or "der wievielte ist es" in text:
        return True
    return False


def handle(text: str, core: ModuleWrapper):
    text: str = text.lower()
    now: datetime.datetime = datetime.datetime.now()
    if " uhr " in text or "spät" in text:
        core.say("Es ist " + skills.get_time(now))
    elif (
            "welchen tag" in text
            or "welcher tag" in text
            or "wochentag" in text
            or "datum" in text
            or "den wievielten haben wir heute" in text
            or "der wievielte ist es" in text
    ):
        core.say(get_day())


def get_day() -> str:
    now: datetime.datetime = datetime.datetime.now()
    weekday: int = datetime.datetime.today().weekday()
    tage: dict[int, str] = {
        0: "Montag",
        1: "Dienstag",
        2: "Mittwoch",
        3: "Donnerstag",
        4: "Freitag",
        5: "Samstag",
        6: "Sonntag",
    }

    output: str = (
            "Heute ist "
            + str(tage.get(weekday))
            + " der "
            + str(now.day)
            + "."
            + str(now.month)
            + "."
    )
    return output
