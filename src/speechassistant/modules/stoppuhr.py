from datetime import datetime

from src.speechassistant.resources.module_skills import Skills


def isValid(text):
    if 'stoppuhr' in text.lower():
        return True
    elif 'stopp' in text and 'zeit' in text:
        return True
    return False


def handle(text, core, skills):
    if 'start' in text:
        start(core, skills)
    elif 'stop' in text or 'beend' in text:
        stop(core, skills)
    else:
        core.say('Ich kann die Stoppuhr nur starten oder stoppen.')


def start(core: ModuleWrapper, skills: Skills):
    if 'stopwatch' in core.local_storage.keys():
        core.say('Es läuft bereits eine Stoppuhr. Soll ich diese erst stoppen?')
        if skills.is_desired(core.listen()):
            core.say('Alles klar. Die alte Stoppuhr wurde bei {} gestoppt und eine neue gestartet.'.format(
                skills.get_time(core.local_storage['stoppuhr']),
                skills.get_time_difference(core.local_storage['stoppuhr'])))
            core.local_storage['stoppuhr'] = datetime.now()
        else:
            core.say('Alles klar, die alte Stoppuhr läuft weiter.')
    else:
        core.say(
            'Alles klar, die Stoppuhr wurde um {} gestartet.'.format(skills.get_time(datetime.now())))
        core.local_storage['stoppuhr'] = datetime.now()


def stop(core: ModuleWrapper, skills: Skills):
    if 'stoppuhr' in core.local_storage.keys() and core.local_storage['stoppuhr'] != '':
        core.say('Alles klar, die Stoppuhr wurde um {} gestoppt. Sie dauerte {}.'.format(
            skills.get_time(datetime.now()),
            skills.get_time_difference(core.local_storage["stoppuhr"], datetime.now())))
        core.local_storage['stoppuhr'] = ''
    else:
        core.say('Es wurde noch keine Stoppuhr gestartet. Soll ich eine starten?')
        if skills.is_desired(core.listen()):
            core.say('Alles klar, Stoppuhr wurde um {} gestartet'.format(
                skills.get_time(datetime.now())))
            core.local_storage['stoppuhr'] = datetime.now()
