def isValid(text):
    text = text.lower()
    if "transkribier" in text or "schreib mit" in text:
        return True


def handle(text, core, skills):
    start_word = "transkribiere" if "transkribier" in text else "mit"
    text = skills.get_text_between(start_word, text, output="String")
    core.say(text, output="messenger")
