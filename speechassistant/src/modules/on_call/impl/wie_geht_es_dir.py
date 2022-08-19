import random

from src.modules import ModuleWrapper


def isValid(text: str) -> bool:
    text = text.lower()
    if "wie" in text and (
        ("geht" in text and "dir" in text)
        or "läuft" in text
        or "geht's" in text
        or "gehts" in text
    ):
        return True
    else:
        return False


def handle(text: str, wrapper: ModuleWrapper) -> None:
    answers = [
        "Danke, gut!",
        "Mir gehts gut, {}.".format(wrapper.user.first_name),
        "Alles gut, {}.".format(wrapper.user.first_name),
    ]
    reply = wrapper.listen(text=random.choice(answers) + "Und wie geht es dir?").lower()
    if (
        "nicht so" in reply
        or "schlecht" in reply
        or "müde" in reply
        or "mies" in reply
        or "suboptimal" in reply
    ):
        wrapper.say(
            "Das ist blöd, aber denk immer daran: Alles hat ein Ende nur die Wurst hat zwei!"
        )
    elif (
        "gut" in reply
        or "besser" in reply
        or "bestens" in reply
        or "super" in reply
        or "wundervoll" in reply
        or "glücklich" in reply
        or "froh" in reply
    ):
        wrapper.say("Das freut mich!")
    else:
        wrapper.say(
            "Ich fürchte, ich konnte dich nicht verstehen. Geht es dir so schlecht?"
        )
