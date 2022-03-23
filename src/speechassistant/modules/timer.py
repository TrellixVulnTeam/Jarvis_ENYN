from __future__ import annotations

from datetime import datetime
import logging

from src.speechassistant.core import ModuleWrapper
from src.speechassistant.resources.module_skills import Skills
from src.speechassistant.resources.enums import OutputTypes

PRIORITY = 2  # Conflicts with module "wie_lange_noch"


def isValid(text):
    text = text.lower()
    if 'timer' in text:
        if 'stell' in text or 'beginn' in text:
            return True
        elif 'wie' in text and 'lange' in text:
            return True
        elif 'lösch' in text or 'beend' in text or 'stopp' in text:
            return True
    return False


def handle(text, core, skills):
    timer = Timer(core, skills)
    if 'stell' in text or 'beginn' in text:
        timer.create_timer(text)
    elif 'wie' in text and 'lange' in text:
        core.say(timer.get_remain_duration())
    elif 'lösch' in text or 'beend' in text or 'stopp' in text:
        timer.delete_timer()


class Timer:

    def __init__(self, core: ModuleWrapper, skills: Skills):
        self.core: ModuleWrapper = core
        self.timer_interface = self.core.data_base.timer_interface
        self.skills: Skills = skills

    def create_timer(self, text: str) -> None:
        # replace "auf" zu "in", damit die Analyze-Funktion funktioniert
        text = text.replace(' auf ', ' in ')
        target_time: datetime = self.core.Analyzer.analyze(text)['datetime']
        timer_text: str = "Dein Timer ist abgelaufen."
        duration = self.get_duration(text)
        if duration is None:
            return

        # Vermeidung von Redundanz. Wird für ein und mehrere Timer verwendet
        # Aufzählung wenn mehrere Timer
        position: int = self.timer_interface.add_timer(target_time, timer_text, user_id=self.core.user.get('id'))
        if not self.core.messenger_call:
            temp_text = self.core.skills.statics.numb_to_ordinal[position]
        else:
            temp_text = str(position) + "."
        self.core.say(temp_text + ' Timer: ' + str(duration) + ' ab jetzt.')

    def get_duration(self, text: str) -> str | None:
        text = text.replace(' auf ', ' in ')
        text = text.replace(' von ', ' in ')
        duration = self.skills.get_text_between('in', text, output='String')
        if duration is "":
            self.core.say('Ich habe nicht verstanden, wie lange der Timer dauern soll. Bitte versuche es erneut!')
            return None
        return duration

    def get_remain_duration(self) -> str:
        self.timer_interface.delete_passed_timer()
        # Just query timer from user
        # user_timer = self.timer_interface.get_timer_of_user(self.core.user['id'])
        user_timer = self.timer_interface.get_all_timer(output_type=OutputTypes.TUPLE)
        output = ''

        if len(user_timer) == 0:
            output = "Du hast keinen aktiven Timer!"
        else:
            if len(user_timer) > 1:
                output = f'Du hast {str(len(user_timer))} Timer gestellt.\n  '

            for timer_id, duration, time, text, uid in user_timer:
                output += duration + 'Timer mit ' + self.skills.get_time_difference(datetime.now(),
                                                                                    time) + ' verbleibend.\n '
        return output

    def delete_timer(self) -> None:
        self.core.say('Diese Funktion wird derzeit auf das Webinterface ausgelagert.')
