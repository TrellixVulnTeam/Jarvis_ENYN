import datetime

from src.modules import ModuleWrapper


def isValid(text: str) -> bool:
    text = text.lower()
    if "ist" in text and "schaltjahr" in text:
        return True
    elif "wann" in text and "schaltjahr" in text:
        return True


def handle(text: str, wrapper: ModuleWrapper) -> None:
    text = text.lower()
    if "wann" in text and ("nächste" in text or "wieder" in text):
        year = datetime.date.today().year + 1
        while True:
            if leap_year(year) is True:
                wrapper.say("Das nächste Schaltjahr ist {}".format(year))
                break
            else:
                year += 1
    elif "ist" in text and "schaltjahr" in text:
        ist_schaltjahr = leap_year(get_year(text))
        output = "vielleicht ein"
        if ist_schaltjahr is True:
            output = "ein"
        else:
            output = "kein"
        wrapper.say("Das Jahr {} ist {} Schaltjahr.".format(get_year(text), output))
    else:
        wrapper.say(
            "Ich habe nicht verstanden, was du im Zusammenhang mit Schaltjahren wissen möchtest."
        )


def get_year(text: str):
    year = -1
    text = text.split(" ")
    for item in text:
        try:
            year = int(item)
        except ValueError:
            pass
    return year


def leap_year(y: int):
    is_leap_year = False
    if y % 400 == 0:
        is_leap_year = True
    if y % 100 == 0:
        is_leap_year = False
    if y % 4 == 0:
        is_leap_year = True
    return is_leap_year
