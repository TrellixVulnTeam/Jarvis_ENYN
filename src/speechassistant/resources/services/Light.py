from .light_systems import Phue


class LightController:
    __instance = None

    @staticmethod
    def get_instance():
        if LightController.__instance is None:
            LightController()
        return LightController.__instance

    def __init__(self):
        if LightController.__instance is not None:
            raise Exception("Singleton cannot be instantiated more than once!")
        from src.speechassistant.core import Core

        self.core: Core = Core.get_instance()
        self.systems = []
        self.lights = []

        LightController.__instance = self

    def generate_light_systems(self):
        system_list = []
        phue = Phue.PhilipsWrapper(
            self.core.local_storage["service_storage"]["philips_hue"]["Bridge-IP"]
        )
        system_list.append({"name": "phue", "systemObject": phue})

        self.systems = system_list

    def add_lights(self):
        for system in self.systems:
            for light in system["systemObject"].get_lights_in_json():
                self.lights.append(
                    {"id": light["id"], "name": light["name"], "system": system}
                )

    def __get_named_lights(self, text):
        text = text.lower()
        named_lights = []

        if ("bis" in text and "auf" in text) or "außer" in text:
            for light in self.lights:
                if light["name"].lower() not in text:
                    named_lights.append(light)
        else:
            for light in self.lights:
                if light["name"].lower() in text:
                    named_lights.append(light)

        for system in self.systems:
            for light in system.get_named_groupt(text):
                named_lights.append(light)

        return named_lights

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
            for i, item in enumerate(colors):
                if item in text:
                    # folgende 2 Zeilen werden nur dann verwendet, wenn man die Farben als hex-Code angibt
                    # color[0] = converter.hex_to_xy(farbe)[0]
                    # color[1] = converter.hex_to_xy(farbe)[1]
                    return color_code[i]
            return None
