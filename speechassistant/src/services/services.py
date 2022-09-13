from .impl.light_systems import LightController
from .impl.weather import Weather


class ServiceWrapper:
    def __init__(self, core, __data: dict) -> None:
        self.weather: Weather = Weather(core)
        self.light_system: LightController = LightController(core)
