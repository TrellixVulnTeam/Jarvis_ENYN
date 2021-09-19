from time import sleep


def isValid(text):
    text = text.lower()
    if 'erinner' in text or 'erinnere' in text:
        return True
    else:
        return False


def get_text(core, text):
    remembrall = ''
    e_ind = 0
    text = text.lower()

    if ' zu ' not in text:
        remembrall = text.replace('zu', (''))
        remembrall = remembrall.replace(' ans ', (' '))
    else:
        remembrall = text.replace(' ans ', (' '))
    if ' in ' in text and ' minuten' in text:
        remembrall = remembrall.replace(' minuten ', (' '))
        remembrall = remembrall.replace(' in ', (' '))
        s = str.split(remembrall)
        for t in s:
            try:
                if int(t) >= 0:
                    remembrall = remembrall.replace(t, (''))
            except ValueError:
                remembrall = remembrall
    satz = {}
    ausgabe = ''
    ind = 1
    i = str.split(remembrall)
    for w in i:
        satz[ind] = w
        ind += 1
    if ' am ' in satz.items():
        for index, word in satz.items():
            if word == 'am':
                am_ind = index
                try:
                    if int(satz.get(am_ind + 2)):
                        summand = 3
                        for i, w in satz.items():
                            try:
                                ausgabe = ausgabe + satz.get(am_ind + summand) + ' '
                                summand += 1
                            except TypeError:
                                ausgabe = ausgabe
                except (ValueError, TypeError):
                    summand = 2
                    for i, w in satz.items():
                        try:
                            ausgabe = ausgabe + satz.get(am_ind + summand) + ' '
                            summand += 1
                        except TypeError:
                            ausgabe = ausgabe
    elif ' daran dass' in text:
        for ind, w in satz.items():
            if w == 'daran':
                reminder = ''
                n = 1
                try:
                    try:
                        while n < 30:
                            if satz.get(ind + n) != None:
                                reminder = reminder + str(satz.get(ind + n)) + ' '
                                n += 1
                            else:
                                reminder = reminder
                                break
                    except KeyError:
                        reminder = reminder
                        break
                except ValueError:
                    reminder = reminder
                    break
                ausgabe = reminder
    else:
        for index, word in satz.items():
            if word == 'erinner' or word == 'erinnere':
                e_ind = index
                s_ind = e_ind + 2
                ausgabe = satz.get(s_ind) + ' '
                summand = 1
                for i, w in satz.items():
                    try:
                        ausgabe = ausgabe + satz.get(s_ind + summand) + ' '
                        summand += 1
                    except TypeError:
                        ausgabe = ausgabe
    ausgabe = ausgabe.replace('übermorgen ', (' '))
    ausgabe = ausgabe.replace('morgen ', (' '))
    ausgabe = ausgabe.replace('daran ', (' '))
    ausgabe = ausgabe.replace('ich', ('du'))
    ausgabe = ausgabe.replace('mich', ('dich'))
    if 'dass ' in text:
        lang = len(ausgabe)
        if ausgabe[(lang - 1):] == ' ':
            ausgabe = ausgabe[:(lang - 1)]
        l = len(ausgabe)
        if ausgabe[(l - 2):] == 'st':
            ausgabe = ausgabe
        elif ausgabe[(l - 1):] == 's':
            ausgabe = ausgabe + 't'
        else:
            ausgabe = ausgabe + 'st'
    return ausgabe


def get_reply_time(core, dicanalyse):
    time = dicanalyse.get('time')
    jahr = str(time['year'])
    monat = str(time['month'])
    tag = str(time['day'])
    stunde = str(time['hour'])
    minute = str(time['minute'])
    if int(minute) <= 9:
        minute = '0' + minute
    if int(monat) <= 9:
        monat = '0' + monat

    if minute[0] == '0':
        mine = minute[1]
        if mine == '0':
            mine = ''
        else:
            mine = mine
    else:
        mine = minute
    day = core.skills.Statics.numb_to_day_numb.get(tag)
    month = core.skills.Statics.numb_to_month.get(str(monat))
    hour = core.skills.Statics.numb_to_hour.get(str(stunde))
    zeit_der_erinnerung = str(day) + ' ' + str(month) + ' um ' + str(hour) + ' Uhr ' + str(mine)
    reply = zeit_der_erinnerung
    return reply


def handle(text, core, skills):
    if 'lösch' in text:
        time = core.analyze['time']
        erinnerungen = core.local_storage['Erinnerungen']
        founded = []
        for item in erinnerungen:
            if item['Zeit'] is time:
                founded.append(item)
        if len(founded) is 0:
            core.say(
                'Ich habe leider keine Erinnerung zu dieser Zeit gefunden. Ich werde mal nach deinen Einträgen gucken.')
            sleep(2)
            entries = []
            for item in erinnerungen:
                if item['Benutzer'] is core.user:
                    entries.append(item)
                core.say(
                    'Ich habe folgendes herausgefunden: du hast {} Erinnerungseinträge. Soll ich sie dir Vorlesen und '
                    'du sagst, wenn es das richtige ist?'.format(str(len(entries))))
                answer = core.listen()
                if 'ja' in answer:
                    for item in entries:
                        core.say(
                            'Okay, ich werde dir einfach die Einträge vorlesen und nach jedem Eintrag sagst du entweder ja oder nein.')
                        hit = False
                        for item in entries:
                            if not hit:
                                core.say(item['Text'] + ' Ist das richtig?')
                                response = core.listen()
                                if 'ja' in response:
                                    founded = True
                                    erinnerungen.remove(item)
                                    core.local_storage['Erinnerungen'] = erinnerungen
                else:
                    core.say('Okay, vielleicht probierst du es erneut.')
        if len(founded) > 1:
            core.say('Zu dieser Zeit gibt es mehrere Erinnerungen. Soll ich alle löschen?')
            response = core.listen()
            if 'ja' in response:
                core.say('Alles klar, ich werde alle Einträge zu diesem Zeitpunkt löschen.')
                for item in founded:
                    erinnerungen.remove(item)
                core.local_storage['Erinnerungen'] = erinnerungen
            else:
                core.say('Soll ich dir jeden Eintrag vorlesen und du sagst mir, ob es der richtige war oder nicht?')
                response = core.listen()
                if 'ja' in response:
                    core.say(
                        'Okay, ich werde dir einfach die Einträge vorlesen und nach jedem Eintrag sagst du entweder ja oder nein.')
                    for item in founded:
                        core.say(response['Text'] + ' Ist das richt?')
                        response = core.listen()
                        if 'ja' in response:
                            erinnerungen.remove(item)
                            core.local_storage['Erinnerungen'] = erinnerungen
                else:
                    core.say('Alles klar, dann probiere es vielleicht nocheinmal.')

    elif text != '_UNDO_':
        reply = ''
        Erinnerung = {}
        r = get_text(core, text)
        E_eins = {'Zeit': core.analysis['datetime'], 'Text': r, 'Benutzer': core.user}
        if 'Erinnerungen' in core.local_storage.keys():
            core.local_storage['Erinnerungen'].append(E_eins)
        else:
            core.local_storage['Erinnerungen'] = [E_eins]
        rep = get_reply_time(core, core.analysis)
        if 'dass ' in r:
            antwort = 'Alles klar, ich sage dir am ' + rep + ' bescheid, ' + r + '.'  ###
        elif 'ans ' in text:
            antwort = 'Alles klar, ich erinnere dich am ' + rep + ' ans ' + r + '.'
        else:
            antwort = 'Alles klar, ich sage dir am ' + rep + ' bescheid, dass du ' + r + ' musst.'
        core.say(antwort)
    else:
        liste = core.local_storage.get('Erinnerungen')
        element = liste[len(liste)]
        if element.get('Benutzer') == core.user:
            del liste[len(liste)]
        else:
            element = liste[len(liste) - 1]
            if element.get('Benutzer') == core.user:
                del liste[len(liste) - 1]
            else:
                element = liste[len(liste) - 2]
                if element.get('Benutzer') == core.user:
                    del liste[len(liste) - 2]
                else:
                    del liste[len(liste) - 3]
