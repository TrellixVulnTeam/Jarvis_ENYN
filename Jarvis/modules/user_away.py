import random


def handle(text, core, skills):
    user = core.user
    farewells = ['Auf wiedersehen, {}!',
                 'Bis bald {}',
                 'Machs gut {}',
                 'Viel Spaß!']
    farewell = random.choice(farewells)
    if '{}' in farewell:
        farewell = farewell.format(user)
    core.say(farewell)


def isValid(text):
    text = text.lower()
    if 'tschüss' in text or ('auf' in text and 'wiedersehen' in text) or (
            'ich' in text and 'bin' in text and 'weg' in text) or ('mach' in text and 'gut' in text):
        return True
    else:
        return False
