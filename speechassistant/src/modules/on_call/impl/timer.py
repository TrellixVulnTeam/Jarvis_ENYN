from __future__ import annotations

from datetime import datetime

from src.enums import OutputTypes
from src.modules import ModuleWrapper, skills

PRIORITY = 2  # Conflicts with module "wie_lange_noch"


# toDo: refactor and using database

def isValid(text: str) -> bool:
    text = text.lower()
    if "timer" in text:
        if "stell" in text or "beginn" in text:
            return True
        elif "wie" in text and "lange" in text:
            return True
        elif "lösch" in text or "beend" in text or "stopp" in text:
            return True
    return False


def handle(text: str, core: ModuleWrapper):
    timer_interface = core.data_base.timer_interface
    if "stell" in text or "beginn" in text:
        create_timer(core, text)
    elif "wie" in text and "lange" in text:
        core.say(get_remain_duration())
    elif "lösch" in text or "beend" in text or "stopp" in text:
        delete_timer(core)


def create_timer(
        core: ModuleWrapper, text: str
) -> None:
    # replace "auf" zu "in", damit die Analyze-Funktion funktioniert
    text = text.replace(" auf ", " in ")
    target_time: datetime = core.analyzer.analyze(text)["datetime"]
    timer_text: str = "Dein Timer ist abgelaufen."
    duration = get_duration(core, skills, text)
    if duration is None:
        return

    # Vermeidung von Redundanz. Wird für ein und mehrere Timer verwendet
    # Aufzählung wenn mehrere Timer
    position: int = timer_interface.add_timer(
        target_time, timer_text, user_id=core.user.get("id")
    )
    if not core.messenger_call:
        temp_text = core.skills.statics.numb_to_ordinal[position]
    else:
        temp_text = str(position) + "."
    core.say(temp_text + " Timer: " + str(duration) + " ab jetzt.")


def get_duration(core, skills, text: str) -> str | None:
    text = text.replace(" auf ", " in ")
    text = text.replace(" von ", " in ")
    duration = skills.get_text_between("in", text, output="String")
    if duration is "":
        core.say(
            "Ich habe nicht verstanden, wie lange der Timer dauern soll. Bitte versuche es erneut!"
        )
        return None
    return duration


def get_remain_duration() -> str:
    timer_interface.delete_passed_timer()
    # Just query timer from user
    # user_timer = self.timer_interface.get_timer_of_user(self.core.user['id'])
    user_timer = timer_interface.get_all_timer(output_type=OutputTypes.TUPLE)
    output = ""

    if len(user_timer) == 0:
        output = "Du hast keinen aktiven Timer!"
    else:
        if len(user_timer) > 1:
            output = f"Du hast {str(len(user_timer))} Timer gestellt.\n  "

        for timer_id, duration, time, text, uid in user_timer:
            output += (
                    duration
                    + "Timer mit "
                    + skills.get_time_difference(datetime.now(), time)
                    + " verbleibend.\n "
            )
    return output


def delete_timer(core: ModuleWrapper) -> None:
    core.say("Diese Funktion wird derzeit auf das Webinterface ausgelagert.")
