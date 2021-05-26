from resources.akinator.akinator import Akinator
PRIORITY = 3

def isValid(text):
    text = text.lower()
    if ('start' in text or 'beginn' in text) and ('ratespiel' in text or 'akinator' in text):
        return True
    return False


def handle(text, core, skills):
    core.say(
        'Wilkommen zum Rate-spiel! Ich werde dir Fragen stellen, die du wahrheitsgemäß mit wahlweise \n"Ja"\n"Nein"\n"wahrscheinlich"\n"wahrscheinlich nicht"\noder "keine Ahnung" beantworten musst. Wenn du keine Lust mehr auf das Spiel hast, sag einfach "stopp" oder "beende das Spiel".')

    aki = Akinator()
    question = aki.start_game(language='de')

    while aki.progression <= 80:
        core.say(question)
        user_input = assign_user_input(core.listen(), core)
        if user_input == "b":
            try:
                question = aki.back()
            except Exception:
                pass
        else:
            question = aki.answer(user_input)
    aki.win()

    core.say(f'Es ist {aki.first_guess["name"]}! Stimmt das?')

    user_input = core.listen().lower()
    if 'ja' in user_input or 'das stimmt' in user_input or 'richtig' in user_input:
        core.say('Das freut mich!')
    else:
        core.say('Dann muss ich wohl noch ein bisschen lernen!')


def assign_user_input(user_input, core):
    user_input = user_input.lower()
    if 'stopp' in user_input or 'stopp' in user_input or 'kein lust' in user_input:
        return 'stopp'
    elif 'nein' in user_input or 'falsch' in user_input or 'stimmt nicht' in user_input:
        return 'no'
    elif 'ja' in user_input or 'richtig' in user_input or 'stimmt' in user_input:
        return 'yes'
    elif 'wahrscheinlich' in user_input:
        if 'nicht' in user_input:
            return 'probably not'
        else:
            return 'probably'
    elif ('keine' in user_input and 'ahnung' in user_input) or ('weiß' in user_input and 'nicht' in user_input):
        return 'idk'
    else:
        core.say('Das habe ich leider nicht verstanden. Versuche es bitte noch einmal mit den Antwortmöglichkeiten \n"Ja"\n"Nein"\n"wahrscheinlich"\n"wahrscheinlich nicht"\noder "keine Ahnung"!')
        assign_user_input(core.listen(), core)


class Core():
    def __init__(self):
        pass

    def say(self, text):
        print(text)

    def listen(self):
        return input()


if __name__ == "__main__":
    handle("", Core(), None)