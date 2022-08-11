from datetime import datetime

from src.core import ModuleWrapper
from src.resources import Skills


def isValid(text):
    text = text.lower()
    if "erinner" in text or "erinnere" in text:
        return True
    else:
        return False


# toDo: rework get_text
def get_text(core, text):
    remembrall = ""
    e_ind = 0
    text = text.lower()

    if " zu " not in text:
        remembrall = text.replace("zu", (""))
        remembrall = remembrall.replace(" ans ", (" "))
    else:
        remembrall = text.replace(" ans ", (" "))
    if " in " in text and " minuten" in text:
        remembrall = remembrall.replace(" minuten ", (" "))
        remembrall = remembrall.replace(" in ", (" "))
        s = str.split(remembrall)
        for t in s:
            try:
                if int(t) >= 0:
                    remembrall = remembrall.replace(t, (""))
            except ValueError:
                remembrall = remembrall
    satz = {}
    ausgabe = ""
    ind = 1
    i = str.split(remembrall)
    for w in i:
        satz[ind] = w
        ind += 1
    if " am " in satz.items():
        for index, word in satz.items():
            if word == "am":
                am_ind = index
                try:
                    if int(satz.get(am_ind + 2)):
                        summand = 3
                        for i, w in satz.items():
                            try:
                                ausgabe = ausgabe + satz.get(am_ind + summand) + " "
                                summand += 1
                            except TypeError:
                                ausgabe = ausgabe
                except (ValueError, TypeError):
                    summand = 2
                    for i, w in satz.items():
                        try:
                            ausgabe = ausgabe + satz.get(am_ind + summand) + " "
                            summand += 1
                        except TypeError:
                            ausgabe = ausgabe
    elif " daran dass" in text:
        for ind, w in satz.items():
            if w == "daran":
                reminder = ""
                n = 1
                try:
                    try:
                        while n < 30:
                            if satz.get(ind + n) != None:
                                reminder = reminder + str(satz.get(ind + n)) + " "
                                n += 1
                            else:
                                reminder = reminder
                                break
                    except KeyError:
                        reminder = reminder
                        break
                except ValueError:
                    reminder = reminder
                    break
                ausgabe = reminder
    else:
        for index, word in satz.items():
            if word == "erinner" or word == "erinnere":
                e_ind = index
                s_ind = e_ind + 2
                ausgabe = satz.get(s_ind) + " "
                summand = 1
                for i, w in satz.items():
                    try:
                        ausgabe = ausgabe + satz.get(s_ind + summand) + " "
                        summand += 1
                    except TypeError:
                        ausgabe = ausgabe
    ausgabe = ausgabe.replace("übermorgen ", (" "))
    ausgabe = ausgabe.replace("morgen ", (" "))
    ausgabe = ausgabe.replace("daran ", (" "))
    ausgabe = ausgabe.replace("ich", ("du"))
    ausgabe = ausgabe.replace("mich", ("dich"))
    if "dass " in text:
        lang = len(ausgabe)
        if ausgabe[(lang - 1):] == " ":
            ausgabe = ausgabe[: (lang - 1)]
        l = len(ausgabe)
        if ausgabe[(l - 2):] == "st":
            ausgabe = ausgabe
        elif ausgabe[(l - 1):] == "s":
            ausgabe = ausgabe + "t"
        else:
            ausgabe = ausgabe + "st"
    return ausgabe


def get_reply_time(core, dicanalyse):
    time = dicanalyse.get("time")
    jahr = str(time["year"])
    monat = str(time["month"])
    tag = str(time["day"])
    stunde = str(time["hour"])
    minute = str(time["minute"])
    if int(minute) <= 9:
        minute = "0" + minute
    if int(monat) <= 9:
        monat = "0" + monat

    if minute[0] == "0":
        mine = minute[1]
        if mine == "0":
            mine = ""
        else:
            mine = mine
    else:
        mine = minute
    day = core.skills.Statics.numb_to_day_numb.get(tag)
    month = core.skills.Statics.numb_to_month.get(str(monat))
    hour = core.skills.Statics.numb_to_hour.get(str(stunde))
    zeit_der_erinnerung = (
            str(day) + " " + str(month) + " um " + str(hour) + " Uhr " + str(mine)
    )
    reply = zeit_der_erinnerung
    return reply


def handle(text: str, core: ModuleWrapper, skills: Skills):
    if "lösch" in text:
        time: datetime = core.analysis["datetime"]
        erinnerungen = core.local_storage["Erinnerungen"]

        counter: int = core.data_base.reminder_interface.delete_reminder()
        if counter == 0:
            core.say(
                f"Du hast keine Erinnerungen am {time.day}.{time.month} um {skills.get_time(time)}."
            )
        elif counter == 1:
            core.say(
                "Ich habe eine Erinnerung am {time.day}.{time.month} um {skills.get_time(time)} gelöscht."
            )
        else:
            core.say(
                f"Ich habe {counter} Erinnerung am {time.day}.{time.month} um {skills.get_time(time)} gelöscht."
            )

    else:
        reminder_text: str = get_text(core, text)
        core.data_base.reminder_interface.add_reminder(
            reminder_text, core.analysis["datetime"], core.user
        )

        rep = get_reply_time(core, core.analysis)
        if "dass " in reminder_text:
            antwort = (
                    "Alles klar, ich sage dir am "
                    + rep
                    + " bescheid, "
                    + reminder_text
                    + "."
            )  ###
        elif "ans " in text:
            antwort = (
                    "Alles klar, ich erinnere dich am "
                    + rep
                    + " ans "
                    + reminder_text
                    + "."
            )
        else:
            antwort = (
                    "Alles klar, ich sage dir am "
                    + rep
                    + " bescheid, dass du "
                    + reminder_text
                    + " musst."
            )
        core.say(antwort)
