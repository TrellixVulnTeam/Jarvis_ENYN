import time
from threading import Thread

from src.modules import ModuleWrapper
from src.services.light_systems.phue import PhilipsWrapper


def is_valid(text: str) -> bool:
    return False


def handle(text: str, wrapper: ModuleWrapper) -> None:
    th = Thread(target=run, args=(wrapper,))
    th.daemon = True
    th.start()


def run(wrapper: ModuleWrapper):
    # toDo: wrapper must be ip of bridge
    wrapper = PhilipsWrapper(wrapper)
    lights = wrapper.light_names.keys()

    wrapper.light_on(lights, change_brightness=False)
    wrapper.light_change_color(lights, "weiß")
    wrapper.set_light_brightness(lights, 17)

    for i in range(14):
        time.sleep(120)
        wrapper.inc_dec_brightness(lights, 17)
