import time

from src.modules import ModuleWrapper


def isValid(text: str) -> bool:
    return "lad" in text and "audio" in text


def handle(text: str, wrapper: ModuleWrapper) -> None:
    if "output" in text or "ausgabe" in text:
        restart_output(wrapper)
        wrapper.say("Die Audioausgabe wurde neu gestartet.")
    elif "input" in text or "eingabe" in text:
        restart_input(wrapper)
        wrapper.say("Die Audioeingabe wurde neu gestartet.")
    else:
        restart_input(wrapper)
        restart_output(wrapper)
        wrapper.say("Die Audiotreiber wurden neu gestartet.")


def restart_output(wrapper: ModuleWrapper) -> None:
    wrapper.core.audio_output.stop()
    time.sleep(1)
    wrapper.core.audio_output.start()


def restart_input(wrapper: ModuleWrapper) -> None:
    wrapper.core.audio_input.stop()
    time.sleep(1)
    wrapper.core.audio_input.start()
