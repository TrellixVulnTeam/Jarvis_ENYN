import time

from philips_hue import PhillipsWrapper
from threading import Thread


def isValid(text):
    return False


def handle(text, core, skills):
    th = Thread(target=run, args=(core,))
    th.daemon = True
    th.start()


def run(core):
    wrapper = PhillipsWrapper(core)
    lights = []

    for name in wrapper.light_names.keys():
        lights.append(name)
    wrapper.light_on(lights, change_brightness=False)
    wrapper.set_light_brightness(lights, 17)

    for i in range(14):
        time.sleep(120)
        wrapper.inc_dec_brightness(lights, 17)
