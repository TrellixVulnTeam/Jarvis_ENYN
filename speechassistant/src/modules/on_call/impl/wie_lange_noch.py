from datetime import date, datetime

from src.models import User
from src.modules import ModuleWrapper, skills


def isValid(text: str) -> bool:
    text = text.lower()
    if "timer" in text:
        return False
    elif (
        "wie" in text
        and ("weit" in text or "lange") in text
        and ("noch" in text or "bis" in text)
    ):
        return True
    return False


def handle(text: str, wrapper: ModuleWrapper) -> None:
    text = text.lower()
    now = datetime.now()
    if "weihnachten" in text:
        target_date = date(now.year, 12, 24)
        targets_name = "Weihnachten"
    elif "geburtstag" in text:
        if "von" in text:
            user = text.split(" ")[skills.get_word_index(text, "von") + 1]
            target_date = get_birthday_date_from_name(
                wrapper.local_storage["birthdays"].get(user)
            )
            targets_name = user.capitalize() + " Geburtstag"
        elif wrapper.user is None:
            user = wrapper.listen(
                text="Von wessen Geburtstag sprichst du? Antworte bitte nicht im Genitiv und nur den "
                "Namen!"
            )
            target_date = get_birthday_date_from_name(user["date_of_birth"])
            targets_name = user.capitalize() + " Geburtstag"
        else:
            target_date = get_birthday_date_from_name(wrapper.user)
            targets_name = "zu deinem Geburtstag"
    elif "silvester" in text or ("neu" in text and "jahr" in text):
        target_date = date(now.year, 12, 31)
        targets_name = "Silvester"
    else:
        wrapper.say(
            "Ich habe nicht ganz verstanden, von welchem Ereignis du die Zeitdifferenz wissen möchtest. Versuch "
            "es doch nochmal mit anderen Worten. Beachte, dass ich dir bisher die Zeitdifferenz nur zu "
            "Geburtstagen, Weihnachten und bis Silvester sagen kann."
        )
        return
    time_delta = target_date - now.date()
    wrapper.say("Bis " + targets_name + " sind es noch " + str(time_delta.days) + " Tage!")


def get_birthday_date_from_name(user: User):
    birthday: date = user.birthday
    return date(birthday.year, birthday.month, birthday.day)
