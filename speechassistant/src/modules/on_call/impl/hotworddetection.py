from src.modules import ModuleWrapper

# toDo: refactor

def isValid(text: str) -> bool:
    if "hotworddetection" in text:
        return True


def handle(text: str, wrapper: ModuleWrapper) -> None:
    room = wrapper.analyze["room"]
    if room is None:
        room = wrapper.room_name

    if "start" in text:
        wrapper.change_hotworddetection(room=room, changing_to="on")
        wrapper.say(
            "Die Hotworddetection wurde eingeschaltet, ab jetzt höre ich wieder auf deine Komandos.",
            output="speech",
        )
        wrapper.say(
            f"Die Hotworddetection wurde im Raum {room} eingeschaltet.",
            output="messenger",
        )
    elif "stopp" in text:
        wrapper.change_hotworddetection(room=room, changing_to="off")
        wrapper.say(
            "Die Hotworddetection wurde ausgeschaltet, ab jetzt höre ich nicht mehr auf deine Komandos.",
            output="speech",
        )
        wrapper.say(
            f"Die Hotworddetection wurde im Raum {room} ausgeschaltet, ab jetzt höre ich nicht mehr auf deine Komandos.",
            output="messenger",
        )
