import time

SECURE = False
#toDo Asynchronus say
def reload_own(luna):
    print('\n\n--------- RELOAD ---------')
    # Eigene Module neu laden
    luna.core.Modules.stop_continuous()
    luna.core.Modules.load_modules()
    luna.core.Modules.start_continuous()

def handle(text, luna, profile):
    #luna.say('Okay, warte einen Moment')
    reload_own(luna)
    print('--------- FERTIG ---------\n\n')
    luna.say('Die Module wurden neu geladen.')


def isValid(text):
    text = text.lower()
    if ('lad' in text or 'nadel' in text or 'load' in text) and ('module' in text or 'Duden' in text):
        return True
    else:
        return False
