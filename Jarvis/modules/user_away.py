import random

def handle(text, core, skills):
    user = core.user
    '''farewells = ['Auf wiedersehen, {}!',
                 'Bis bald {}',
                 'Machs gut {}',
                 'Viel Spaß!']'''
    farewells = ['Bis bald, wir werden uns wiedersehen...']
    farewell = random.choice(farewells)
    if '{}' in farewell:
        farewell = farewell.format(user)
    core.say(farewell)

    # Erst den User aus allen Räumen entfernen...
    for raum in core.local_storage['rooms'].values():
        try:
            if user in raum['users']:
                raum['users'].remove(user)
        except KeyError:
            raum['users'] = []
            continue
    for raum in core.rooms.values():
        if user in raum.users:
            raum.users.remove(user)
    # ...Und den Raum aus dem User!
    try:
        if not core.local_storage['users'][user]['messenger_id'] == 0:
            core.local_storage['users'][user]['room'] = 'Telegram'
        else:
            core.local_storage['users'][user]['room'] = ''
    except:
        pass


def isValid(text):
    text = text.lower()
    if 'tschüss' in text or ('auf' in text and 'wiedersehen' in text) or ('ich' in text and 'bin' in text and 'weg' in text) or ('mach' in text and 'gut' in text):
        return True
    else:
        return False
