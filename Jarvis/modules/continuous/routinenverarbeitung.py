import json
from datetime import datetime
import Jarvis.modules.sonnen_auf_und_untergang as sun_rise_set
import requests

INTERVALL = 2

numb_to_day: {
    "1": "monday",
    "2": "tuesday",
    "3": "wednesday",
    "4": "thursday",
    "5": "friday",
    "6": "saturday",
    "7": "sunday"
}


def run(core, skills):
    with open("../resources/routine/declaration.json") as declaration_file:
        inf = json.load(declaration_file)
    now = datetime.now()

    for routine in inf:
        if is_day_correct(now, routine) and is_time_correct(now, routine, core):
            for command in routine["actions"]:
                for text in command["text"]:
                    core.start_module(name=command["module_name"], text=text)

def is_day_correct(now, inf):
    is_correct = False
    day_name = numb_to_day.get(str(now.isoweekday()))
    day_inf = inf["retakes"]["days"]
    if day_inf["daily"] or day_inf[day_name]:
        is_correct = True
    for day in day_inf["date_of_day"]:
        if int(day) == now.day:
            is_correct = True
    return is_correct


def is_time_correct(now, inf, core):
    # after_alarm is ignored, since this is only called by the alarm itself
    is_correct = False
    time_inf = inf["retakes"]["time"]
    for time in time_inf["clock_time"]:
        if now.hour >= time.split(":")[0] and now.minute >= time.split(":")[1]:
            is_correct = True
    if inf["retakes"]["after_sunrise"]:
        if is_sunrise(core.local_storage, now):
            is_correct = True
    if inf["retakes"]["after_sunset"]:
        if is_sunset(core.local_storage, now):
            is_correct = True
    return is_correct


def is_sunrise(local_storage, now):
    location = local_storage["home_location"]
    sunrise, sunset = get_sunrise_sunset_inf(location)
    if (sunrise // 60) >= now.hour and (sunrise % 60) >= now.minute:
        return True


def is_sunset(local_storage, now):
    location = local_storage["home_location"]
    sunrise, sunset = get_sunrise_sunset_inf(location)
    if (sunset // 60) >= now.hour and (sunset % 60) >= now.minute:
        return True


def get_sunrise_sunset_inf(location):
    place = location.replace(" ", "+")
    r = requests.get("https://nominatim.openstreetmap.org/search?q={0}&format=json".format(place))
    try:
        response = json.loads(r.text)
        placeData = response[0]
        lat = float(placeData["lat"])
        lon = float(placeData["lon"])
        datetimeTemp = datetime.now()

        day_of_year = int(datetimeTemp.strftime("%j"))
        if 88 < day_of_year < 298:
            timezone = 2
        else:
            timezone = 1
        sT = sun_rise_set.sunsetTimes(lat, lon, day_of_year, timezone)
        sunrise, sunset = sT.converted
        return sunrise, sunset
    except:
        print("[WARINING] Something went wrong with the Sunrise and Sunset module!")
