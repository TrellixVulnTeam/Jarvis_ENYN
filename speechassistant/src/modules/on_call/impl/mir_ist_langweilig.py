import random

from src.modules import ModuleWrapper, skills


def is_valid(text: str) -> bool:
    return "mir" in text and "langweilig" in text


def handle(text: str, wrapper: ModuleWrapper) -> None:
    wrapper.say("Soll ich dir was interessantes erzählen?")
    response = wrapper.listen()
    if skills.is_desired(response):
        options = ["witz", "fun fact", "zungenbrecher", "phobie", "gedicht"]
        text = "erzähl mir einen " + random.choice(options)
        wrapper.start_module(name="smalltalk", text=text)
    else:
        wrapper.say("Alles klar, vielleicht findest du ja eine Beschäftigung.")
