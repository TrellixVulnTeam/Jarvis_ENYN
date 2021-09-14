import json

from phue import Bridge

colors = ['blau', 'rot', 'gelb', 'grün', 'pink', 'lila', 'türkis', 'weiß', 'orange', 'warmweiß']
# color_code = ['0000ff', 'ff0000', 'ffff00', '00FF00', 'ff1493', '9400d3', '00ffff', 'ffffff', '006400', '8b4513', 'ff8c00',
#        'F5DA81']
color_code = [[0.1548, 0.1117], [0.6778, 0.3017], [0.439, 0.4446], [0.2015, 0.6763], [0.5623, 0.2457], [0.2398, 0.1197],
              [0.1581, 0.2367], [0.3146, 0.3304], [0.588, 0.386], [0.4689, 0.4124]]


def isValid(text):
    text = text.lower()
    colors = ['blau', 'rot', 'gelb', 'grün', 'pink', 'lila', 'türkis', 'weiß', 'dunkelgrün', 'braun', 'orange',
              'warmweiß']
    if ('mach' in text or 'licht' in text) and (
            'an' in text or 'aus' in text or 'heller' in text or 'dunkler' in text or '%' in text or 'prozent' in text) \
            and not 'fernseh' in text:
        return True
    for item in colors:
        if item in text and 'licht' in text:
            return True


def handle(text, core, skills):
    pass


class PhillipsWrapper:
    def __init__(self, core, skills):
        BRIDGE_IP = core.local_storage["module_storage"]["philips_hue"]["Bridge-Ip"]
        self.bridge = Bridge(BRIDGE_IP)
        self.bridge.connect()

        self.skills = skills
        self.core = core

        self.lights = self.bridge.lights
        self.light_names = self.bridge.get_light_objects('name')

    def wrapper(self, text, core):
        lights = Logic.get_lights(text, self)
        # core.say("Okay.")
        if 'aus' in text:
            self.light_off(lights)
            return

        elif 'an' in text:
            self.light_on(lights)
            return

        elif 'heller' in text:
            if 'viel' in text:
                self.inc_dec_brightness(lights, 140)
            else:
                self.inc_dec_brightness(lights, 60)
            return

        elif 'dunkler' in text or 'dimm' in text:
            if 'viel' in text:
                self.inc_dec_brightness(lights, -140)
            else:
                self.inc_dec_brightness(lights, -60)
            return

        elif 'hell' in text:
            self.light_set_brightness(lights, 254)
            return

        elif 'prozent' in text or '%' in text:
            self.light_set_brightness(lights, Logic.get_percent_as_brightness(text))
            return

        else:
            for item in colors:
                if item in text:
                    self.light_change_color(lights, text)
                    return

        core.say('Leider habe ich nicht verstanden, was ich mit dem Licht machen soll.')

    def light_set_powerstate(self, lights, powerstate):

        if powerstate is None and (type(lights) == type("") or len(lights) <= 1):
            print("first if")
            if self.bridge.get_light(lights, 'on'):
                powerstate = 'off'
            else:
                powerstate = 'on'
        print("change powerstate of " + lights + " to " + powerstate)
        if powerstate == 'on':
            self.bridge.set_light(lights, 'on', True)
        elif powerstate == 'off':
            self.bridge.set_light(lights, 'on', False)
        else:
            return 'err'

    def light_on(self, lights):
        self.bridge.set_light(lights, 'on', True)
        self.bridge.set_light(lights, 'bri', 254)

    def light_off(self, lights):
        self.bridge.set_light(lights, 'on', False)

    def light_change_color(self, lights, text):
        color = Logic.get_named_color(text)
        if color[0] != -1 and color[1] != -1:
            self.light_on(lights)
            self.bridge.set_light(lights, 'xy', [color[0], color[1]])
            self.bridge.set_light(lights, 'bri', 254)
        else:
            self.core.say('Es tut mir leid, leider konnte ich nicht heraus filtern, welche Farbe du wünschst.')

    def light_set_brightness(self, lights, value):
        self.bridge.set_light(lights, 'bri', value)

    def inc_dec_brightness(self, lights, value):
        for light in lights:
            brightness = self.bridge.get_light(light.id, 'bri') + value
            if brightness > 254:
                brightness = 254
            if brightness < 0:
                brightness = 0
            self.bridge.set_light(light.id, 'bri', brightness)

    def get_light_in_json(self, light_name):
        tempLight = self.bridge.get_light(light_name)
        return {
            "on": self.bridge.get_light(tempLight["name"], 'on'),
            "brightness": self.bridge.get_light(tempLight["name"], 'bri'),
            "name": tempLight["name"]
        }

    def get_lights_in_json(self, order_by_id=False):
        output = {}
        light_objects = self.bridge.get_light_objects('id')
        if (order_by_id):
            for item in light_objects:
                output[item] = {
                    'id': item,
                    'name': light_objects[item].name,
                    'on': light_objects[item].on,
                    'brightness': light_objects[item].brightness,
                    'color': light_objects[item].hue,
                    'saturation': light_objects[item].saturation
                }
            return output
        else:
            for item in light_objects:
                output[light_objects[item].name] = {
                    'id': item,
                    'name': light_objects[item].name,
                    'on': light_objects[item].on,
                    'brightness': light_objects[item].brightness,
                    'color': light_objects[item].hue,
                    'saturation': light_objects[item].saturation
                }
            return output

    def is_light_in_system(self, light_name):
        for light_n in self.light_names:
            if light_n == light_name:
                return True
        return False

    def create_group(self, name, lights):
        for light in lights:
            if format(light) == format("String"):
                lights.remove(light)
                lights.append(self.bridge.get_light(light).id)
        self.bridge.create_group(name, lights)

    def rename_group(self, group_name, new_name):
        self.bridge.set_group(group_name, 'name', new_name)

    def change_lights_in_group(self, group_name, lights):
        for light in lights:
            if format(light) == format("String"):
                lights.remove(light)
                lights.append(self.bridge.get_light(light).id)
        self.bridge.set_group(group_name, 'lights', lights)

    def get_groups(self):
        return self.bridge.get_group()

    def get_group(self, group_name):
        return self.bridge.get_group(group_name)


class Logic:
    @staticmethod
    def get_lights(text, wrapper):
        lights = []
        text = text.lower()
        for item in wrapper.light_names:
            if item.lower() in text:
                lights.append(item)
        for group in wrapper.bridge.get_group():
            if group.name.lower() in text:
                for light in group.lights:
                    lights.append(light)
        if not lights:
            lights = wrapper.lights
        return lights

    @staticmethod
    def get_percent_as_brightness(text):
        text = text.replace('prozent', '%')  # unnötig, da sowieso wegen der SpeechRecognition % aber sicher ist sicher
        text_split = text.split(' ')
        for item in range(len(text_split)):
            if '%' in text_split[item]:
                percent = text_split[item].replace('%', '')
                percent = int(percent) / 100 * 254
                return int(percent)
        return -1

    @staticmethod
    def get_named_color(text):
        named_colors = []
        for i in range(len(colors)):
            if colors[i] in text:
                # folgende 2 Zeilen werden nur dann verwendet, wenn man die Farben als hex-Code angibt
                # color[0] = converter.hex_to_xy(farbe)[0]
                # color[1] = converter.hex_to_xy(farbe)[1]
                named_colors.append(color_code[i])
        return named_colors


class Core:
    def __init__(self):
        self.local_storage = {"module_storage": {
            "philips_hue": {
                "Bridge-Ip": "192.168.0.191"
            }
        }}

    def module_storage(self, module_name=""):
        return {"Bridge-Ip": "192.168.0.191"}


if __name__ == "__main__":
    ph = PhillipsWrapper(Core(), None)
    ph.light_set_powerstate("Küche", None)
