SECURE = True


def isValid(text):
    return False


def handle(text, core, skills):
    infos = core.local_storage["users"][core.user]["wartende_benachrichtigungen"]
    if len(infos) >= 1:
        if len(infos) > 1:
            text = "Hier noch ein paar wichtige Nachrichten für dich:"
        else:
            text = "Hier noch eine wichtige Nachricht für dich:"

        core.say(text)
        for item in infos:
            # Es wird auch überprüft, ob die Benachrichtigung eventuell eine Audio ist, oder nicht
            if item.startswith("\Audio:"):
                core.play(pfad=item.remove("\Audio:"))
            else:
                core.say(item)
            core.local_storage["users"][core.user]["wartende_benachrichtigungen"].remove(item)
