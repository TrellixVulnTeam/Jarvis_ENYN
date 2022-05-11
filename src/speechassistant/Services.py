from src.speechassistant.core import Core
from src.speechassistant.resources.services import Weather, LightController


class ServiceWrapper:
    def __init__(self, core: Core, __data: dict, configuration_data: dict) -> None:
        self.weather: Weather = Weather(__data["api_keys"]["open_weather_map"],
                                        configuration_data["Local_storage"]["home_location"],
                                        core.skills)
        self.light_system: LightController = LightController(core)
