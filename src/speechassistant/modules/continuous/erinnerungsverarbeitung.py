import datetime

from src.speechassistant.core import ModuleWrapperContinuous

INTERVALL = 10


def run(core: ModuleWrapperContinuous, profile):
    result_set: list[dict]

    reminder_interface = core.data_base.reminder_interface

    result_set = reminder_interface.get_reminder(passed=True)

    for item in result_set:
        core.start_module(
            name="erinnerungsausgabe", text=item["text"], user=item["uid"]
        )
        reminder_interface.delete_reminder(item["id"])
