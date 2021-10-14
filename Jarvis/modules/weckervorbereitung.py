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
    wrapper.set_light_brightness(wrapper.lights, 17)
    wrapper.light_on(wrapper.lights)

    for i in range(len(14)):
        wrapper.inc_dec_brightness(wrapper.lights, 17)
        time.sleep(120)
