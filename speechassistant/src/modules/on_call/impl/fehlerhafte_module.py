from src.modules import skills, ModuleWrapper


def isValid(text: str) -> bool:
    text = text.lower()
    # funktionier = ["funktionieren", "funktioniert"]
    return "fehlerhaft" in text or skills.match_all(text, "funktionier", "nicht")


def handle(text: str, wrapper: ModuleWrapper) -> None:
    faulty_list = [module for module in wrapper.local_storage["modules"] if module["status"] == "error"]
    if len(faulty_list) == 0:
        wrapper.say("Alle Module konnten korrekt geladen werden.")
    else:
        wrapper.say(
            f"Folgende Module konnten nicht geladen werden: {skills.get_enumerate(faulty_list)}"
        )
