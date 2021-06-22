import datetime


def isValid(text):
    text = text.lower()
    if 'weck' in text:
        return True
    return False


def handle(text, core, skills):
    alarm = Alarm(core, skills, core.analysis["time"], get_day(core, text, skills), get_repeat(text))

    """
            if core.analysis["time"] is None:
            if not (' um ' in text or ' in ' in text):
                response_time = core.listen(text='Um wie viel Uhr möchtest du geweckt werden?')
            else:
                response_time = core.listen(text='Bitte wiederhole, wann du geweckt werden möchtest.')
        else:
            response_time = text
    """

    if 'lösch' in text or 'beend' in text or ('schalt' in text and 'ab' in text):
        alarm.delete_alarm()
    else:
        alarm.create_alarm()


def get_repeat(text):
    text = text.lower()
    if ('jeden' in text or 'immer' in text) and not ('nur am' in text or 'nur an dem' in text):
        return 'regular'
    else:
        return 'single'


def get_day(core, text, skills):
    text = text.lower()
    days = []

    if 'täglich' in text or 'jeden tag' in text or 'alle' in text or 'jeden morgen' in text or 'jeden abend' in text:
        days = [each_day.lower() for each_day in skills.Statics.weekdays_engl]
    elif 'wochentag' in text or 'unter der woche' in text:
        for i in range(5):
            days.append(skills.Statics.weekdays_engl[i].lower())
    elif 'wochenende' in text:
        days = ['saturday', 'sunday']
    else:
        for item in skills.Statics.weekdays:
            if item.lower() in text:
                days.append(skills.Statics.weekdays_ger_to_eng[item.lower()])

    if days == []:
        days = [datetime.datetime.today().strftime("%A").lower()]
    return days


class Alarm:
    def __init__(self, core, skills, time, days, repeat):
        self.core = core
        self.local_storage = core.local_storage
        self.skills = skills
        self.create_alarm_storage()

        self.time = time
        self.user = core.user
        self.days = days
        self.repeat = repeat

        user_name = ' ' if self.user is None else f', {self.user["first_name"].capitalize()}'
        self.text = f'Alles Gute zum Geburtstag{user_name}!' if self.is_birthday() else f'Guten Morgen{user_name}!'
        total_seconds = self.time["hour"] * 3600 + self.time["minute"] * 60 + self.time["second"]
        self.list = {"time": {"hour": self.time["hour"], "minute": self.time["minute"], "second": self.time["second"],
                              "total_seconds": total_seconds},
                     "sound": self.user["alarm_sound"], "user": self.user["name"],
                     "text": self.text, "active": True}

    def create_alarm(self):
        # toDo: dont add alarm when exists
        if not type(self.days) == type([]):
            self.days = [self.days]

        for _day in self.days:
            if self.core.local_storage["alarm"][self.repeat][_day] is None or not _day in \
                                                                                  self.core.local_storage["alarm"][
                                                                                      "regular"].keys():
                self.core.local_storage["alarm"][self.repeat][_day] = []
            self.core.local_storage["alarm"][self.repeat][_day].append(self.list)
        self.confirm_action()

    def delete_alarm(self):
        # repeat means "regular" or "single"
        if not type(self.days) == type([]):
            self.days = [self.days]
        for item in self.days:
            try:
                for alarm in self.core.local_storage["alarm"][self.repeat][item]:
                    # check every alarm
                    if self.time.hour == alarm["time"]["hour"] and self.time.minute == alarm["time"]["minute"]:
                        # if hour and minute matches, remove it
                        self.core.local_storage["alarm"][self.repeat].remove(alarm)
            except:
                self.core.say("Leider habe ich nicht verstanden welchen Wecker ich löschen soll. Bitte versuche es "
                              "über das online-Portal oder über einen erneuten Sprachbefehl mit Zeitangabe erneut.")

    def is_birthday(self):
        if self.core.user:
            birth_date = self.core.user["date_of_birth"]
            today = datetime.datetime.today()
            if birth_date["month"] == today.month and birth_date["day"] == today.day:
                return True
        return False

    def get_reply(self):
        # toDo: Mehrere Tage
        now = datetime.datetime.today().day
        monat = str(self.time["month"])
        tag = str(self.time["day"])
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
            return 'den ' + self.core.correct_output(core_output, messenger_output)

    def create_alarm_storage(self):
        if not 'alarm' in self.core.local_storage.keys():
            self.core.local_storage["alarm"] = {}

        if not 'regular' in self.core.local_storage["alarm"].keys():
            self.core.local_storage["alarm"]["regular"] = {}

        if not 'single' in self.core.local_storage["alarm"].keys():
            self.core.local_storage["alarm"]["single"] = {}

        for extension in ['regular', 'single']:
            for day in [each_day.lower() for each_day in self.skills.Statics.weekdays_engl]:
                if not day in self.core.local_storage["alarm"][extension].keys():
                    self.core.local_storage["alarm"][extension][day] = []

    def confirm_action(self):
        repeatings = 'Regelmäßiger ' if self.repeat == 'regular' else ' '
        day_names = []
        for item in self.days:
            day_names.append(self.skills.Statics.weekdays_eng_to_ger[item])

        day_enum = self.skills.get_enumerate(day_names)
        if len(self.days) > 1:
            self.core.say(f'{repeatings}Wecker gestellt für{day_enum} um {self.skills.get_time(self.time)}')
        else:
            self.core.say(
                f'{repeatings}Wecker gestellt für{self.get_reply()}, {self.time["hour"]} Uhr {self.time["minute"]}')
