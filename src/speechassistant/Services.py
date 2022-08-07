from src.speechassistant.resources.services import Weather, LightController


class ServiceWrapper:
    def __init__(self, core, __data: dict) -> None:
        self.weather: Weather = Weather.get_instance(
            core.data["api_keys"]["open_weather_map"],
            core.local_storage["actual_location"],
        )
        self.light_system: LightController = LightController(core)
