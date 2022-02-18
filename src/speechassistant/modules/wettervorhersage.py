
def handle(text, core, skills):
    if core.analysis['town'] != None:
        output = core.services.weather.get_current_weather_string(city=core.analysis['town'])
        core.say(output)
