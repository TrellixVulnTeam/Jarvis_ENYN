from datetime import datetime

from src.database.connection import ReminderInterface
from src.exceptions import NoMatchingEntry
from src.models import Reminder
from src.modules import ModuleWrapper

_data_base: ReminderInterface = ReminderInterface()


def is_valid(text: str) -> bool:
    text = text.lower()
    return skills.match_all(text, "erinner", "mich")


def handle(text: str, wrapper: ModuleWrapper) -> None:
    # toDo: database access

    if "lösch" in text:
        __delete_reminder(wrapper)
    else:
        __create_new_reminder(text, wrapper)


# toDo: rework __get_reminder_text
def __get_reminder_text(text: str):
    remembrall = ""
    e_ind = 0
    text = text.lower()

    if " zu " not in text:
        remembrall = text.replace("zu", "")
        remembrall = remembrall.replace(" ans ", " ")
    else:
        remembrall = text.replace(" ans ", " ")
    if " in " in text and " minuten" in text:
        remembrall = remembrall.replace(" minuten ", " ")
        remembrall = remembrall.replace(" in ", " ")
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


def __convert_time_to_output(time: datetime) -> str:
    year, month, day, hour, minute = __get_time_units(time)

    day = skills.Statics.numb_to_day_numb.get(day)
    month = skills.Statics.numb_to_month.get(str(month))
    hour = skills.Statics.numb_to_hour.get(str(hour))

    return f"{str(day)} {str(month)} um {str(hour)} Uhr {str(minute)}"


def __get_time_units(time: datetime) -> tuple[int, int, int, int, int]:
    return time.year, time.month, time.day, time.hour, time.minute


def __create_new_reminder(text, wrapper) -> None:
    reminder_text: str = __get_reminder_text(text)
    reminder_time: datetime = wrapper.analysis["datetime"]
    new_reminder: Reminder = Reminder(text=reminder_text, time=reminder_time, user_id=wrapper.user.uid)

    _data_base.create(new_reminder)
    time_for_output: str = __convert_time_to_output(reminder_time)
    __give_feedback_after_create(reminder_text, time_for_output, text, wrapper)


def __give_feedback_after_create(reminder_text, rep, text, wrapper) -> None:
    if "dass " in reminder_text:
        wrapper.say(f"Alles klar, ich sage dir am {rep} bescheid, {reminder_text}.")
    elif "ans " in text:
        wrapper.say(f"Alles klar, ich erinnere dich am {rep} ans {reminder_text}.")
    else:
        wrapper.say(f"Alles klar, ich sage dir am {rep} bescheid, dass du {reminder_text} musst.")


def __delete_reminder(wrapper) -> None:
    time: datetime = wrapper.analysis["datetime"]
    try:
        counter: int = _data_base.delete_by_datetime(time)
        __give_feedback_after_delete(counter, time, wrapper)
    except NoMatchingEntry:
        wrapper.say(f"Du hast keine Erinnerungen am {time.day}.{time.month} um {skills.get_time(time)}.")


def __give_feedback_after_delete(counter, time, wrapper) -> None:
    if counter == 1:
        wrapper.say("Ich habe eine Erinnerung am {time.day}.{time.month} um {skills.get_time(time)} gelöscht.")
    else:
        wrapper.say(
            f"Ich habe {counter} Erinnerung am {time.day}.{time.month} um {skills.get_time(time)} gelöscht.")
