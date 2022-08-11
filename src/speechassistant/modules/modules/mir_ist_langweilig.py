import random

from core import ModuleWrapper
from resources.module_skills import Skills


def isValid(text: str) -> bool:
    if "mir" in text and "langweilig" in text:
        return True
    return False


def handle(text, core: ModuleWrapper, skills: Skills):
    core.say("Soll ich dir was interessantes erzählen?")
    response = core.listen()
    if skills.is_desired(response):
        options = ["witz", "fun fact", "zungenbrecher", "phobie", "gedicht"]
        text = "erzähl mir einen " + random.choice(options)
        handle(text, core, skills)
    else:
        core.say("Alles klar, vielleicht findest du ja eine Beschäftigung.")
