from phue import Bridge

# !!! When a color is added, it is essential that it is also added to Intents.json !!!
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
    pw = PhillipsWrapper(core)
    pw.wrapper(text)


class PhillipsWrapper:
    def __init__(self, core):
        bridge_ip = core.local_storage["module_storage"]["philips_hue"]["Bridge-Ip"]
        self.bridge = Bridge(bridge_ip)
        self.bridge.connect()

        self.skills = core.skills
        self.core = core

        self.lights = self.bridge.lights
        self.light_names = self.bridge.get_light_objects('name')

    def wrapper(self, text):
        lights = Logic.get_lights(text, self)
        # self.core.say("Okay.")
        if 'aus' in text:
            self.light_off(lights)
            return

        elif 'an' in text:
            # toDo: distinguish between different times
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
            self.set_light_brightness(lights, 254)
            return

        elif 'prozent' in text or '%' in text:
            self.set_light_brightness(lights, Logic.get_percent_as_brightness(text))
            return

        else:
            for item in colors:
                if item in text:
                    self.light_change_color(lights, text)
                    return

        self.core.say('Leider habe ich nicht verstanden, was ich mit dem Licht machen soll.')

    def set_light_powerstate(self, lights, powerstate):

        if powerstate is None and (type(lights) == type("") or len(lights) <= 1):
            if self.bridge.get_light(lights, 'on'):
                powerstate = 'off'
            else:
                powerstate = 'on'
        if powerstate == 'on':
            self.bridge.set_light(lights, 'on', True)
        elif powerstate == 'off':
            self.bridge.set_light(lights, 'on', False)
        else:
            return 'err'

    def get_light_powerstate(self, light):
        if light is None:
            light = self.lights[0]
        return self.bridge.get_light(light, 'on')

    def light_on(self, lights, change_brightness=True):
        if type(lights) != type([]) and type(lights) != type("") and type(lights) != (1):
            lights = self.bridge.get_light(lights)
            # toDO: possibility that lights is an array of Objects
        self.bridge.set_light(lights, 'on', True)
        if change_brightness:
            self.bridge.set_light(lights, 'bri', 254)

    def light_off(self, lights):
        self.bridge.set_light(lights, 'on', False)

    def light_change_color(self, lights, text):
        color = Logic.get_named_color(text)
        if color != None:
            self.light_on(lights)
            self.bridge.set_light(lights, 'xy', [color[0], color[1]])
            # self.bridge.set_light(lights, 'bri', 254)
        else:
            self.core.say('Es tut mir leid, leider konnte ich nicht heraus filtern, welche Farbe du wünschst.')

    def set_light_color_temp(self, value):
        pass # toDo

    def set_light_brightness(self, lights, value):
        self.bridge.set_light(lights, 'bri', int(value))

    def inc_dec_brightness(self, lights, value):
        if type(lights[0]) is not type("") and type(lights[0]) is not type(1):
            for i in range(len(lights)):
                lights[i] = lights[i].id
        for light in lights:
            brightness = self.bridge.get_light(light, 'bri') + value
            if brightness > 254:
                brightness = 254
            if brightness < 0:
                brightness = 0
            self.bridge.set_light(light, 'bri', brightness)

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
        is_on = True
        group = self.bridge.get_group(group_name)
        for light in group["lights"]:
            if not light["on"]:
                is_on = False
        group["on"] = is_on
        print(group)
        return group


class Logic:
    def __init__(self):
        pass

    @staticmethod
    def get_lights(text, wrapper):
        lights = []
        text = text.lower()
        for item in wrapper.light_names:
            if item.lower() in text:
                lights.append(item)
        for group in wrapper.bridge.get_group():
            if wrapper.bridge.get_group(int(group), 'name').lower() in text:
                for light in group.lights:
                    lights.append(light.lower())
        if not lights:
            for item in wrapper.light_names:
                lights.append(item)
        print(lights)
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
    def get_brightness_as_percent(value):
        return value / 254 * 100

    @staticmethod
    def get_named_color(text):
        named_colors = []
        for i in range(len(colors)):
            if colors[i] in text:
                # folgende 2 Zeilen werden nur dann verwendet, wenn man die Farben als hex-Code angibt
                # color[0] = converter.hex_to_xy(farbe)[0]
                # color[1] = converter.hex_to_xy(farbe)[1]
                return color_code[i]
        return None
