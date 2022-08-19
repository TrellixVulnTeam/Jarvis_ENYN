from src.modules import ModuleWrapper

PRIORITY = 1


def isValid(text: str) -> bool:
    text = text.replace(".", (""))
    text = text.replace("?", (""))
    if "wo " in text and "ist" in text:
        return True


def handle(text: str, wrapper: ModuleWrapper) -> None:
    text = text.lower()
    for user in wrapper.core.users.get_user_list(): # toDo: database query: where text contains user.alias.lower OR ...
        if (
                user.alias.lower() in text
                or user.first_name.lower() in text
                or user.last_name.lower() in text
        ):
            try:
                room = wrapper.local_storage["users"][user]["room"]
                wrapper.say(f"{user.alias} ist gerade im {room}.")
            except KeyError:
                wrapper.say(f"Ich konnte {user.alias} gerade nicht finden")
            return
    # Es wurde nach keiner Person gefragt. Vielleicht nach einer Stadt, einem Land.
    # Starten wir lieber das wo_ist_welt Modul
    wrapper.start_module(user=wrapper.user, name="wo_ist_welt", text="" + str(text))
