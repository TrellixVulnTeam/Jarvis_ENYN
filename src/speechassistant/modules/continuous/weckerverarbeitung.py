from datetime import datetime
from core import ModuleWrapperContinuous

INTERVALL = 60


def run(core: ModuleWrapperContinuous):
    active: list[dict]
    init: list[dict]
    now: datetime = datetime.now()
    alarm_interface = core.data_base.alarm_interface
    active, init = alarm_interface.get_alarms(active=True)

    for item in active:
        dic = {"text": item["text"], "sound": item["sound"], "user": item["user"]}
        core.start_module(name="weckerausgabe", text=dic)
        alarm_interface.update_alarm(
            item["aid"], _last_executed=f"{now.day}.{now.month}.{now.year}"
        )

    for item in init:
        core.start_module(name="wecker_sonnenaufgang", text="")
        alarm_interface.update_alarm(item["aid"], _initiated=True)
