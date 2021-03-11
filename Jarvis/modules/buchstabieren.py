import time

def isValid(text):
    text = text.lower()
    if 'buchstabier' in text or 'diktier' in text or ('wie' in text and ('geschrieben' in text or 'schreibt' in text)):
        return True
    return False

def handle(text, luna, profile):
    if 'buchstabier' in text:
        word = profile.get_text_beetween('buchstabier', text)[0]
    elif 'diktier' in text:
        word = profile.get_text_beetween('diktier', text)[0]
    elif 'wie' in text and 'geschrieben' in text:
        word = profile.get_text_beetween('wird', text)[0]
    elif 'wie' in text and 'schreibt' in text:
        word = profile.get_text_beetween('man', text)[0]

    spelling = ""
    for letter in word:
        spelling += letter + ",  "

    luna.say(spelling)