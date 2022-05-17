import datetime
import logging
import traceback

from src.speechassistant.core import ModuleWrapper
from src.speechassistant.resources.module_skills import Skills


def isValid(text: str) -> bool:
    return "weck" in text.lower()


def handle(text: str, core: ModuleWrapper, skills: Skills):
    alarm: Alarm = Alarm(core)

    """
            if core.analysis["time"] is None:
            if not (' um ' in text or ' in ' in text):
                response_time = core.listen(text='Um wie viel Uhr möchtest du geweckt werden?')
            else:
                response_time = core.listen(text='Bitte wiederhole, wann du geweckt werden möchtest.')
        else:
            response_time = text
    """

    if (
        "abends" not in text
        or "abend" not in text
        or not ("spät" in text and "Stunde" in text)
        or not ("in" in text and ("stunde" in text or "minute" in text))
    ):
        # Alarm clocks are usually set for the morning. Since there are otherwise problems with analyze, the morning is
        # automatically assumed here if evening is not explicitly meant.
        text += " morgens"

    regular: bool = is_regular(text)
    time: datetime.datetime = core.analysis["time"]
    repeating: list[dict] = get_repeating(text, skills)

    if "lösch" in text or "beend" in text or ("schalt" in text and "ab" in text):
        try:
            alarm.delete_alarm(repeating, regular, time=time)
        except ValueError:
            core.say(
                "Es gab einen fatalen internen Error in dem Modul Wecker. Am besten du meldest den Fehler, "
                "damit das Modul so schnell wie möglich wieder funktionsfähig ist."
            )
    else:
        # days, repeat, time=None, hour=None, minute=None, text=None, sound=None
        alarm.create_alarm(regular, time)
        core.say(alarm.get_reply(text, time, regular))


def is_regular(text: str) -> bool:
    text = text.lower()
    if ("jeden" in text or "immer" in text) and not (
        "nur am" in text or "nur an dem" in text
    ):
        return True
    else:
        return False


def get_repeating(text: str, skills: Skills) -> list[dict]:
    text: str = text.lower()
    repeating: list[dict] = []

    if (
        "täglich" in text
        or "jeden tag" in text
        or "alle" in text
        or "jeden morgen" in text
        or "jeden abend" in text
    ):
        repeating = [
            {each_day.lower(): True} for each_day in skills.statics.weekdays_engl
        ]
    elif "wochentag" in text or "unter der woche" in text:
        # add monday - friday (as True values)
        for i in range(5):
            repeating.append({skills.statics.weekdays_engl[i].lower(): True})
        # add saturday and sunday (as False values)
        for i in [6, 7]:
            repeating.append({skills.statics.weekdays_engl[i].lower(): False})
    elif "wochenende" in text:
        # add monday - friday (as False values)
        for i in range(5):
            repeating.append({skills.statics.weekdays_engl[i].lower(): False})
        # add saturday and sunday (as True values)
        for i in [6, 7]:
            repeating.append({skills.statics.weekdays_engl[i].lower(): True})
    else:
        for item in skills.statics.weekdays:
            if item.lower() in text:
                repeating.append(
                    {skills.statics.weekdays_ger_to_eng[item.lower()]: True}
                )
            else:
                repeating.append(
                    {skills.statics.weekdays_ger_to_eng[item.lower()]: False}
                )
    if repeating is []:
        repeating = [
            {each_day.lower(): False} for each_day in skills.statics.weekdays_engl
        ]
    return repeating


def get_time_stamp(hour: int, minute: int) -> str:
    hour = str(hour)
    minute = str(minute)

    if len(hour) == 1:
        hour = "0" + hour
    if len(minute) == 1:
        minute = "0" + minute

    return f"{hour}:{minute}Uhr"


class Alarm:
    def __init__(self, core: ModuleWrapper) -> None:
        self.core: ModuleWrapper = core
        self.local_storage: dict = core.local_storage
        self.skills: Skills = core.skills
        self.alarm_interface = self.core.data_base.alarm_interface

        self.user: dict
        self.days: dict
        self.repeat: dict
        self.text: dict
        self.list: dict

    def create_alarm(
        self,
        is_regular: bool,
        time: dict = None,
        hour: int = None,
        minute: int = None,
        text: str = None,
        sound: str = None,
    ) -> None:
        if not (time is not None or (hour is not None and minute is not None)):
            raise ValueError("missing values!")
        if time is not None:
            hour: int = time["hour"]
            minute: int = time["minute"]
        if self.core.user is not None:
            alarm_sound: str = self.core.user["alarm_sound"]
            user_id: int = self.core.user.get("id")
            user_name: str = f', {self.core.user["first_name"].capitalize()}'
        else:
            alarm_sound: str = "standart.wav"
            user_id: int = -1
            user_name: str = ""
        if text is None:
            text: str = (
                f"Alles Gute zum Geburtstag{user_name}!"
                if self.is_birthday()
                else f"Guten Morgen{user_name}!"
            )
        if sound is not None:
            alarm_sound: str = sound
        total_seconds: int = int(hour) * 3600 + int(minute) * 60
        time: dict = {"hour": hour, "minute": minute, "total_seconds": total_seconds}
        repeating: list[dict] = get_repeating(text, self.skills)
        repeating.append({"regular": is_regular})
        self.alarm_interface.add_alarm(time, text, user_id, repeating, song=alarm_sound)
        self.core.say(
            self.get_reply(text, time, repeating[len(repeating) - 1]["regular"])
        )

    def delete_alarm(self, days, repeat, time=None, hour=None, minute=None):
        self.core.say("Die Löschfunktion wird derzeit auf die Website ausgelagert.")

    def is_birthday(self) -> bool:
        if self.core.user:
            birth_date = self.core.user["date_of_birth"]
            today = datetime.datetime.today()
            if birth_date["month"] == today.month and birth_date["day"] == today.day:
                return True
        return False

    def get_reply(self, text: str, time: dict, is_regular: bool) -> str:
        output = "Wecker gestellt "

        now = datetime.datetime.now()
        if is_regular:
            if time["day"] == now.day:
                output += "für heute"
            elif time["day"] == (now.day + 1):
                output += "für morgen"
            else:
                output += "am " + time["day"] + "." + time["month"]
        else:
            output += "für jeden "

            for item in self.skills.statics.weekdays:
                if item.lower() in text.lower():
                    output += item
                    break

        output += " um " + self.skills.get_time(time)
        return output
