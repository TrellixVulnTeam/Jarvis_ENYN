import logging
from datetime import datetime

SECURE = True


def isValid(text):
    return False


def handle(text, core, skills):
    if core.user is None:
        return
    try:
        if not "waiting_notifications" in core.user.keys():
            core.user["waiting_notifications"] = []

        if not "elapsed_awaiting_notifications" in core.user.keys():
            core.user["elapsed_awaiting_notifications"] = []

        for item in core.user["waiting_notifications"]:
            # clear the storage
            if item.get("Date") is not None and item.get("Date") is not []:
                # if Date is defined and in the past: move it
                if (item.get("Date") - datetime.now()) < 0:
                    core.user["elapsed_awaiting_notifications"].append(item)
                    core.user["waiting_notifications"].remove(item)

        # create a parameter with storage, so we can work with it (delete items and co)
        infos = core.user["waiting_notifications"]

        if text is None:
            # module was called via core
            for item in infos:
                if type(item.get("Date")) is type([]) and item.get("Date") is not []:
                    for date in item.get("Date"):
                        if not date == datetime.today():
                            infos.remove(item)
                else:
                    if not item.get("Date") == datetime.today():
                        infos.remove(item)
        else:
            for item in infos.keys():
                if not item in text:
                    infos.remove(item)

        if len(infos) >= 1:
            # if at least one or more item(s) is|are there, go on
            if len(infos) > 1:
                core.say("Hier noch ein paar wichtige Nachrichten für dich:")
            else:
                core.say("Hier noch eine wichtige Nachricht für dich:")

            for item in infos.get("message"):
                # It also checks whether the notification is audio or not
                if item.startswith("\Audio:"):
                    core.play(pfad=item.remove("\Audio:"))
                else:
                    core.say(item)
                core.local_storage["users"][core.user]["waiting_notifications"].remove(item)
    except:
        logging.info('Something went wrong in Module "wartende_benachrichtigungen"')
