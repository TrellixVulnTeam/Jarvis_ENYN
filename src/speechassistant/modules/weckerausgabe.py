from src.speechassistant.resources.services import PhilipsWrapper


def handle(text, core, skills):
    ton = text.get('Ton')
    user = text.get('User')
    path = core.path + "/modules/resources/alarm_sounds/" + ton
    try:
        if core.local_storage['module_storage']['philips_hue']['Bridge-Ip'] != '':
            pw = PhilipsWrapper(core)
            pw.wrapper("mach das Licht weiß")
    except RuntimeError:
        pass
    try:
        core.play(path=path, next=True)
    except FileNotFoundError:
        core.say('Alarm! Alarm! Alarm! Aufstehen! Klingeling!')
    if user.get('fist_name') == 'Unknown':
        core.say('Guten Morgen! Ich hoffe du hast gut geschlafen und wünsche dir einen tollen Tag!')
    else:
        core.say('Guten Morgen {}! Ich hoffe du hast gut geschlafen und wünsche dir einen tollen Tag'.format(
            user.get('first_name')))

    for routine in core.local_storage["alarm_routines"]:
        core.start_module(name="start_routine", text=routine, user=core.user)


def isValid(text):
    return False
