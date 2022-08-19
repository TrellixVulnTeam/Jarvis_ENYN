import random

from src.modules import ModuleWrapper, skills


def is_valid(text: str) -> bool:
    return "wie" in text and "geht" in text and "dir" in text


def handle(text: str, wrapper: ModuleWrapper) -> None:
    answers = [
        "Danke, gut!",
        "Mir gehts gut, {}.".format(wrapper.user["name"]),
        "Alles gut, {}.".format(wrapper.user["name"]),
    ]
    reply = wrapper.listen(text=random.choice(answers) + "Und wie geht es dir?").lower()
    if skills.match_any(reply, "schlecht", "müde", "mies", "suboptimal") or "nicht" in text and not "schlecht" in text:
        wrapper.say("Das ist blöd, aber denk immer daran: Alles hat ein Ende nur die Wurst hat zwei!")
    elif skills.match_any(reply, "gut", "besser", "bestens", "super", "wundervoll", "glücklich", "froh"):
        wrapper.say("Das freut mich!")
    else:
        wrapper.say("Ich fürchte, ich konnte dich nicht verstehen. Geht es dir so schlecht?")
