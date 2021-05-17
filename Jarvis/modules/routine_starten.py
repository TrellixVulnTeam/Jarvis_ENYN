import json


def isValid(text):
    if 'starte' in text and 'routine' in text:
        return True
    else:
        return False

def handle(text, core, skills):

    for word in text:
        if "routine" in word.lower():
            routine = inf.get(word)
            for command in routine["actions"]:
                for text in command["text"]:
                    core.start_module(name=command["module_name"], text=text)
            break