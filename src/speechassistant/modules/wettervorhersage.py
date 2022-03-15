from datetime import datetime, timedelta


def handle(text, core, skills):
    weather_service: core.services.weather = core.services.weather
    city: str = core.analysis['town']
    time: timedelta = core.analysis['datetime'] - datetime.now()

    if 'morgens' in text or (' am' in text and 'morgen' in text) or 'früh' in text:
        time.min = 540      # = 9 hours
    elif 'mittags' in text or (' am' in text and 'Mittag' in text):
        time.min = 840      # = 14 hours
    elif 'abend' in text:
        time.min = 1200     # = 12 hours
    elif 'nacht' in text:
        time.min = 1380     # = 23 hours

    hour_offset: int = time.days * 24 + int(time.min / 60)

    # weather-API gives hourly data for 47 hours. Take them if possible, else the daily once
    if hour_offset <= 47:
        core.say(weather_service.get_hourly_forecast_string(city, offset=hour_offset))
    else:
        core.say(weather_service.get_daily_forecast_string(city, time.days))
