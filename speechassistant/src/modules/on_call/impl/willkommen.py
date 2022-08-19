import datetime

from src.modules import ModuleWrapper, skills


def isValid(text: str) -> bool:
    text = text.lower()
    if (
        (text.startswith("hallo") or text == "hi" or text == "hey" or text == "/start")
        and not "geht" in text
        or "läuft" in text
    ):
        return True
    elif "gute" in text and (
        "tag" in text or "morgen" in text or "abend" in text or "nacht" in text
    ):
        return True
    return False


def handle(text: str, wrapper: ModuleWrapper) -> None:
    text = text.lower()
    now = datetime.datetime.now()
    time = now.hour
    if "hallo" in text:
        wrapper.say("Hallo!")

    elif "guten" in text and "tag" in text:
        if time >= 20 or time <= 4:
            wrapper.say(
                'Naja "Tag" würde ich das nicht mehr nennen, aber ich wünsche dir auch einen guten Abend'
            )
        elif 5 <= time <= 20:
            wrapper.say("Guten Tag!")

    elif "guten" in text and "morgen" in text:
        if time is 4 or time is 5:
            wrapper.say("Hast du heute was wichtiges anstehen?")
            response = wrapper.listen
            if "ja" in text:
                wrapper.say("Dann wünsche ich dir dabei viel Erfolg!")
            else:
                wrapper.say(
                    "Dann schlaf ruhig weiter, es ist noch viel zu früh, um aufzustehen."
                )
        elif 6 <= time <= 10:
            wrapper.say("Guten Morgen!")
        elif time is 11 or time is 12:
            wrapper.say("Wurde aber auch langsam Zeit. Aber auch dir einen guten Morgen.")
        elif 14 <= time <= 18:
            wrapper.say(
                "Ob es noch Morgen ist, liegt wohl im Blickwinkel des Betrachters. Ich würde eher sagen, "
                "dass es Mittag oder Nachmittag ist."
            )
        elif time >= 19 or time <= 3:
            wrapper.say(
                "Also Morgen ist es auf jeden Fall nicht mehr. Daher wünsche ich dir einfach Mal einen guten Abend."
            )
        else:
            wrapper.say("Hallo!")

    elif "guten" in text and "abend" in text:
        if 6 <= time <= 17:
            wrapper.say(
                "Ob es Abend ist, liegt wohl im Blickwinkel des Betrachters. In Amerika ist es jetzt in der Tat Abend."
            )
        elif time >= 18 or time <= 5:
            wrapper.say("Gute nacht")
        else:
            wrapper.say("Guten Abend.")

    elif "gute" in text and "nacht" in text:
        if 1 <= time <= 13:
            wrapper.say("Du solltest echt langsam ins Bett gehen.")
        elif (8 <= time <= 24) or time is 0:
            wrapper.say("Gute Nacht.")
        else:
            wrapper.say("Eine sehr interessante Definition der derzeitigen Uhrzeit.")
        response = wrapper.listen(text="Soll ich dich morgen wecken?")
        if skills.is_desired(response):
            if wrapper.analysis["datetime"] is None:
                response_two = wrapper.listen("Wann soll ich dich denn wecken?")
                wrapper.start_module(text="weck mich " + response_two)
            else:
                wrapper.start_module(text="weck mich " + response)
        else:
            wrapper.say("Okay.")
