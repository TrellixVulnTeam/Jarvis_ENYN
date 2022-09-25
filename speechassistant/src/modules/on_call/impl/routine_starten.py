from src import log
from src.models import Module
from src.modules import ModuleWrapper


# toDo: refactor

def is_valid(text: str) -> bool:
    return False


def handle(text: Module, wrapper: ModuleWrapper):
    actions = text["actions"]["commands"]

    try:
        for action in actions:
            if action["module_name"] == "":
                wrapper.start_module(text=action["text"], user=wrapper.user)
            else:
                wrapper.start_module(
                    name=action["module_name"], text=action["text"], user=wrapper.user
                )
    except Exception:
        # todo: specify exceptions
        log.warning(
            f'Routine with action {text["description"]} doesnt works. It is removed from the List!'
        )
