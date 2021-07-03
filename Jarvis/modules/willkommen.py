import datetime


def isValid(text):
    text = text.lower()
    if (text.startswith(
            'hallo') or text == 'hi' or text == 'hey' or text == '/start') and not 'geht' in text or 'läuft' in text:
        return True
    elif 'gute' in text and ('tag' in text or 'morgen' in text or 'abend' in text or 'nacht' in text):
        return True
    return False


def handle(text, core, skills):
    text = text.lower()
    now = datetime.datetime.now()
    time = now.hour
    if 'hallo' in text:
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
            core.say('Wurde aber auch langsam Zeit. Aber auch dir einen guten Morgen.')
        elif 14 <= time <= 18:
            core.say(
                'Ob es noch Morgen ist, liegt wohl im Blickwinkel des Betrachters. Ich würde eher sagen, '
                'dass es Mittag oder Nachmittag ist.')
        elif time >= 19 or time <= 3:
            core.say(
                'Also Morgen ist es auf jeden Fall nicht mehr. Daher wünsche ich dir einfach Mal einen guten Abend.')
        else:
            core.say('Hallo!')

    elif 'guten' in text and 'abend' in text:
        if 6 <= time <= 17:
            core.say(
                'Ob es Abend ist, liegt wohl im Blickwinkel des Betrachters. In Amerika ist es jetzt in der Tat Abend.')
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
        if skills.is_desired(response):
            if core.analysis['datetime'] is None:
                core.say('Wann soll ich dich denn wecken?')
                response_two = core.listen()
                text = 'weck ' + response_two
                core.start_module(text=text)
            else:
                core.start_module(text=text)
        else:
            core.say('Okay.')
