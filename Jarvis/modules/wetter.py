

def handle(text, core, skills):
    __prepare_output(core.weather)
    __include_past(core.weather)


def __prepare_output(weather):
    pass


def __include_past(weather):
    rain_subsides = False
    old_inf = weather.old_weather_inf["minutely"]
    current = weather.get_current_weather()

    if old_inf["0"]["precipitation"] != 0:
        raising_times = 0
        for i in range(len(old_inf["minutely"])-2):
            if old_inf["minutely"][i+1] > old_inf["minutely"][i]:
                raising_times += 1
        if raising_times < 10:
            rain_subsides = True

