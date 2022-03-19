from datetime import datetime


def isValid(text):
    if 'stoppuhr' in text.lower():
        return True
    elif 'stopp' in text and 'zeit' in text:
        return True
    return False


def handle(text, core, skills):
    stop_watch = StopWatch(core, skills)
    if 'start' in text:
        stop_watch.start()
    elif 'stop' in text or 'beend' in text:
        stop_watch.stop()
    else:
        core.say('Ich kann die Stoppuhr nur starten oder stoppen.')
        # bald sollte noch eine Pause-Funktion hinzugefügt werden


class StopWatch:
    def __init__(self, core, skills):
        self.core = core
        self.skills = skills

    def start(self):
        if 'stopwatch' in self.core.local_storage.keys():
            self.core.say('Es läuft bereits eine Stoppuhr. Soll ich diese erst stoppen?')
            if self.skills.is_approved(self.core.listen()):
                self.core.say('Alles klar. Die alte Stoppuhr wurde bei {} gestoppt und eine neue gestartet.'.format(
                    self.skills.get_time(self.core.local_storage['stoppuhr']),
                    self.skills.get_time_difference(self.core.local_storage['stoppuhr'], self.skills)))
                self.core.local_storage['stoppuhr'] = datetime.now()
            else:
                self.core.say('Alles klar, die alte Stoppuhr läuft weiter.')
        else:
            self.core.say(
                'Alles klar, die Stoppuhr wurde um {} gestartet.'.format(self.skills.get_time(datetime.now())))
            self.core.local_storage['stoppuhr'] = datetime.now()

    def stop(self):
        if 'stoppuhr' in self.core.local_storage.keys() and self.core.local_storage['stoppuhr'] != '':
            self.core.say('Alles klar, die Stoppuhr wurde um {} gestoppt. Sie dauerte {}.'.format(
                self.skills.get_time(datetime.now()),
                self.skills.get_time_difference(self.core.local_storage["stoppuhr"], datetime.now())))
            self.core.local_storage['stoppuhr'] = ''
        else:
            self.core.say('Es wurde noch keine Stoppuhr gestartet. Soll ich eine starten?')
            if self.skills.is_approved(self.core.listen()):
                self.core.say('Alles klar, Stoppuhr wurde um {} gestartet'.format(
                    self.skills.get_time(datetime.now())))
                self.core.local_storage['stoppuhr'] = datetime.now()
