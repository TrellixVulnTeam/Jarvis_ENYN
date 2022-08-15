from ModuleWrapper import ModuleWrapper
from src.resources import Skills

PRIORITY = 1


def isValid(text):
    text = text.replace(".", (""))
    text = text.replace("?", (""))
    if "wo " in text and "ist" in text:
        return True


def handle(text: str, core: ModuleWrapper, skills: Skills):
    text = text.lower()
    for user in core.core.users:
        if (
                user.alias.lower() in text
                or user.first_name.lower() in text
                or user.last_name.lower() in text
        ):
            try:
                room = core.local_storage["users"][user]["room"]
                core.say(f"{user.alias} ist gerade im {room}.")
            except KeyError:
                core.say(f"Ich konnte {user.alias} gerade nicht finden")
            return
    # Es wurde nach keiner Person gefragt. Vielleicht nach einer Stadt, einem Land.
    # Starten wir lieber das wo_ist_welt Modul
    core.start_module(user=core.user, name="wo_ist_welt", text="" + str(text))
