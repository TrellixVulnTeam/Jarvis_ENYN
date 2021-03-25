import os

def handle(text, core, skills):
    ton = text.get('Ton')
    user = text.get('User')
    path = core.path + "/modules/resources/clock_sounds/" + ton
    
    if core.local_storage['module_storage']['phillips_hue']['Bridge-IP'] != '':
        core.start_module(name='phillips_hue', text='Mach das Licht weiß')
    try:
        core.play(path=path, next=True)
    except FileNotFoundError:
        pass
    if user.get('fist_name') == 'Unknown':
        core.say('Guten Morgen! Ich hoffe du hast gut geschlafen und wünsche dir einen tollen Tag!')
    else:
        core.say('Guten Morgen {}! Ich hoffe du hast gut geschlafen und wünsche dir einen tollen Tag'.format(user.get('first_name')))

def isValid(text):
    return False
