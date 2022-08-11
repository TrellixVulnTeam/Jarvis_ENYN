import random
import re

PRIORITY = 1

data = [
    [
        ["zum geburtstag gratulieren"],
        [
            "Herzlichen Glückwunsch.",
            "Alles Gute",
            "Alles Gute im neuen Lebensjahr",
            "Happy Birthday!",
            "Alles Liebe und Gute zum Geburtstag!",
        ],
        [
            "Herzlichen Glückwunsch {}.",
            "Alles Gute {}",
            "Alles Gute im neuen Lebensjahr {}",
            "Happy Birthday, {}!",
            "Alles Liebe und Gute zum Geburtstag, {}!",
        ],
    ],
    [
        ["eine freude machen", "einen gefallen tun"],
        ["Du könntest etwas verschenken, was du nicht mehr brauchst."],
        ["Du könntest {} etwas schenken, was du nicht mehr brauchst."],
    ],
]

personPattern = re.compile(r".*?wie kann ich (.*?)\s.*", re.I)


def isValid(text):
    text = text.lower()
    ret = personPattern.match(text) is not None
    return ret


def handle(text, core, skills):
    text = text.lower()
    if "wie kann ich jemand" in text:
        for entry in data:
            for str in entry[0]:
                if str.lower() in text:
                    core.say(random.choice(entry[1]))
                    return
        core.say("Da kann ich dir leider nicht helfen.")
    else:
        match = personPattern.match(text)
        if match is not None:
            person = match.group(1)
            for entry in data:
                for str in entry[0]:
                    if str.lower() in text:
                        core.say(random.choice(entry[2]).format(person))
                        return
        core.say("Da kann ich dir leider nicht helfen.")
