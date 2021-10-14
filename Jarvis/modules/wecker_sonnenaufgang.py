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
    wrapper.light_on(lights)
    wrapper.set_light_brightness(lights, 17)

    for i in range(len(14)):
        wrapper.inc_dec_brightness(lights, 17)
        time.sleep(120)
