PRIORITY = 1

def isValid(text):
    text = text.replace('.', (''))
    text = text.replace('?', (''))
    if 'wo ' in text and 'ist' in text:
        return True
        
def handle(text, core, skills):
    for user in core.userlist:
        if user.lower() in text.lower():
            try:
                room = core.local_storage['users'][user]['room']
                core.say('{} ist gerade im {}.'.format(user, room))
            except KeyError:
                core.say('Ich konnte {} gerade nicht finden'.format(user))
            return
    # Es wurde nach keiner Person gefragt. Vielleicht nach einer Stadt, einem Land.
    # Starten wir lieber das wo_ist_welt Modul
    # Wir hängen noch ein '§DIRECTCALL_FROM_WO_IST§' an.
    core.start_module(user = core.user, name = "wo_ist_welt", text = '§DIRECTCALL_FROM_WO_IST§' + str(text))
