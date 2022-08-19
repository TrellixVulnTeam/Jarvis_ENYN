import random

from src.modules import ModuleWrapper


def isValid(text: str) -> bool:
    text = text.lower()
    return "spiel" in text and ("zahl" in text or "erraten" in text)


def handle(text: str, wrapper: ModuleWrapper) -> None:
    number = random.randrange(1000)
    guess = 0
    steps = 0

    wrapper.say(
        "Ok, lasse uns spielen. Versuche die Zufallszahl in möglichst wenigen Schritten zu erraten. Sag bitte immer nur die Zahl!"
    )

    while guess != number:
        guess = int(wrapper.listen(text="Dein Tipp:"))

        if number < guess:
            wrapper.say("Die gesuchte Zahl ist kleiner als " + str(guess))
        if number > guess:
            wrapper.say("Die gesuchte Zahl ist größer als " + str(guess))
        steps += 1

    wrapper.say("Du hast die Zahl beim " + str(steps) + ". Tipp erraten! SUPER!")
