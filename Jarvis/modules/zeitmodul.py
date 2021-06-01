from time import sleep
import datetime

SECURE = True


def isValid(text):
    text = text.lower()
    if 'timer' in text or 'stoppuhr' in text or 'countdown' in text:
        return True


def handle(text, core, skills):
    text = text.lower()
    now = datetime.datetime.now()
    # wochentag = datetime.datetime.today().weekday()

    if 'timer' in text:
        timer(text, core, skills)
    elif 'stoppuhr' in text:
        stopwatch(text, core, skills)
    elif 'counter' in text:
        countdown(text, core)
    else:
        core.say('Aaahhh, das sind zu viele Möglichkeiten mit Zeiten umzugehen. Bitte versuche es erneut.')


def timer(text, core, skills):
    if 'start' in text:
        core.say('Sicher, dass du nicht die Stoppuhr meinst? Soll ich für dich eine Stoppuhr starten?')
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
        text = text.replace(' von ', ' in ')

        time = core.Analyzer.analyze(text)['datetime']

        temp_text = "Dein Timer ist abgelaufen."

        duration = skills.get_text_beetween('in', text, output='String')
        if duration is "":
            core.say('Ich habe nicht verstanden, wie lange der Timer dauern soll. Bitte versuche es erneut!')
            return

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
                try:
                    #erst einmal checken, ob der Timer vlt eigentlich schon abgelaufen ist, was eigentlich nicht passieren sollte.
                    now = datetime.datetime.now()
                    timer_abgelaufen = (now - item["Zeit"])
                    if timer_abgelaufen:
                        user_timer.remove(item)
                        core.local_storage["Timer"].remove(item)
                except:
                    # local_storage doesn´t extend this timer. Just write this into the Log
                    core.core.Log.write("WARNING", 'Not existing timer could not be deleted')

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
        if 'Timer' in core.local_storage.keys() and not core.local_storage["Timer"] is None and not core.local_storage["Timer"] == []:
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
                        text += temp_string
                    text += "Bitte schreib nur die Ziffer des Timers, welcher gelöscht werden soll."
                    core.say(text, output='messenger') #Der output ist eigentlich unnötig, aber wir gehen auf nummer sicher
                    number = core.listen()
                    if number <= len(user_timer):
                        core.local_storage["Timer"].remove(user_timer[int(number)-1])
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
                core.say('Alles klar. Die alte Stoppuhr wurde bei {} gestoppt und eine neue gestartet.'.format(skills.get_time(core.local_storage['stoppuhr']), get_time_differenz(core.local_storage['stoppuhr'], skills)))
                core.local_storage['stoppuhr'] = datetime.datetime.now()
            else:
                core.say('Alles klar, die alte Stoppuhr läuft weiter.')
        else:
            core.say('Alles klar, die Stoppuhr wurde um {} gestartet.'.format(skills.get_time(datetime.datetime.now())))
            core.local_storage['stoppuhr'] = datetime.datetime.now()

    elif 'stopp' in text or 'beende' in text:

        if 'stoppuhr' in core.local_storage.keys() and core.local_storage['stoppuhr'] != '':
            core.say('Alles klar, die Stoppuhr wurde um {} gestoppt. Sie dauerte {}.'.format(skills.get_time(datetime.datetime.now()), get_time_differenz(core.local_storage["stoppuhr"], skills)))
            core.local_storage['stoppuhr'] = ''
        else:
            core.say('Es wurde noch keine Stoppuhr gestartet. Soll ich eine starten?')
            response = core.listen()
            if 'ja' in response:
                core.say('Alles klar, Stoppuhr wurde um {} gestartet'.format(
                    skills.get_time(datetime.datetime.now())))
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





