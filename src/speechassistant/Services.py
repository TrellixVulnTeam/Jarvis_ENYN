from resources.services import Weather, LightController


class ServiceWrapper:
    def __init__(self, core, __data: dict, configuration_data: dict) -> None:
        self.weather: Weather = Weather()
        self.light_system: LightController = LightController(core)
