from src.speechassistant.core import ModuleWrapper
from src.speechassistant.resources.module_skills import Skills


def handle(text: str, core: ModuleWrapper, skills: Skills) -> None:
    core.services.weather.get_current_weather()