import datetime

INTERVALL = 2


def run(core, skills):
    if 'alarm' in core.local_storage.keys():
        alarms = core.local_storage.get('alarm')
        for repeat in alarms:
            # iterate over 'regular' and 'single'
            for day in alarms[repeat]:
                for alarm in alarms[repeat][day]:
                    # iterate over each weekday
                    if is_day_correct(day):
                        if get_total_seconds(alarm["time"]) <= 0 and alarm["active"]:
                            dic = {'Text': alarm["text"], 'Ton': alarm["sound"], 'User': alarm["user"]}
                            core.start_module(name='weckerausgabe', text=dic)
                            alarms[repeat][day].remove(alarm)
                            core.local_storage['alarm'] = alarms
                        elif get_total_seconds(alarm["time"]) <= 1800:
                            core.start_module(name="wecker_sonnenaufgang", text="")


def is_day_correct(day):
    if day.lower() == datetime.datetime.today().strftime("%A").lower():
        return True
    return False


def get_total_seconds(alarm_time):
    now = datetime.datetime.now()
    now_seconds = now.hour * 3600 + now.minute * 60 + now.second
    return alarm_time["total_seconds"] - now_seconds
