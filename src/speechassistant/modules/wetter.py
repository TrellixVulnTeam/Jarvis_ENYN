from src.speechassistant.core import ModuleWrapper
from src.speechassistant.resources.module_skills import Skills
from src.speechassistant.services import Weather


def handle(text: str, core: ModuleWrapper, skills: Skills) -> None:
    __prepare_output(core.services.weather)
    __include_past(core.services.weather)


def __prepare_output(weather: Weather):
    pass


def __include_past(weather: Weather):
    rain_subsides: bool = False
    old_inf: dict = weather.old_weather_inf["minutely"]
    current: dict = weather.get_current_weather()

    if old_inf["0"]["precipitation"] != 0:
        raising_times: int = 0
        for i in range(len(old_inf["minutely"])-2):
            if old_inf["minutely"][i+1] > old_inf["minutely"][i]:
                raising_times += 1
        if raising_times < 10:
            rain_subsides: bool = True

