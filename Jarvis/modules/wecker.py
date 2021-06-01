import datetime


def isValid(text):
    text = text.lower()
    if 'weck ' in text or 'wecke' in text:
        return True


def handle(text, core, skills):
    text = text.lower()
    time = core.analysis["time"]
    minute = str(time['minute']) if time['minute'] != 0 else ''
    ton = core.user.get('wecker_ton')
    """
    if not 'morgens' in text and not 'früh' in text and not 'abends' in text:
        core.say("Meintest du {} Uhr {} morgens oder Abends?".format(str(time['hour']-12), minute))
        response =core.listen()
        if 'morgens' in text or 'früh' in text:
            time = time -12
    """
    stunde = str(time['hour'])
    if 'lösch' in text or 'beend' in text or ('schalt' in text and 'ab' in text):
        if 'täglich' in text or 'jeden tag' in text:
            days = ["montag", "dienstag", "mittwoch", "donnerstag", "freitag", "samstag", "sonntag"]
            try:
                time = core.analysis["time"]
                wecker = {'Zeit': time, 'User': core.user, 'Ton': ton}
                for item in days:
                    core.local_storage["regular_alarm"][item].remove(wecker)
                core.say("Täglichen Wecker um {} Uhr {} gelöscht.".format(stunde, minute))
            except:
                core.say("Welchen Wecker soll ich ausschalten?")
                for item in core.local_storage["regular_alarm"].keys():
                    stunde = item["Zeit"]["hour"]
                    minute = item["Zeit"]["minute"]
                    core.say("{} Uhr {}".format(stunde, minute))
                response = core.listen()
                wecker = {'Zeit': core.Analyzer.analyze(response)['time'], 'User': core.user, 'Ton': ton}
                for item in core.local_storage["regular_alarm"].keys():
                    core.local_storage["regular_alarm"][item].remove(wecker)
                core.say(
                    "Täglichen Wecker um {} Uhr {} gelöscht.".format(wecker['Zeit']['hour'], wecker['Zeit']['minute']))

        elif 'alle' in text:
            core.say('Soll ich auch die regelmäßigen Wecker löschen?')
            response = core.listen()
            if skills.is_approved(response):
                core.local_storage["Wecker"] = []
            if 'was' in response and ('regelmäßig' in response or 'sind' in response):
                core.say(
                    'Damit sind diese Wecker gemeint, welche zum Beispiel jeden Dienstag oder jeden Tag klingeln. Also solche, die regelmäßig wiederholt werden. Soll ich auch die regelmäßigen Wecker löschen?')
                response = core.listen()
            if skills.is_approved(response):
                core.local_storage["regular_alarm"] = []

        elif 'wochenende' in text:
            days = ["samstag", "sonntag"]
            try:
                time = core.analysis["time"]
                wecker = {'Zeit': time, 'User': core.user, 'Ton': ton}
                for item in days:
                    core.local_storage["regular_alarm"][item].remove(wecker)
                core.say("Täglichen Wecker um {} Uhr {} gelöscht.".format(stunde, minute))
            except:
                core.say("Welchen Wecker soll ich ausschalten?")
                for item in days:
                    stunde = item["Zeit"]["hour"]
                    minute = item["Zeit"]["minute"]
                    core.say("{} Uhr {}".format(stunde, minute))
                response = core.listen()
                wecker = {'Zeit': core.Analyzer.analyze(response)['time'], 'User': core.user, 'Ton': ton}
                for item in days:
                    core.local_storage["regular_alarm"][item].remove(wecker)
                core.say("Wecker am Wochenende um {} Uhr {} gelöscht.".format(wecker['Zeit']['hour'],
                                                                              wecker['Zeit']['minute']))

        elif 'wochentag' in text or 'unter der woche' in text:
            days = ["montag", "dienstag", "mittwoch", "donnerstag", "freitag"]
            try:
                time = core.analysis["time"]
                wecker = {'Zeit': time, 'User': core.user, 'Ton': ton}
                for item in days:
                    core.local_storage["regular_alarm"][item].remove(wecker)
                core.say("Wecker unter der Woche um {} Uhr {} gelöscht.".format(stunde, minute))
            except:
                core.say("Welchen Wecker soll ich ausschalten?")
                for item in days:
                    stunde = item["Zeit"]["hour"]
                    minute = item["Zeit"]["minute"]
                    core.say("{} Uhr {}".format(stunde, minute))
                response = core.listen()
                wecker = {'Zeit': core.Analyzer.analyze(response)['time'], 'User': core.user, 'Ton': ton}
                for item in days:
                    core.local_storage["regular_alarm"][item].remove(wecker)
                core.say("Wecker unter der Woche um {} Uhr {} gelöscht.".format(wecker['Zeit']['hour'],
                                                                                wecker['Zeit']['minute']))

        elif 'jeden' in text or 'jedem' in text:
            days = skills.get_text_beetween('jeden', text)
            for item in days:
                if item.lower() not in ["montag", "dienstag", "mittwoch", "donnerstag", "freitag", "samstag",
                                        "sonntag"]:
                    days.remove(item)
            try:
                time = core.analysis["time"]
                wecker = {'Zeit': time, 'User': core.user, 'Ton': ton}
                for item in days:
                    core.local_storage["regular_alarm"][item].remove(wecker)
                core.say("Täglichen Wecker um {} Uhr {} gelöscht.".format(stunde, minute))
            except:
                core.say("Welchen Wecker soll ich ausschalten?")
                for item in days:
                    stunde = item["Zeit"]["hour"]
                    minute = item["Zeit"]["minute"]
                    core.say("{} Uhr {}".format(stunde, minute))
                response = core.listen()
                wecker = {'Zeit': core.Analyzer.analyze(response)['time'], 'User': core.user, 'Ton': ton}
                for item in days:
                    core.local_storage["regular_alarm"][item].remove(wecker)
                core.say("Wecker unter der Woche um {} Uhr {} gelöscht.".format(wecker['Zeit']['hour'],
                                                                                wecker['Zeit']['minute']))

        else:
            if 'Wecker' in core.local_storage.keys():
                wecker = {'Zeit': core.analysis['datetime'], 'User': core.user, 'Ton': ton}
                core.local_storage['Wecker'].remove(wecker)
                core.say("Wecker gelöscht: {}, {} Uhr {}".format(get_reply(core, time), stunde, minute))
            else:
                core.say("Für diesem Tag hast du noch keinen Wecker gestellt.")

    else:
        if 'täglich' in text or 'jeden tag' in text or 'jeden morgen' in text or 'jeden abend' in text:
            wecker = {'Zeit': time, 'User': core.user, 'Ton': ton}
            for item in core.local_storage["regular_alarm"].keys():
                core.local_storage["regular_alarm"][item].append(wecker)
            core.say("Wecker gestellt für jeden Tag um {} Uhr {}.".format(stunde, minute))
        elif 'wochenende' in text:
            wecker = {'Zeit': time, 'User': core.user, 'Ton': ton}
            core.local_storage["regular_alarm"]["samstag"].append(wecker)
            core.local_storage["regular_alarm"]["sonntag"].append(wecker)
            core.say("Wecker gestellt für jeden Samstag und Sonntag um {} Uhr {}".format(stunde, minute))
        elif 'wochentags' in text or 'unter der woche' in text:
            wecker = {'Zeit': time, 'User': core.user, 'Ton': ton}
            core.local_storage["regular_alarm"]["montag"].append(wecker)
            core.local_storage["regular_alarm"]["dienstag"].append(wecker)
            core.local_storage["regular_alarm"]["mittwoch"].append(wecker)
            core.local_storage["regular_alarm"]["donnerstag"].append(wecker)
            core.local_storage["regular_alarm"]["freitag"].append(wecker)
            core.say("Wecker gestellt für jeden Wochentag um {} Uhr {}.".format(stunde, minute))
        elif 'jeden' in text or 'jedem' in text:
            if not 'regular_alarm' in core.local_storage.keys():
                core.local_storage["regular_alarm"] = []
            wecker = {'Zeit': time, 'User': core.user, 'Ton': ton}
            days = skills.get_text_beetween('jeden', text)
            for item in days:
                if item.lower() in ["montag", "dienstag", "mittwoch", "donnerstag", "freitag", "samstag", "sonntag"]:
                    core.local_storage["regular_alarm"][item.lower()].append(wecker)
                else:
                    days.remove(item)
                print(days)
                print(skills.get_enumerate(days))
            core.say("Wecker gestellt für jeden {} um {} Uhr {}.".format(skills.get_enumerate(days), stunde, minute))
        else:
            wecker = {'Zeit': core.analysis['datetime'], 'User': core.user, 'Ton': ton}
            if 'Wecker' in core.local_storage.keys():
                core.local_storage['Wecker'].append(wecker)
            else:
                core.local_storage['Wecker'] = [wecker]
            core.say("Wecker gestellt für {}, {} Uhr {}".format(get_reply(core, time), stunde, minute))


def get_reply(core, time):
    now = datetime.datetime.today().day
    monat = str(time['month'])
    tag = str(time['day'])
    if int(monat) <= 9:
        monat = '0' + monat
    if len(tag) == 1:
        tag = '0' + tag
    tage = {'01': 'ersten', '02': 'zweiten', '03': 'dritten', '04': 'vierten', '05': 'fünften',
            '06': 'sechsten', '07': 'siebten', '08': 'achten', '09': 'neunten', '10': 'zehnten',
            '11': 'elften', '12': 'zwölften', '13': 'dreizehnten', '14': 'vierzehnten', '15': 'fünfzehnten',
            '16': 'sechzehnten', '17': 'siebzehnten', '18': 'achtzehnten', '19': 'neunzehnten', '20': 'zwanzigsten',
            '21': 'einundzwanzigsten', '22': 'zweiundzwanzigsten', '23': 'dreiundzwanzigsten',
            '24': 'vierundzwanzigsten',
            '25': 'fünfundzwanzigsten', '26': 'sechsundzwanzigsten', '27': 'siebenundzwanzigsten',
            '28': 'achtundzwanzigsten',
            '29': 'neunundzwanzigsten', '30': 'dreißigsten', '31': 'einunddreißigsten', '32': 'zweiunddreißigsten'}
    monate = {'01': 'Januar', '02': 'Februar', '03': 'März', '04': 'April', '05': 'Mai', '06': 'Juni',
              '07': 'Juli', '08': 'August', '09': 'September', '10': 'Oktober', '11': 'November',
              '12': 'Dezember'}
    if int(tag) == int(now):
        return 'heute'
    elif tag == now + 1:
        return 'morgen'
    elif tag == now + 2:
        return 'übermorgen'
    else:
        core_output = tage.get(tag) + monate.get(monat)
        messenger_output = tag + '. ' + monat
        return 'den ' + core.correct_output(core_output, messenger_output)
