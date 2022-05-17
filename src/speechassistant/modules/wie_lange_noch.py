from datetime import date, datetime


def isValid(text):
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


def handle(text, core, skills):
    text = text.lower()
    now = datetime.now()
    if "weihnachten" in text:
        target_date = date(now.year, 12, 24)
        targets_name = "Weihnachten"
    elif "geburtstag" in text:
        if "von" in text:
            user = text.split(" ")[skills.get_word_index(text, "von") + 1]
            target_date = get_birthday_date_from_name(
                core.local_storage["birthdays"].get(user)
            )
            targets_name = user.capitalize() + " Geburtstag"
        elif core.user is None:
            user = core.listen(
                text="Von wessen Geburtstag sprichst du? Antworte bitte nicht im Genitiv und nur den "
                "Namen!"
            )
            target_date = get_birthday_date_from_name(user["date_of_birth"])
            targets_name = user.capitalize() + " Geburtstag"
        else:
            user_birthday = core.user["date_of_birth"]
            target_date = get_birthday_date_from_name(user_birthday)
            targets_name = "zu deinem Geburtstag"
    elif "silvester" in text or ("neu" in text and "jahr" in text):
        target_date = date(now.year, 12, 31)
        targets_name = "Silvester"
    else:
        core.say(
            "Ich habe nicht ganz verstanden, von welchem Ereignis du die Zeitdifferenz wissen möchtest. Versuch "
            "es doch nochmal mit anderen Worten. Beachte, dass ich dir bisher die Zeitdifferenz nur zu "
            "Geburtstagen, Weihnachten und bis Silvester sagen kann."
        )
        return
    time_delta = target_date - now.date()
    core.say("Bis " + targets_name + " sind es noch " + str(time_delta.days) + " Tage!")


def get_birthday_date_from_name(user_birthday):
    year = user_birthday["year"]
    month = user_birthday["month"]
    day = user_birthday["day"]
    return date(year, month, day)
