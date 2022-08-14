from .light_systems import LightController
from .weather import Weather


class ServiceWrapper:
    def __init__(self, core, __data: dict) -> None:
        self.weather: Weather = Weather.get_instance()
        self.light_system: LightController = LightController(core)
