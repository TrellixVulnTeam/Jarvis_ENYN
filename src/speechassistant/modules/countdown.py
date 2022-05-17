from time import sleep


def isValid(text):
    if "countdown" in text.lower():
        return True
    elif "zähl" in text.lower() and "runter" in text.lower():
        return True
    return False


def handle(text, core, skills):
    count_down = CountDown(core)
    count_down.start(text)


class CountDown:
    def __init__(self, core):
        self.core = core

    def start(self, text):
        time_code = -1
        for i in range(len(text.split(" ")) - 1):
            try:
                time_code = int(text[i])
            except:
                pass

        if "minute" in text:
            time_code *= 60
        elif "stunde" in text:
            self.core.say("Ist das nicht ein bisschen zu lang?")
            if "nein" in self.core.listen():
                time_code *= 3600

        if time_code is not -1:
            for i in range(time_code):
                self.core.say(str(time_code - i))
                sleep(1)
        else:
            self.core.say(
                "Tut mir leid, leider habe ich nicht verstanden, von wo ich herunter zählen soll"
            )
