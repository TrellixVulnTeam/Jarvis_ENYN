from src.modules import ModuleWrapper, skills


# toDo: refactor

def is_valid(text: str) -> bool:
    text = text.lower()
    if "transkribier" in text or "schreib mit" in text:
        return True


def handle(text: str, wrapper: ModuleWrapper) -> None:
    start_word = "transkribiere" if "transkribier" in text else "mit"
    text = skills.get_text_between(start_word, text, output="String")
    wrapper.say(text, output="messenger")
