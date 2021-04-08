from time import sleep
import datetime

SECURE = True


def isValid(text):
    text = text.lower()
    if (text.startswith(
            'hallo') or text == 'hi' or text == 'hey' or text == '/start') and not 'geht' in text or 'läuft' in text:
        return True
    elif 'wie' in text and ('uhr' in text or 'spät' in text):
        return True
    elif 'welchen tag' in text or 'welcher tag' in text or 'wochentag' in text or 'datum' in text or 'den wievielten haben wir heute' in text or 'der wievielte ist es' in text:
        return True
    elif 'guten' in text and 'tag' in text:
        return True
    elif 'guten' in text and 'morgen' in text:
        return True
    elif 'guten' in text and 'abend' in text:
        return True
    elif 'gute' in text and 'nacht' in text:
        return True
    elif 'timer' in text or 'stoppuhr' in text or 'countdown' in text:
        return True


def handle(text, core, skills):
    text = text.lower()
    now = datetime.datetime.now()
    # wochentag = datetime.datetime.today().weekday()
    time = now.hour
    if ' uhr ' in text or 'spät' in text:
        core.say('Es ist ' + get_time(now))
    elif 'welchen tag' in text or 'welcher tag' in text or 'wochentag' in text or 'datum' in text or 'den wievielten haben wir heute' in text or 'der wievielte ist es' in text:
        core.say(get_day(text))
    elif 'hallo' in text:
        core.say('Hallo!')
    elif 'guten' in text and 'tag' in text:
        if time >= 20 or time <= 4:
            core.say('Naja "Tag" würde ich das nicht mehr nennen, aber ich wünsche dir auch einen guten Abend')
        elif 5 <= time <= 20:
            core.say('Guten Tag!')
    elif 'guten' in text and 'morgen' in text:
        if time is 4 or time is 5:
            core.say('Hast du heute was wichtiges anstehen?')
            response = core.listen
            if 'ja' in text:
                core.say('Dann wünsche ich dir dabei viel Erfolg!')
            else:
                core.say('Dann schlaf ruhig weiter, es ist noch viel zu früh, um aufzustehen.')
        elif 6 <= time <= 10:
            core.say('Guten Morgen!')
        elif time is 11 or time is 12:
            core.say('Wurde aber auch langsam Zeit. Aber dennoch auch dir einen guten Morgen.')
        elif 14 <= time <= 18:
            core.say(
                'Ob es noch Morgen ist, liegt wohl im Blickwinkel des Betrachters. Ich würde eher sagen, dass es Mittag oder Nachmittag ist.')
        elif time >= 19 or time <= 3:
            core.say(
                'Also Morgen ist es auf jeden Fall nicht mehr. Daher wünsche ich dir einfach Mal einen guten Abend.')
        else:
            core.say('Hallo!')
    elif 'guten' in text and 'abend' in text:
        if 6 <= time <= 17:
            core.say(
                'Ob es noch Abend ist, liegt wohl im Blickwinkel des Betrachters. In Amerika ist es jetzt in der Tat Abend.')
        elif time >= 18 or time <= 5:
            core.say('Gute nacht')
        else:
            core.say('Guten Abend.')

    elif 'gute' in text and 'nacht' in text:
        if 1 <= time <= 13:
            core.say('Du solltest echt langsam ins Bett gehen.')
        elif (8 <= time <= 24) or time is 0:
            core.say('Gute Nacht.')
        else:
            core.say('Eine sehr interessante Definition der derzeitigen Uhrzeit.')
        core.say('Soll ich dich morgen wecken?')
        response = core.listen()
        if 'ja' in response or 'gerne' in response or 'bitte' in response:
            if core.analysis['datetime'] is None:
                core.say('Wann soll ich dich denn wecken?')
                response_two = core.listen()
                text = 'weck ' + response_two
                core.start_module(text=text)
            else:
                core.start_module(text=text)
        else:
            core.say('Okay, dann wünsche ich dir eine gute Nacht.')
    elif 'timer' in text:
        timer(text, core, skills)
    elif 'stoppuhr' in text:
        stopwatch(text, core, skills)
    elif 'counter' in text:
        countdown(text, core)
    else:
        core.say('Aaahhh, das sind zu viele Möglichkeiten mit Zeiten umzugehen. Bitte versuche es erneut.')


def timer(text, core, skills):
    if 'start' in text:
        core.say('Sicher, dass du nicht die Stoppuhr meinst?')
        core.say('Soll ich für dich eine Stoppuhr starten?')
        response = core.listen()
        if 'ja' in response or 'bitte' in text or 'gerne' in text:
            core.say('Okay, soll ich eine Stoppuhr nur für dich oder für alle starten?')
            response = core.listen()
            if 'mich' in response or 'meine' in response:
                stopwatch('starte meine stoppuhr', core, skills)
            else:
                stopwatch('starte die stoppuhr', core, skills)
        else:
            core.say('Okay. Dann mach ich nichts.')

    elif 'stell' in text or 'beginn' in text:
        # Einheitlichkeit
        text = text.replace(' auf ', ' in ')

        time = core.Analyzer.analyze(text)['datetime']

        temp_text = "Dein Timer ist abgelaufen."

        duration = skills.get_text_beetween('in', text, output='String')

        # Zeit: Um wieviel Uhr der Timer fertig ist; Text: Antwort von Core; Benutzer; Raum; Dauer: Wie lange der Timer gehen soll
        E_eins = {'Zeit': time, 'Text': temp_text, 'Dauer': duration, 'Benutzer': core.user}

        # Vermeidung von Redundanz. Wird für 1 und mehrere Timer verwendet
        # Aufzählung wenn mehrere Timer
        if 'Timer' in core.local_storage.keys():
            core.local_storage['Timer'].append(E_eins)
            anzahl = len(core.local_storage['Timer'])
            core.say(str(anzahl) + '. Timer: ' + str(E_eins['Dauer']) + ' ab jetzt.')
        else:
            core.local_storage['Timer'] = [E_eins]
            core.say(str(E_eins['Dauer']) + ' ab jetzt.')

    elif 'wie' in text and 'lange' in text:
        #Begrenzt Timer auf die des Benutzers
        user_timer = core.local_storage['Timer']
        aussage_timer = ''
        if len(user_timer) == 0:
            aussage_timer = "Du hast keinen aktiven Timer!"
        else:
            for item in user_timer:
                #erst einmal checken, ob der Timer vlt eigentlich schon abgelaufen ist, was eigentlich nicht passieren sollte.
                now = datetime.datetime.now()
                timer_abgelaufen = (now - item["Zeit"])
                if timer_abgelaufen:
                    user_timer.remove(item)
                    core.local_storage["Timer"].remove(item)

                # Verbleibende Zeit runden
                genaue_zeit = item['Zeit'] - datetime.datetime.now()

                tage = genaue_zeit.days
                sekunden = genaue_zeit.seconds

                # Wenn Timer kurz vor Ende, dann überspringen
                if tage == 0 and sekunden<3:
                    continue

                sekunden = genaue_zeit.seconds

                if (sekunden % 60) >= 30:
                    sekunden += 60 - (sekunden % 60)
                if sekunden > 30:
                    sekunden += 60 - (sekunden % 60)

                verbleibende_zeit = datetime.timedelta()

                aussage_timer += 'Du hast einen ' + item['Dauer'] + ' mit noch etwa ' + get_time_differenz(skills, verbleibende_zeit) + ' verbleibend.\n'

            if len(user_timer) > 1:
                aussage = 'Du hast ' + str(len(core.local_storage['Timer'])) + ' Timer gestellt.\n' + aussage_timer

        core.say(aussage_timer)


    elif 'lösch' in text or 'beend' in text or 'stopp' in text:
        user_timer = core.local_storage["Timer"]
        if 'Timer' in core.local_storage.keys():
            if 'alle' in text:
                for item in user_timer:
                    core.local_storage['Timer'].remove(item)
                    core.say("Alle Timer von dir gelöscht!")

            elif 'von' in text:
                duration = skills.get_text_beetween('von', text, output='String')
                for item in user_timer:
                    if item["Dauer"] == duration:
                        timer = core.local_storage["Timer"].remove(item)
                        core.local_storage["Timer"] = timer
                        core.say("Alles klar, ich habe den Timer mit der Dauer " + item["Dauer"] + " gelöscht.")
                        break
            else:
                if core.messenger_call:
                    text = "Folgende Timer habe ich in deiner Liste gefunden:\n"
                    i = 1
                    for item in user_timer:
                        temp_string = str(i)+". Dauer: "+item["Dauer"]+" Du hast den Timer im Raum '"+item["Raum"]+"' gestellt.\n"
                        text = text + temp_string
                    text = text + "Bitte schreib nur die Ziffer des Timers, welcher gelöscht werden soll."
                    core.say(text, output='messenger') #Der output ist eigentlich unnötig, aber wir gehen auf nummer sicher
                    number = core.listen()
                    if number <= len(user_timer):
                        timer = core.local_storage["Timer"].remove(user_timer[int(number)-1])
                        core.say("Ich habe den Timer mit der Dauer " + item["Dauer"]+" gelöscht!", output='messenger')
                    else:
                        core.say("Deine Eingabe war ungültig!", output='messenger')
                else:
                    core.say(
                        "Ich werde dir jetzt die Zeitlängen aller Timer von dir vorlesen. Du sagst dann einfach ja, wenn es das richtige ist.")
                    for item in user_timer:
                        core.say(item["Dauer"])
                        response = core.listen()
                        if "ja" in response:
                            timer = core.local_storage["Timer"].remove(item)
                            core.local_storage["Timer"] = timer
                            core.say(core.correct_output("Alles klar, ich habe den Timer mit der Dauer " + item["Dauer"] + " gelöscht."))
                            break

        else:
            core_array = ["Du hast noch gar keinen Teimer gestellt, daher kann ich auch keinen löschen"]
            messenger_array = ["Du hast noch gar keinen Timer gestellt, daher kann ich auch keinen löschen"]
            core.say(core.correct_output(core_array, messenger_array))

    elif 'beend' in text:
        core.say('Ich kann einen Timer nicht beenden, nur löschen. Vielleicht meinst du ja die Stoppuhr.')
    else:
        core.say('Leider weiß ich nicht, was ich mit dem Timer machen soll.')


def stopwatch(text, core, skills):
    if 'start' in text:
        if 'stoppuhr' in core.local_storage.keys():
            core.say('Es läuft bereits eine Stoppuhr. Soll ich diese erst stoppen?')
            response = core.listen()
            if 'ja' in response:
                core.say('Alles klar. Die alte Stoppuhr wurde bei {} gestoppt und eine neue gestartet.'.format(get_time(core.local_storage['stoppuhr']), get_time_differenz(core.local_storage['stoppuhr'], skills)))
                core.local_storage['stoppuhr'] = datetime.datetime.now()
            else:
                core.say('Alles klar, die alte Stoppuhr läuft weiter.')
        else:
            core.say('Alles klar, die Stoppuhr wurde um {} gestartet.'.format(get_time(datetime.datetime.now())))
            core.local_storage['stoppuhr'] = datetime.datetime.now()

    elif 'stopp' in text or 'beende' in text:

        if 'stoppuhr' in core.local_storage.keys() and core.local_storage['stoppuhr'] != '':
            core.say('Alles klar, die Stoppuhr wurde um {} gestoppt. Sie dauerte {}.'.format(get_time(datetime.datetime.now()), get_time_differenz(core.local_storage["stoppuhr"], skills)))
            core.local_storage['stoppuhr'] = ''
        else:
            core.say('Es wurde noch keine Stoppuhr gestartet. Soll ich eine starten?')
            response = core.listen()
            if 'ja' in response:
                core.say('Alles klar, Stoppuhr wurde um {} gestartet'.format(
                    get_time(datetime.datetime.now())))
                core.local_storage['stoppuhr'] = datetime.datetime.now()
    else:
        core.say(
            'Ich kann die Stoppuhr nur starten oder stoppen.')  # bald sollte noch eine Pause-Funktion hinzugefügt werden


def countdown(text, core):
    text = text.split(' ')
    timecode = -1
    for i in range(len(text)):
        if text[i] is 'von':
            timecode = int(text[i+1])
    if 'minute' in text:
        timecode = timecode * 60
    elif 'stunde' in text:
        core.say('Ist das nicht ein bisschen zu lang?')
        response = core.listen()
        if 'nein' in text:
            timecode = timecode * 3600

    if timecode is not -1:
        for i in range(timecode):
            time = timecode - i
            core.say(str(time))
            sleep(1)
    else:
        core.say('Tut mir leid, leider habe ich nicht verstanden, von wo ich herunter zählen soll')


def get_time_differenz(start_time, skills, time=datetime.datetime.now()):
    aussage = []
    if time == None:
        dz = start_time
    else:
        dz = start_time - time
    days = dz.days
    seconds = dz.seconds
    microseconds = dz.microseconds

    years = 0
    hours = 0
    minutes = 0

    if days >= 365:
        years = int(days / 365)
        days = days % 365
    if seconds >= 3600:
        hours = int(seconds / 3600)
        seconds = seconds % 3600
    if seconds >= 60:
        minutes = int(seconds / 60)
        seconds = seconds % 60
    if microseconds >= 5:
        seconds += 1

    if years == 1:
        aussage.append('einem Jahr')
    elif years > 1:
        aussage.append(str(years) + ' Jahren')
    if days == 1:
        aussage.append('einem Tag')
    elif days > 1:
        aussage.append(str(days) + ' Tagen')
    if hours == 1:
        aussage.append('einer Stunde')
    elif hours > 1:
        aussage.append(str(hours) + ' Stunden')
    if minutes == 1:
        aussage.append('einer Minute')
    elif minutes > 1:
        aussage.append(str(minutes) + ' Minuten')
    if seconds == 1:
        aussage.append('einer Sekunde')
    elif seconds > 1:
        aussage.append(str(seconds) + ' Sekunden')
    return skills.get_enumerate(aussage)

def get_time(i):
    stunde = i.hour
    naechste_stunde = stunde + 1
    if naechste_stunde == 24:
        naechste_stunde = 0
    minute = i.minute
    stunde = str(stunde) if stunde > 9 else '0' + str(stunde)
    minute = str(minute) if minute > 9 else '0' + str(minute)
    if minute == 0:
        ausgabe = stunde + ' Uhr.'
    elif minute == 5:
        ausgabe = 'fünf nach ' + stunde
    elif minute == 10:
        ausgabe = 'zehn nach ' + stunde
    elif minute == 15:
        ausgabe = 'viertel nach ' + stunde
    elif minute == 20:
        ausgabe = 'zwanzig nach ' + stunde
    elif minute == 25:
        ausgabe = 'fünf vor halb ' + stunde
    elif minute == 30:
        ausgabe = 'halb ' + naechste_stunde
    elif minute == 35:
        ausgabe = 'fünf nach halb ' + naechste_stunde
    elif minute == 40:
        ausgabe = 'zwanzig vor ' + naechste_stunde
    elif minute == 45:
        ausgabe = 'viertel vor ' + naechste_stunde
    elif minute == 50:
        ausgabe = 'zehn vor ' + naechste_stunde
    elif minute == 55:
        ausgabe = 'fünf vor ' + naechste_stunde
    else:
        ausgabe = stunde + ':' + minute + ' Uhr'
    return ausgabe


def get_day(i):
    now = datetime.datetime.now()
    wochentag = datetime.datetime.today().weekday()
    tage = {0: 'Montag', 1: 'Dienstag', 2: 'Mittwoch', 3: 'Donnerstag', 4: 'Freitag', 5: 'Samstag', 6: 'Sonntag'}

    ausgabe = 'Heute ist ' + str(tage.get(wochentag)) + ' der ' + str(now.day) + '.' + str(now.month) + '.'
    return ausgabe
