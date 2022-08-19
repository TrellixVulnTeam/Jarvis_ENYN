from src.enums import OutputTypes
from src.modules import ModuleWrapper, skills

PRIORITY = 0


def isValid(text: str) -> bool:
    text = text.lower()
    if "spiel " in text or "spiele " in text:
        return True
    return False


def handle(text: str, wrapper: ModuleWrapper) -> None:
    wrapper.say("Alles klar.")
    startword = "spiele" if "spiele" in text else "spiel"
    until = ""
    until_words = ["nächstes", "danach", "gleich", "als"]
    for word in until_words:
        if word in text:
            until = word
            break
    song = skills.get_text_between(startword, text, end_word=until, output=OutputTypes.STRING)
    as_next = skills.match_any(text, "nächstes", "danach", "gleich")

    # toDo

    wrapper.play_music(
        by_name=song,
        url=False,
        path=False,
        next=as_next,
        now=False,
        playlist=False,
        announce=False,
    )
