from src.models.user import User
from src.resources.services import PhilipsWrapper


def handle(text, core, skills):
    ton: str = text.get("Ton")
    user: User = text.get("User")
    path: str = core.path + "/modules/resources/alarm_sounds/" + ton
    try:
        if core.local_storage["module_storage"]["philips_hue"]["Bridge-Ip"] != "":
            pw: PhilipsWrapper = PhilipsWrapper(core)
            pw.wrapper("mach das Licht weiß")
    except RuntimeError:
        pass
    try:
        core.play(path=path, next=True)
    except FileNotFoundError:
        core.say("AlarmSchema! AlarmSchema! AlarmSchema! Aufstehen! Klingeling!")
    if user.first_name == "Unknown":
        core.say(
            "Guten Morgen! Ich hoffe du hast gut geschlafen und wünsche dir einen tollen Tag!"
        )
    else:
        core.say(
            f"Guten Morgen {user.first_name}! Ich hoffe du hast gut geschlafen und wünsche dir einen tollen Tag"
        )

    for routine in core.local_storage["alarm_routines"]:
        core.start_module(name="start_routine", text=routine, user=core.user)


def isValid(text):
    return False
