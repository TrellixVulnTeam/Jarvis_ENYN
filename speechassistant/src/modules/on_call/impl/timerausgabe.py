from src.modules import ModuleWrapper


def handle(text: dict, core: ModuleWrapper):
    duration = text.get("Dauer")
    core.say("Dein Timer von {} ist abgelaufen!".format(duration))
    if not core.messenger_call:
        core.say(
            "Dein Timer von {} ist abgelaufen!".format(duration), output="messenger"
        )


def isValid(text: str) -> bool:
    return False
