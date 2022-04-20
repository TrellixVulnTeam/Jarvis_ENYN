from datetime import datetime

from src.speechassistant.core import ModuleWrapperContinuous

INTERVALL = 2


def run(core: ModuleWrapperContinuous, skills):
    now = datetime.now()

    routine_interface = core.data_base.routine_interface

    result_set = routine_interface.get_routines()

    for routine in core.local_storage["routines"]:
        if is_day_correct(now, routine, skills) and is_time_correct(now, routine, core):
            core.start_module(name="start_routine", text=routine)


def is_day_correct(now, inf, skills):
    is_correct = False
    # check if no day is specified
    all_false = True
    for day in inf["retakes"]["days"].keys():
        if day is True or not day == []:
            all_false = False
    if all_false:
        return True

    day_name = skills.Statics.numb_to_day.get(str(now.isoweekday()))
    day_inf = inf.get("retakes").get("days")
    if day_inf["daily"] or day_inf[day_name]:
        is_correct = True
    for day in day_inf["date_of_day"]:
        if day == skills.Statics.numb_to_day.get(now.day):
            is_correct = True
    return is_correct


def is_time_correct(now, inf, core):
    # after_alarm is ignored, since this is only called by the alarm itself
    time_inf = inf["retakes"]["activation"]
    if time_inf["clock_time"] is not [""] and time_inf["clock_time"] is not []:
        for time in time_inf["clock_time"]:
            if len(time.split(":")) == 2:
                hour = int(time.split(":")[0])
                minute = int(time.split(":")[1])
                if now.hour >= hour and now.minute >= minute:
                    return True
    if inf["retakes"]["activation"]["after_sunrise"]:
        if is_sunrise(core.local_storage, now):
            return True
    if inf["retakes"]["activation"]["after_sunset"]:
        if is_sunset(core.local_storage, now):
            return True
    return False


def is_sunrise(core, now):
    suntimes = core.weather.get_sunrise_sunset()
    if (suntimes[0] // 60) >= now.hour and (suntimes[0] % 60) >= now.minute:
        return True


def is_sunset(core, now):
    suntimes = core.weather.get_sunrise_sunset()
    if (suntimes[1] // 60) >= now.hour and (suntimes[1] % 60) >= now.minute:
        return True