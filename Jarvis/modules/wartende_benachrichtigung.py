import datetime

SECURE = True


def isValid(text):
    return False


def handle(text, core, skills):
    infos = core.local_storage["users"][core.user]["wartende_benachrichtigungen"]

    if text == None:
        # module was called via core
        for item in infos:
            if type(item.get("Date")) is type([]):
                for date in item.get("Date"):
                    if not date == datetime.datetime.today():
                        infos.remove(item)
            else:
                if item.get("Date") == datetime.datetime.today():
                    infos.remove(item)
    else:
        for item in infos.keys():
            if not item in text:
                infos.remove(item)

    if len(infos) >= 1:
        # if at least one or more item(s) is|are there, go on
        if len(infos) > 1:
            text = "Hier noch ein paar wichtige Nachrichten für dich:"
        else:
            text = "Hier noch eine wichtige Nachricht für dich:"

        core.say(text)
        for item in infos.get("message"):
            # Es wird auch überprüft, ob die Benachrichtigung eventuell eine Audio ist, oder nicht
            if item.startswith("\Audio:"):
                core.play(pfad=item.remove("\Audio:"))
            else:
                core.say(item)
            core.local_storage["users"][core.user]["wartende_benachrichtigungen"].remove(item)
