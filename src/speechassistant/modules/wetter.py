from src.speechassistant.core import ModuleWrapper
from src.speechassistant.resources.module_skills import Skills


def isValid(text: str) -> bool:
    if 'wie' in text and 'ist' in text and 'wetter' in text and not 'wird' in text:
        return True
    return False


def handle(text: str, core: ModuleWrapper, skills: Skills) -> None:
    core.services.weather.get_current_weather()
