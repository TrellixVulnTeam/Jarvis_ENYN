from datetime import datetime

from src.modules import ModuleWrapper, skills


def is_valid(text):
    if "stoppuhr" in text.lower():
        return True
    elif "stopp" in text and "zeit" in text:
        return True
    return False


def handle(text: str, wrapper: ModuleWrapper) -> None:
    if "start" in text:
        start(wrapper)
    elif "stop" in text or "beend" in text:
        stop(wrapper)
    else:
        wrapper.say("Ich kann die Stoppuhr nur starten oder stoppen.")


def start(wrapper: ModuleWrapper):
    if "stopwatch" in wrapper.local_storage.keys():
        wrapper.say("Es läuft bereits eine Stoppuhr. Soll ich diese erst stoppen?")
        if skills.is_desired(wrapper.listen()):
            wrapper.say(
                "Alles klar. Die alte Stoppuhr wurde bei {} gestoppt und eine neue gestartet.".format(
                    skills.get_time(wrapper.local_storage["stoppuhr"]),
                    skills.get_time_difference(wrapper.local_storage["stoppuhr"]),
                )
            )
            wrapper.local_storage["stoppuhr"] = datetime.now()
        else:
            wrapper.say("Alles klar, die alte Stoppuhr läuft weiter.")
    else:
        wrapper.say(
            "Alles klar, die Stoppuhr wurde um {} gestartet.".format(
                skills.get_time(datetime.now())
            )
        )
        wrapper.local_storage["stoppuhr"] = datetime.now()


def stop(wrapper: ModuleWrapper):
    if "stoppuhr" in wrapper.local_storage.keys() and wrapper.local_storage["stoppuhr"] != "":
        wrapper.say(
            "Alles klar, die Stoppuhr wurde um {} gestoppt. Sie dauerte {}.".format(
                skills.get_time(datetime.now()),
                skills.get_time_difference(
                    wrapper.local_storage["stoppuhr"], datetime.now()
                ),
            )
        )
        wrapper.local_storage["stoppuhr"] = ""
    else:
        wrapper.say("Es wurde noch keine Stoppuhr gestartet. Soll ich eine starten?")
        if skills.is_desired(wrapper.listen()):
            wrapper.say(
                "Alles klar, Stoppuhr wurde um {} gestartet".format(
                    skills.get_time(datetime.now())
                )
            )
            wrapper.local_storage["stoppuhr"] = datetime.now()
