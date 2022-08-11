# !!! When a color is added, it is essential that it is also added to Intents.json !!!
from phue import Bridge

from src.resources import Skills

colors = [
    "blau",
    "rot",
    "gelb",
    "grün",
    "pink",
    "lila",
    "türkis",
    "weiß",
    "orange",
    "warmweiß",
]
# color_code = ['0000ff', 'ff0000', 'ffff00', '00FF00', 'ff1493', '9400d3', '00ffff', 'ffffff', '006400', '8b4513', 'ff8c00',
#        'F5DA81']
color_code = [
    [0.1548, 0.1117],
    [0.6778, 0.3017],
    [0.439, 0.4446],
    [0.2015, 0.6763],
    [0.5623, 0.2457],
    [0.2398, 0.1197],
    [0.1581, 0.2367],
    [0.3146, 0.3304],
    [0.588, 0.386],
    [0.4689, 0.4124],
]


class PhilipsWrapper:
    def __init__(self, ip: str):
        bridge_ip = ip
        self.bridge = Bridge(bridge_ip)
        self.bridge.connect()

        self.skills = Skills()

        self.lights = self.bridge.lights
        self.light_names = self.bridge.get_light_objects("name")

    def wrapper(self, text: str) -> str:
        lights = self.Logic.get_lights(text, self)
        if "aus" in text:
            self.light_off(lights)
            return ""

        elif "an" in text:
            # toDo: distinguish between different times
            self.light_on(lights)
            return ""

        elif "heller" in text:
            if "viel" in text:
                self.inc_dec_brightness(lights, 140)
            else:
                self.inc_dec_brightness(lights, 60)
            return ""

        elif "wärmer" in text:
            self.set_light_color_temp(lights, 25)

        elif "kälter" in text:
            self.set_light_color_temp(lights, -25)

        elif "dunkler" in text or "dimm" in text:
            if "viel" in text:
                self.inc_dec_brightness(lights, -140)
            else:
                self.inc_dec_brightness(lights, -60)
            return ""

        elif "hell" in text:
            self.set_light_brightness(lights, 254)
            return ""

        elif "prozent" in text or "%" in text:
            self.set_light_brightness(
                lights, self.Logic.get_percent_as_brightness(text)
            )
            return ""

        else:
            for item in colors:
                if item in text:
                    self.light_change_color(lights, text)
                    return ""

        return "Leider habe ich nicht verstanden, was ich mit dem Licht machen soll."

    def set_light_powerstate(self, lights, powerstate):
        if powerstate is None and (type(lights) is type("") or len(lights) <= 1):
            if self.bridge.get_light(lights, "on"):
                powerstate = "off"
            else:
                powerstate = "on"
        if powerstate == "on":
            self.bridge.set_light(lights, "on", True)
        elif powerstate == "off":
            self.bridge.set_light(lights, "on", False)
        else:
            return "err"

    def get_light_powerstate(self, light):
        if light is None:
            light = self.lights[0]
        return self.bridge.get_light(light, "on")

    def light_on(self, lights, change_brightness=True):
        if type(lights) != type([]) and type(lights) != type("") and type(lights) != 1:
            lights = self.bridge.get_light(lights)
            # toDO: possibility that lights is an array of Objects
        self.bridge.set_light(lights, "on", True)
        if change_brightness:
            self.bridge.set_light(lights, "bri", 254)
        """if self.color_adjustment:
            now = datetime.now()
            # add sunrise and sunset
            self.bridge.set_light(lights, 'sat', )"""

    def light_off(self, lights):
        self.bridge.set_light(lights, "on", False)

    def light_change_color(self, lights, text) -> str:
        color = self.Logic.get_named_color(text)
        if color is not None:
            self.light_on(lights)
            self.bridge.set_light(lights, "xy", [color[0], color[1]])
            # self.bridge.set_light(lights, 'bri', 254)
        else:
            return "Es tut mir leid, leider konnte ich nicht heraus filtern, welche Farbe du wünschst."

    def inc_dec_ct(self, lights, value):
        for light in lights:
            ct = light.ct + value
            if ct > 254:
                ct = 254
            elif ct < 0:
                ct = 0
            self.bridge.set_light(light, "ct", ct)

    def set_light_color_temp(self, lights, value):
        self.bridge.set_light(lights, "sat", int(value))

    def set_light_brightness(self, lights, value):
        self.bridge.set_light(lights, "bri", int(value))

    def inc_dec_brightness(self, lights, value):
        if type(lights[0]) is not type("") and type(lights[0]) is not type(1):
            for item in lights:
                item = item.id
        for light in lights:
            brightness = self.bridge.get_light(light, "bri") + value
            if brightness > 254:
                brightness = 254
            if brightness < 0:
                brightness = 0
            self.bridge.set_light(light, "bri", brightness)

    def get_light_in_json(self, light_name):
        temp_tight = self.bridge.get_light(light_name)
        return {
            "on": self.bridge.get_light(temp_tight["name"], "on"),
            "brightness": self.bridge.get_light(temp_tight["name"], "bri"),
            "name": temp_tight["name"],
        }

    def get_lights_in_json(self, order_by_id=False):
        output = {}
        light_objects = self.bridge.get_light_objects("id")
        if order_by_id:
            for item in light_objects:
                output[item] = {
                    "id": item,
                    "name": light_objects[item].name,
                    "on": light_objects[item].on,
                    "brightness": light_objects[item].brightness,
                    "color": light_objects[item].hue,
                    "saturation": light_objects[item].saturation,
                    "ct": light_objects[item].ct,
                }
            return output
        else:
            for item in light_objects:
                output[light_objects[item].name] = {
                    "id": item,
                    "name": light_objects[item].name,
                    "on": light_objects[item].on,
                    "brightness": light_objects[item].brightness,
                    "color": light_objects[item].hue,
                    "saturation": light_objects[item].saturation,
                    "ct": light_objects[item].ct,
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
        self.bridge.set_group(group_name, "name", new_name)

    def change_lights_in_group(self, group_name, lights):
        for light in lights:
            if format(light) == format("String"):
                lights.remove(light)
                lights.append(self.bridge.get_light(light).id)
        self.bridge.set_group(group_name, "lights", lights)

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
            if ("bis" in text and "auf" in text) or "außer" in text:
                for item in wrapper.light_names:
                    if item.lower() not in text:
                        lights.append(item)
            else:
                for item in wrapper.light_names:
                    if item.lower() in text:
                        lights.append(item)
            for group in wrapper.bridge.get_group():
                if wrapper.bridge.get_group(int(group), "name").lower() in text:
                    for light in group.lights:
                        lights.append(light.lower())
            if (
                    ("alle" in text or "überall" in text)
                    and "außer" in text
                    and lights != []
            ):
                temp_lights = []
                for item in wrapper.light_names:
                    if item not in lights:
                        temp_lights.append(item)
                return temp_lights
            if not lights:
                for item in wrapper.light_names:
                    lights.append(item)
            return lights

        @staticmethod
        def get_percent_as_brightness(text):
            text = text.replace(
                "prozent", "%"
            )  # unnötig, da sowieso wegen der SpeechRecognition % aber sicher ist sicher
            text_split = text.split(" ")
            for item in text_split:
                if "%" in item:
                    percent = item.replace("%", "")
                    percent = int(percent) / 100 * 254
                    return int(percent)
            return -1

        @staticmethod
        def get_brightness_as_percent(value):
            return value / 254 * 100

        @staticmethod
        def get_named_color(text):
            colors = [
                "blau",
                "rot",
                "gelb",
                "grün",
                "pink",
                "lila",
                "türkis",
                "weiß",
                "orange",
                "warmweiß",
            ]
            # color_code = ['0000ff', 'ff0000', 'ffff00', '00FF00', 'ff1493', '9400d3', '00ffff', 'ffffff', '006400', '8b4513', 'ff8c00',
            #        'F5DA81']
            color_code = [
                [0.1548, 0.1117],
                [0.6778, 0.3017],
                [0.439, 0.4446],
                [0.2015, 0.6763],
                [0.5623, 0.2457],
                [0.2398, 0.1197],
                [0.1581, 0.2367],
                [0.3146, 0.3304],
                [0.588, 0.386],
                [0.4689, 0.4124],
            ]
            for i, color in enumerate(colors):
                if color in text:
                    # folgende 2 Zeilen werden nur dann verwendet, wenn man die Farben als hex-Code angibt
                    # color[0] = converter.hex_to_xy(farbe)[0]
                    # color[1] = converter.hex_to_xy(farbe)[1]
                    return color_code[i]
            return None
