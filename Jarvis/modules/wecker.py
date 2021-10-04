import datetime
import traceback


def isValid(text):
    text = text.lower()
    if 'weck' in text:
        return True
    return False


def handle(text, core, skills):
    alarm = Alarm(core)

    """
            if core.analysis["time"] is None:
            if not (' um ' in text or ' in ' in text):
                response_time = core.listen(text='Um wie viel Uhr möchtest du geweckt werden?')
            else:
                response_time = core.listen(text='Bitte wiederhole, wann du geweckt werden möchtest.')
        else:
            response_time = text
    """

    if 'abends' not in text or 'abend' not in text or not ('spät' in text and 'Stunde' in text) \
            or not ('in' in text and ('stunde' in text or 'minute' in text)):
        # Alarm clocks are usually set for the morning. Since there are otherwise problems with analyze, the morning is
        # automatically assumed here if evening is not explicitly meant.
        text += ' morgens'

    repeat = get_repeat(text)
    time = core.analysis["time"]
    days = get_day(text, skills, core.analysis["datetime"])

    if 'lösch' in text or 'beend' in text or ('schalt' in text and 'ab' in text):
        try:
            alarm.delete_alarm(days, repeat, time=time)
        except ValueError:
            core.say("Es gab einen fatalen internen Error in dem Modul Wecker. Am besten du meldest den Fehler, "
                     "damit das Modul so schnell wie möglich wieder funktionsfähig ist.")
        except:
            core.say("Leider habe ich nicht verstanden welchen Wecker ich löschen soll. Bitte versuche es "
                     "über das online-Portal oder über einen erneuten Sprachbefehl mit Zeitangabe erneut.")
    else:
        # days, repeat, time=None, hour=None, minute=None, text=None, sound=None
        alarm.create_alarm(days, repeat, time=time)
        core.say(alarm.get_reply(text, time, repeat))


def get_repeat(text):
    text = text.lower()
    if ('jeden' in text or 'immer' in text) and not ('nur am' in text or 'nur an dem' in text):
        return 'regular'
    else:
        return 'single'


def get_day(text, skills, time):
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
        days.append(skills.Statics.weekdays_engl[time.weekday()].lower())
    return days


def get_time_stamp(hour, minute):
    hour = str(hour)
    minute = str(minute)

    if len(hour) == 1:
        hour = '0' + hour
    if len(minute) == 1:
        minute = '0' + minute

    return f'{hour}:{minute}Uhr'


class Alarm:
    def __init__(self, core):
        self.core = core
        self.local_storage = core.local_storage
        self.skills = core.skills
        self.create_alarm_storage()

        self.user = None
        self.days = None
        self.repeat = None
        self.text = None
        self.list = None

    def create_alarm(self, days, repeat, time=None, hour=None, minute=None, seconds=0, text=None, sound=None):
        # toDo: dont add alarm when exists
        if not (time is not None or (hour is not None and minute is not None)):
            raise ValueError("missing values!")
        if repeat != "regular" and repeat != "single":
            raise ValueError("invlaid repeat-value!")
        if time is not None:
            hour = time["hour"]
            minute = time["minute"]
            seconds = time["second"]
        if self.core.user is not None:
            alarm_sound = self.core.user["alarm_sound"]
            user = self.core.user
            user_name = f', {self.core.user["first_name"].capitalize()}'
        else:
            alarm_sound = "standard.wav"
            user = None
            user_name = ''
        if text is None:
            text = f'Alles Gute zum Geburtstag{user_name}!' if self.is_birthday() else f'Guten Morgen{user_name}!'
        if sound is not None:
            alarm_sound = sound

        total_seconds = int(hour) * 3600 + int(minute) * 60
        list = {"time": {"hour": hour, "minute": minute,
                         "total_seconds": total_seconds, "time_stamp": get_time_stamp(hour, minute)},
                "sound": alarm_sound, "user": user,
                "text": text, "active": True}
        if not type(days) == type([]):
            days = [days]
        for _day in days:
            if self.core.local_storage["alarm"][repeat][_day] is None or _day not in self.core.local_storage["alarm"]["regular"].keys():
                self.core.local_storage["alarm"][repeat][_day] = []
            self.core.local_storage["alarm"][repeat][_day].append(list)

    def delete_alarm(self, days, repeat, time=None, hour=None, minute=None):
        if not (time is not None or (hour is not None and minute is not None)):
            raise ValueError("missing values!")
        if repeat != "regular" and repeat != "single":
            raise ValueError("invlaid repeat-value!")
        if time is not None:
            hour = time.hour
            minute = time.minute
        # repeat means "regular" or "single"
        if not type(days) == type([]):
            days = [days]
        for item in days:
            try:
                for alarm in self.core.local_storage["alarm"][repeat][item]:
                    # check every alarm
                    if hour == alarm["time"]["hour"] and minute == alarm["time"]["minute"]:
                        # if hour and minute matches, remove it
                        self.core.local_storage["alarm"][repeat][item].remove(alarm)
            except:
                traceback.print_exc()

    def is_birthday(self):
        if self.core.user:
            birth_date = self.core.user["date_of_birth"]
            today = datetime.datetime.today()
            if birth_date["month"] == today.month and birth_date["day"] == today.day:
                return True
        return False

    def get_reply(self, text, time, repeat):

        output = 'Wecker gestellt '

        now = datetime.datetime.now()
        if repeat == 'single':
            if time["day"] == now.day:
                output += 'für heute'
            elif time["day"] == (now.day+1):
                output += 'für morgen'
            else:
                output += 'am ' + time["day"] + '.' + time["month"]
        else:
            output += 'für jeden '

            for item in self.skills.Statics.weekdays:
                if item.lower() in text.lower():
                    output += item
                    break

        output += ' um ' + self.skills.get_time(time)
        return output

    def create_alarm_storage(self):
        if 'alarm' not in self.core.local_storage.keys():
            self.core.local_storage["alarm"] = {}

        if 'regular' not in self.core.local_storage["alarm"].keys():
            self.core.local_storage["alarm"]["regular"] = {}

        if 'single' not in self.core.local_storage["alarm"].keys():
            self.core.local_storage["alarm"]["single"] = {}

        for extension in ['regular', 'single']:
            for day in [each_day.lower() for each_day in self.skills.Statics.weekdays_engl]:
                if day not in self.core.local_storage["alarm"][extension].keys():
                    self.core.local_storage["alarm"][extension][day] = []

    def confirm_action(self, days):
        repeatings = 'Regelmäßiger ' if self.repeat == 'regular' else ''
        day_names = []
        for item in days:
            day_names.append(self.skills.Statics.weekdays_eng_to_ger[item])

        day_enum = self.skills.get_enumerate(day_names)
        if len(days) > 1:
            self.core.say(f'{repeatings}Wecker gestellt für{day_enum} um {self.skills.get_time(self.time)}')
        else:
            self.core.say(
                f'{repeatings}Wecker gestellt für{self.get_reply()}, {self.time["hour"]} Uhr {self.time["minute"]}')
