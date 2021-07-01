import datetime
import logging


def isValid(text):
    return False
    # toDo


def handle(text, core, skills):
    timer = Timer(core, skills)
    if 'stell' in text or 'beginn' in text:
        timer.create_timer(text)
    elif 'wie' in text and 'lange' in text:
        core.say(timer.get_remain_duration())
    elif 'lösch' in text or 'beend' in text or 'stopp' in text:
        timer.delete_timer()


class Timer:
    def __init__(self, core, skills):
        self.core = core
        self.skills = skills

    def create_timer(self, text):
        time = self.core.Analyzer.analyze(text)['datetime']
        temp_text = "Dein Timer ist abgelaufen."
        duration = self.get_duration(text)
        if duration is None:
            return
        # Zeit: Um wieviel Uhr der Timer fertig ist; Text: Antwort von Core; Benutzer; Raum; Dauer: Wie lange der
        # Timer gehen soll
        E_eins = {'Zeit': time, 'Text': temp_text, 'Dauer': duration, 'Benutzer': self.core.user}

        # Vermeidung von Redundanz. Wird für 1 und mehrere Timer verwendet
        # Aufzählung wenn mehrere Timer
        if 'Timer' in self.core.local_storage.keys():
            self.core.local_storage['Timer'].append(E_eins)
            anzahl = len(self.core.local_storage['Timer'])
            self.core.say(str(anzahl) + '. Timer: ' + str(E_eins['Dauer']) + ' ab jetzt.')
        else:
            self.core.local_storage['Timer'] = [E_eins]
            self.core.say(str(E_eins['Dauer']) + ' ab jetzt.')

    def get_duration(self, text):
        text = text.replace(' auf ', ' in ')
        text = text.replace(' von ', ' in ')
        duration = self.skills.get_text_beetween('in', text, output='String')
        if duration is "":
            self.core.say('Ich habe nicht verstanden, wie lange der Timer dauern soll. Bitte versuche es erneut!')
            return None
        return duration

    def get_remain_duration(self):
        # Begrenzt Timer auf die des Benutzers
        user_timer = self.core.local_storage['Timer']
        timer_enum = ''

        if len(user_timer) == 0:
            timer_enum = "Du hast keinen aktiven Timer!"
        else:
            for item in user_timer:
                self.delete_timer_if_passed(user_timer, item)

                # Verbleibende Zeit runden
                specific_time = item['Zeit'] - datetime.datetime.now()

                days = specific_time.days
                seconds = specific_time.seconds

                # Wenn Timer kurz vor Ende, dann überspringen
                if days == 0 and seconds < 3:
                    continue

                seconds = specific_time.seconds

                if (seconds % 60) >= 30:
                    seconds += 60 - (seconds % 60)
                if seconds > 30:
                    seconds += 60 - (seconds % 60)

                remaining_time = datetime.timedelta()

                timer_enum += 'Du hast einen ' + item['Dauer'] + ' mit noch etwa ' \
                                 + self.get_time_differenz(remaining_time) + ' verbleibend.\n'

            if len(user_timer) > 1:
                output = 'Du hast ' + str(len(self.core.local_storage['Timer'])) + ' Timer gestellt.\n' + timer_enum
        return output

    def delete_timer_if_passed(self, user_timer, item):
        try:
            # erst einmal checken, ob der Timer vlt eigentlich schon abgelaufen ist,
            # was eigentlich nicht passieren sollte.
            now = datetime.datetime.now()
            timer_abgelaufen = (now - item["Zeit"])
            if timer_abgelaufen:
                user_timer.remove(item)
                self.core.local_storage["Timer"].remove(item)
        except:
            # local_storage doesn´t extend this timer. Just write this into the Log
            logging.info("WARNING", 'Not existing timer could not be deleted')

    def delete_timer(self):
        self.core.say('Diese Funktion wird derzeit auf das Webinterface ausgelagert.')

    @staticmethod
    def get_time_differenz(start_time, time=datetime.datetime.now()):
        aussage = []
        if time == None:
            dz = start_time
        else:
            dz = start_time - time
        days = dz.days
        seconds = dz.seconds
        microseconds = dz.microseconds

        years = 0
        hours = 0
        minutes = 0

        if days >= 365:
            years = int(days / 365)
            days = days % 365
        if seconds >= 3600:
            hours = int(seconds / 3600)
            seconds = seconds % 3600
        if seconds >= 60:
            minutes = int(seconds / 60)
            seconds = seconds % 60
        if microseconds >= 5:
            seconds += 1

        if years == 1:
            aussage.append('einem Jahr')
        elif years > 1:
            aussage.append(str(years) + ' Jahren')
        if days == 1:
            aussage.append('einem Tag')
        elif days > 1:
            aussage.append(str(days) + ' Tagen')
        if hours == 1:
            aussage.append('einer Stunde')
        elif hours > 1:
            aussage.append(str(hours) + ' Stunden')
        if minutes == 1:
            aussage.append('einer Minute')
        elif minutes > 1:
            aussage.append(str(minutes) + ' Minuten')
        if seconds == 1:
            aussage.append('einer Sekunde')
        elif seconds > 1:
            aussage.append(str(seconds) + ' Sekunden')
        return skills.get_enumerate(aussage)