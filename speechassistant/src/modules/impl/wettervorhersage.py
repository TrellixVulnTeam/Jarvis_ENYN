from datetime import datetime, timedelta

from src.core import ModuleWrapper
from src.resources import Skills


def isValid(text: str) -> bool:
    if "wie" in text and "wird" in text and "wetter" in text:
        return True
    return False


def handle(text: str, core: ModuleWrapper, skills: Skills) -> None:
    weather_service: core.services.weather = core.services.weather

    city: str = core.analysis.get("town")
    if city is None:
        city = core.local_storage.get("city")

    time_diff: timedelta = core.analysis.get("datetime") - datetime.now()
    if "morgens" in text or (" am" in text and "morgen" in text) or "früh" in text:
        time_diff = timedelta(days=time_diff.days, minutes=540)  # = 9 hours
    elif "mittags" in text or (" am" in text and "Mittag" in text):
        time_diff = timedelta(days=time_diff.days, minutes=840)  # = 14 hours
    elif "abend" in text:
        time_diff = timedelta(days=time_diff.days, minutes=1140)  # = 19 hours
    elif "nacht" in text:
        time_diff = timedelta(days=time_diff.days, minutes=1380)  # = 23 hours

    hour_offset: int = time_diff.days * 24 + int(time_diff.seconds / 3600)

    # weather-API gives hourly data for 47 hours. Take them if possible, else the daily once
    if hour_offset <= 47:
        core.say(weather_service.get_hourly_forecast_string(city, offset=hour_offset))
    else:
        core.say(weather_service.get_daily_forecast_string(city, time_diff.days))
