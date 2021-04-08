import time

SECURE = False
#toDo Asynchronus say
def reload_own(core):
    print('\n\n--------- RELOAD ---------')
    # Eigene Module neu laden
    core.core.Modules.stop_continuous()
    core.core.Modules.load_modules()
    core.core.Modules.start_continuous()

def handle(text, core, skills):
    #core.say('Okay, warte einen Moment')
    reload_own(core)
    print('--------- FERTIG ---------\n\n')
    core.say('Die Module wurden neu geladen.')


def isValid(text):
    text = text.lower()
    if ('lad' in text or 'nadel' in text or 'load' in text) and ('module' in text or 'Duden' in text):
        return True
    else:
        return False
