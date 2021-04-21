def isValid(text):
    return False


def handle(text, core, skills):
    actions = text["actions"]
    for action in actions:
        core.start_module(name=action["module_name"], text=action["text"], user=core.user)
