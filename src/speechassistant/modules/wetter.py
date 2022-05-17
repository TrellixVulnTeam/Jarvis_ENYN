from src.speechassistant.core import ModuleWrapper
from src.speechassistant.resources.module_skills import Skills


def isValid(text: str) -> bool:
    if "wie" in text and "ist" in text and "wetter" in text and not "wird" in text:
        return True
    return False


def handle(text: str, core: ModuleWrapper, skills: Skills) -> None:

    city: str = core.analysis.get("town")
    if city is None:
        city = core.local_storage.get("city")

    response: str = core.services.weather.get_current_weather_string(city)
    core.say(response)
