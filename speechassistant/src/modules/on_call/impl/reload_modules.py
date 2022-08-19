from src import log
from src.modules import ModuleWrapper

SECURE = False


# toDo Asynchronus say
def reload_own(core):
    log.info("\n\n--------- RELOAD ---------")

    core.core.modules.stop_continuous()
    core.core.modules.load_modules()
    core.core.modules.start_continuous()


def handle(text: str, wrapper: ModuleWrapper) -> None:
    # core.say('Okay, warte einen Moment')
    reload_own(wrapper)
    log.info("--------- FERTIG ---------\n\n")
    wrapper.say("Die Module wurden neu geladen.")


def is_valid(text: str):
    text = text.lower()
    if ("lad" in text or "nadel" in text or "load" in text) and (
            "modul" in text or "Duden" in text
    ):
        return True
    else:
        return False
