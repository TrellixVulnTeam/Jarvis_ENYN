import datetime

def isValid(text):
    if 'wecker' in text:
        return True
    return False


def handle(text, core, skills):
    if 'stell' in text:
        while core.analysis["time"] is None:
            if not (' um ' in text or ' in ' in text):
                response_time = core.listen(text='Um wie viel Uhr möchtest du geweckt werden?')
            else:
                response_time = core.listen(text='Bitte wiederhole, wann du geweckt werden möchtest.')
        else:
            response_time = text
    time = core.analyze(response_time)
    sound = core.user.get('wecker_ton')
    birthday_text = f'Alles gute zum Geburtstag, {core.user}. Ich wünsche dir einen super Tag! '
    text = birthday_text if is_birthday(core, time) else f'Guten morgen {core.user}!'

class Alarm:
    def __init__(self, core, skills, time):
        self.core = core
        self.local_storage = core.local_storage
        self.skills = skills
        self.time = time
        self.user = core.user

    def daily():
        for

    def regular_day(self, day):


    def is_birthday(self):
        return False


    def get_reply(self):
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
