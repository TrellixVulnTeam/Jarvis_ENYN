import datetime

INTERVALL = 2


def run(core, skills):
    if 'alarm' in core.local_storage.keys():
        alarms = core.local_storage.get('alarm')
        for repeat in alarms:
            print(alarms)
            # iterate over 'regular' and 'single'
            for day in alarms[repeat]:
                for alarm in alarms[repeat][day]:
                    print(f'repeat: {repeat}, day: {day}, alarm: {alarm}, isdaycorrect: {is_day_correct(day)}, active: {get_total_seconds(alarm["time"]) <= 0 and alarm["active"]}')
                    # iterate over each weekday
                    if is_day_correct(day) and get_total_seconds(alarm["time"]) <= 0 and alarm["active"]:
                        dic = {'Text': alarm["text"], 'Ton': alarm["sound"], 'User': alarm["user"]}
                        core.start_module(name='weckerausgabe', text=dic)
                        alarms[repeat][day].remove(alarm)
                        core.local_storage['alarm'] = alarms


def is_day_correct(day):
    if day.lower() == datetime.datetime.today().strftime("%A").lower():
        return True
    return False


def get_total_seconds(alarm_time):
    now = datetime.datetime.now()
    now_seconds = now.hour * 3600 + now.minute * 60 + now.second
    print(f'alarm_seconds: {alarm_time["total_seconds"]} - now-seconds: {now_seconds} = {alarm_time["total_seconds"] - now_seconds}')
    return alarm_time["total_seconds"] - now_seconds
