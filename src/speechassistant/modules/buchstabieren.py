import time

PRIORITY = 3  # because hanoi


def isValid(text):
    text = text.lower()
    if 'buchstabier' in text or 'diktier' in text or ('wie' in text and ('geschrieben' in text or 'schreibt' in text)):
        return True
    return False


def handle(text, core, skills):
    if 'buchstabier' in text:
        word = skills.get_text_between('buchstabier', text)[0]
    elif 'diktier' in text:
        word = skills.get_text_between('diktier', text)[0]
    elif 'wie' in text and 'geschrieben' in text:
        word = skills.get_text_between('wird', text)[0]
    elif 'wie' in text and 'schreibt' in text:
        word = skills.get_text_between('man', text)[0]
    else:
        core.say("Leider habe ich nicht verstanden, was ich buchstabieren soll.")
        return

    for letter in word:
        core.say(letter)
        time.sleep(0.5)
