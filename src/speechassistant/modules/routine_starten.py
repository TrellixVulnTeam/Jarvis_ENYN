import logging


def isValid(text):
    if 'starte' in text and 'routine' in text:
        return True
    else:
        return False


def handle(text, core, skills):
    actions = text["actions"]["commands"]

    try:
        for action in actions:
            if action["module_name"] == "":
                core.start_module(text=action["text"], user=core.user)
            else:
                core.start_module(name=action["module_name"], text=action["text"], user=core.user)
    except:
        logging.warning(f'Routine with action {text["description"]} doesnt works. It is removed from the List!')
