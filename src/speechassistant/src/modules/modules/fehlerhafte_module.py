def isValid(text):
    text = text.lower()
    if "module" in text and "fehlerhaft" in text:
        return True
    elif "module" in text and "funktionieren" in text and "nicht" in text:
        return True


def handle(text, core, skills):
    faulty_list = []
    for module in core.local_storage["modules"].values():
        if module["status"] == "error":
            faulty_list.append(module["name"])
    if len(faulty_list) == 0:
        core.say("Alle Module konnten korrekt geladen werden.")
    else:
        core.say(
            "Folgende Module konnten nicht geladen werden: "
            + skills.get_enumerate(faulty_list)
        )
