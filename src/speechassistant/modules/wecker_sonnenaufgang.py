import time
from threading import Thread

from src.speechassistant.resources.services.light_systems.Phue import PhilipsWrapper


def isValid(text):
    return False


def handle(text, core, skills):
    th = Thread(target=run, args=(core,))
    th.daemon = True
    th.start()


def run(core):
    wrapper = PhilipsWrapper(core)
    lights = wrapper.light_names.keys()

    wrapper.light_on(lights, change_brightness=False)
    wrapper.light_change_color(lights, "weiß")
    wrapper.set_light_brightness(lights, 17)

    for i in range(14):
        time.sleep(120)
        wrapper.inc_dec_brightness(lights, 17)
