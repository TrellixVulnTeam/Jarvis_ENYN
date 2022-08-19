import traceback
from datetime import datetime

from src import log
from src.modules import ModuleWrapper

SECURE = True

# toDo: use database connection

def isValid(text: str) -> bool:
    # toDo
    return False


def handle(text: str, wrapper: ModuleWrapper) -> None:
    if wrapper.user is None:
        return
    try:
        if "elapsed_awaiting_notifications" not in wrapper.user.keys():
            wrapper.user["elapsed_awaiting_notifications"] = []

        for item in wrapper.user["waiting_notifications"]:
            # clear the storage
            date = item.get("Date")
            now = datetime.now()
            if date is not None and type(date) is type(datetime):
                # if Date is defined and in the past: move it
                if date.day < now.day and date.month <= now.month:
                    wrapper.user["elapsed_awaiting_notifications"].append(item)
                    wrapper.user["waiting_notifications"].remove(item)

        # create a parameter with storage, so we can work with it (delete items and co)
        infos = wrapper.user["waiting_notifications"].copy()
        print(f"Text: {text} and type: {type(text)}")

        # module was called via wrapper
        for item in infos:
            date = item.get("Date")
            if date is None:
                continue
            elif type(date) is type([]) and date is not []:
                for d in date:
                    now = datetime.now()
                    if not (d.day == now.day and d.month == now.month):
                        infos.remove(item)
            else:
                now = datetime.now()
                if not (date.day == now.day and date.month == now.month):
                    infos.remove(item)

        if len(infos) >= 1:
            # if at least one or more item(s) is|are there, go on
            if len(infos) > 1:
                wrapper.say("Hier noch ein paar wichtige Nachrichten für dich:")
            else:
                wrapper.say("Hier noch eine wichtige Nachricht für dich:")

            for item in infos:
                txt = item.get("message")
                # It also checks whether the notification is audio or not
                if txt.startswith("\Audio:"):
                    wrapper.play(pfad=item.remove("\Audio:"))
                else:
                    wrapper.say(txt)
                wrapper.user["waiting_notifications"].remove(item)
    except RuntimeError:
        log.warning('Something went wrong in Module "wartende_benachrichtigungen"')
        traceback.print_exc()
