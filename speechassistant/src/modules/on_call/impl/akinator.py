from src.modules import ModuleWrapper
from src.modules.on_call.utils.akinator.akinator import Akinator
import src.modules.skills as skills

PRIORITY = 3


def isValid(text: str) -> bool:
    text = text.lower()
    return ("start" in text or "beginn" in text) and (
            "ratespiel" in text or "akinator" in text) or "wer bin ich" in text


def handle(text: str, wrapper: ModuleWrapper) -> None:
    wrapper.say(
        "Wilkommen zum Wer-Bin-Ich-Spiel! Ich werde dir Fragen stellen, die du wahrheitsgemäß mit wahlweise "
        '\n"Ja"\n"Nein"\n"wahrscheinlich"\n"wahrscheinlich nicht"\noder "keine Ahnung" beantworten musst. Wenn '
        'du keine Lust mehr auf das Spiel hast, sag einfach "stopp" oder "beende das Spiel".'
    )

    akinator = Akinator()
    question = akinator.start_game(language="de")

    while akinator.progression <= 95:
        question = __progress_questions(akinator, question, wrapper)

    guess: dict = akinator.win()
    __make_a_guess(guess, wrapper)


def __make_a_guess(result: dict, wrapper: ModuleWrapper):
    wrapper.say(f'Es ist {result["name"]}! Stimmt das?')
    user_input = wrapper.listen().lower()
    if "ja" in user_input or "das stimmt" in user_input or "richtig" in user_input:
        wrapper.say("Das freut mich!")
    else:
        wrapper.say("Dann muss ich wohl noch ein bisschen lernen!")


def __progress_questions(aki: Akinator, question: str, wrapper: ModuleWrapper):
    answer_to_question: str = wrapper.listen(text=question)
    intent: str = __assign_user_input(answer_to_question, wrapper)
    if intent == "b":
        return aki.back()
    else:
        return aki.answer(intent)


def __assign_user_input(user_input: str, wrapper: ModuleWrapper):
    user_input = user_input.lower()
    if skills.match_any(user_input, "stopp", "kein lust"):
        return "stopp"
    elif skills.match_any(user_input, "nein", "falsch", "stimmt nicht"):
        return "no"
    elif skills.match_any(user_input, "ja", "richtig", "stimmt"):
        return "yes"
    elif "wahrscheinlich" in user_input:
        return "probably not" if "nicht" in user_input else "probably"
    elif skills.match_all(user_input, "keine", "ahnung") or skills.match_all(user_input, "weiß", "nicht"):
        return "idk"
    else:
        response: str = wrapper.listen(text='Das habe ich leider nicht verstanden. Versuche es bitte noch einmal mit '
                                         'den Antwortmöglichkeiten '
                                         '\n"Ja"\n"Ne'
                                         '#in"\n"wahrscheinlich"\n"wahrscheinlich nicht"\noder "keine '
                                         'Ahnung"!')
        __assign_user_input(response, wrapper)
