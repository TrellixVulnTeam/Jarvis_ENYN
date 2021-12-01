import os
import pkgutil
import random
import time
import traceback
from threading import Thread
import io
import json
import logging
import urllib
from Jarvis.resources.analyze import Sentence_Analyzer as Analyzer
from urllib.request import Request, urlopen
from Wrapper import IntentWrapper

logging.disable(logging.INFO)
# toDO: smalltalk, spacex, transkribieren
class Core:
    def __init__(self):
        self.messenger = False
        self.system_name = "TESTSYSTEM"
        self.path = "C:\\Users\\Jakob\\OneDrive\\Jarvis\\Jarvis"
        self.active_modules = {}
        self.config_data = {"correct_output": []}
        self.analyzer = Analyzer()
        self.skills = skills()
        self.local_storage = {}
        self.Audio_Output = Audio_Output()
        self.Audio_Input = Audio_Input()
        self.modules = Modules(self, self.local_storage)

    def start_module(self, text, name):
        print(f"Starting module '{name}' with text '{text}'")
        self.modules.start_module(None, text, name, False)


class Modules:
    def __init__(self, core, local_storage):
        logging.getLogger().setLevel(logging.INFO)
        self.core = core
        self.local_storage = local_storage
        self.modules = []
        self.continuous_modules = []

        self.module_wrapper = Modulewrapper

        self.continuous_stopped = False
        self.continuous_threads_running = 0

        self.load_modules()

    def load_modules(self):
        self.local_storage["modules"] = {}
        time.sleep(1)
        print('---------- MODULES...  ----------')
        self.modules = self.get_modules('modules')
        if self.modules is []:
            print('[INFO] -- (None present)')

    def get_modules(self, directory, continuous=False):
        dirname = os.path.abspath("C:\\Users\\Jakob\\PycharmProjects\\Jarvis\\Jarvis")
        locations = [os.path.join(dirname, directory)]
        modules = []
        if "modules" not in self.local_storage:
            self.local_storage["modules"] = {}
        for finder, name, ispkg in pkgutil.walk_packages(locations):
            try:
                loader = finder.find_module(name)
                mod = loader.load_module(name)
                self.local_storage["modules"][name] = {"name": name, "status": "loaded"}
            except:
                traceback.print_exc()
                self.local_storage["modules"][name] = {"name": name, "status": "error"}
                print('[WARNING] Modul {} is incorrect and was skipped!'.format(name))
                continue
            else:
                if continuous:
                    print('[INFO] Continuous module {} loaded'.format(name))
                    modules.append(mod)
                else:
                    print('[INFO] Modul {} loaded'.format(name))
                    modules.append(mod)
        modules.sort(key=lambda mod: mod.PRIORITY if hasattr(mod, 'PRIORITY') else 0, reverse=True)
        return modules

    def query_threaded(self, name, text, user, messenger=False):
        mod_skill = self.core.skills
        if text is None:
            # generate a random text
            text = random.randint(0, 1000000000)
            analysis = {}
        else:
            # else there is a valid text -> analyze
            try:
                analysis = self.core.analyzer.analyze(str(text))
            except:
                traceback.print_exc()
                print('[ERROR] Sentence analysis failed!')
                analysis = {}
        if name is not None:
            # Module was called via start_module
            for module in self.modules:
                if module.__name__ == name:
                    self.core.active_modules[str(text)] = self.module_wrapper(self.core, text, analysis, messenger,
                                                                              user)
                    mt = Thread(target=self.run_threaded_module, args=(text, module, mod_skill))
                    mt.daemon = True
                    mt.start()
                    return True
            print('[ERROR] Modul {} could not be found!'.format(name))
        elif text is not None:
            # Search the modules normally
            for module in self.modules:
                try:
                    if module.isValid(str(text).lower()):
                        self.core.active_modules[str(text)] = self.module_wrapper(self.core, text, analysis, messenger,
                                                                                  user)
                        mt = Thread(target=self.run_threaded_module, args=(text, module, mod_skill))
                        mt.daemon = True
                        mt.start()
                        return True
                except:
                    traceback.print_exc()
                    print('[ERROR] Modul {} could not be queried!'.format(module.__name__))
        return False

    def start_module(self, user=None, text=None, name=None, messenger=False):
        # self.query_threaded(name, text, direct, messenger=messenger)
        mod_skill = self.core.skills
        analysis = {}
        if text is None:
            text = str(random.randint(0, 1000000000))
        else:
            try:
                analysis = self.core.analyzer.analyze(str(text))
                # logging.info('Analysis: ' + str(analysis))
            except:
                traceback.print_exc()
                logging.warning('[WARNING] Sentence analysis failed!')

        if name is not None:
            for module in self.modules:
                if module.__name__ == name:
                    logging.info('[ACTION] --Modul {} was called directly (Parameter: {})--'.format(name, text))
                    self.core.active_modules[str(text)] = self.module_wrapper(self.core, text, analysis, messenger,
                                                                              user)
                    mt = Thread(target=self.run_threaded_module, args=(text, module, mod_skill))
                    mt.daemon = True
                    mt.start()
                    break
        else:
            try:
                analysis = self.core.analyzer.analyze(str(text))
            except:
                traceback.print_exc()
                print('[ERROR] Sentence analysis failed!')
                analysis = {}
            for module in self.modules:
                try:
                    if module.isValid(text.lower()):
                        self.core.active_modules[str(text)] = self.module_wrapper(self.core, text, analysis, messenger,
                                                                                  user)
                        mt = Thread(target=self.run_threaded_module, args=(text, module, mod_skill))
                        mt.daemon = True
                        mt.start()
                        mt.join()  # wait until Module is done...
                        self.start_module(user=user, name='wartende_benachrichtigung')
                        break
                except:
                    traceback.print_exc()
                    print('[ERROR] Modul {} could not be queried!'.format(module.__name__))
        return False

    def run_threaded_module(self, text, module, mod_skill):
        try:
            module.handle(text, self.core.active_modules[str(text)], mod_skill)
        except:
            traceback.print_exc()
            print('[ERROR] Runtime error in module {}. The module was terminated.\n'.format(module.__name__))
            self.core.active_modules[str(text)].say(
                'Entschuldige, es gab ein Problem mit dem Modul {}.'.format(module.__name__))
        finally:
            try:
                del self.core.active_modules[str(text)]

            except:
                pass
            return

    def run_module(self, text, module_wrapper, mod_skill):
        for module in self.modules:
            if module.isValid(text):
                module.handle(text, module_wrapper, mod_skill)


class skills:
    def __init__(self):
        pass

    @staticmethod
    def get_enumerate(array):
        # print(array)
        new_array = []  # array=['Apfel', 'Birne', 'Gemüse', 'wiederlich']
        for item in array:
            new_array.append(item.strip(' '))

        # print(new_array)
        ausgabe = ''
        # print('Länge: {}'.format(len(new_array)))
        if len(new_array) == 0:
            pass
        elif len(new_array) == 1:
            ausgabe = array[0]
        else:
            for item in range(len(new_array) - 1):
                ausgabe += new_array[item] + ', '
            ausgabe = ausgabe.rsplit(', ', 1)[0]
            ausgabe = ausgabe + ' und ' + new_array[-1]
        return ausgabe

    @staticmethod
    def is_approved(text):
        if ('ja' in text or 'gerne' in text or 'bitte' in text) and not (
                'nein' in text or 'nicht' in text or 'nö' in text or 'ne' in text):
            return True
        else:
            return False

    @staticmethod
    def get_text_beetween(start_word, text, end_word='', output='array', split_text=True):
        ausgabe = []
        index = -1
        start_word = start_word.lower()
        text = text.replace(".", "")
        if split_text:
            text = text.split(' ')
            for i in range(len(text)-1):
                # toDo: Maybe check if text[i].lower == start_word or this option
                # First here .lower to keep upper and lower case
                if text[i].lower() in start_word:
                    index = i + 1

        if index is not -1:
            if end_word == '':
                for i in range(index, len(text)):
                    ausgabe.append(text[i])
            else:
                founded = False
                while index <= len(text) and not founded:
                    if text[index] is end_word:
                        founded = True
                    else:
                        ausgabe.append(text[index])
                        index += 1
        if output is 'array':
            return ausgabe
        elif output is 'String':
            ausgabe_neu = ''
            for item in ausgabe:
                ausgabe_neu += item + ' '
            return ausgabe_neu

    @staticmethod
    def delete_duplications(array):
        return list(set(array))

    def assamble_new_items(self, array1, array2):
        new_array = []
        for item in array1:
            value1, number1 = self.get_value_number(item)
            try:
                item1 = item.split(" ", 1)[1].lower()
            except:
                item1 = item.lower()
            for field in array2:
                value2, number2 = self.get_value_number(field)
                try:
                    item2 = field.split(" ", 1)[1].lower()
                except:
                    item2 = field.lower()
                # print(f"value1: {item1}, {number1}, {value1};    value2: {item2}, {number2}, {value2}")
                if item1 == item2 or item1.rstrip(item1[-1]) == item2 or item1 == item2.rstrip(item2[-1]):
                    if item1[-1] == "e":
                        item1 += "n"
                    if value1 == value2:
                        final_value = value1
                        final_number = number1 + number2
                        if final_number >= 1000 and final_value == "g":
                            final_value = "kg"
                            final_number /= 1000
                    else:
                        final_value = ""
                        final_number = -1
                    if final_number != -1:
                        new_array.append(str(final_number) + final_value + " " + item1.capitalize())
                    else:
                        new_array.append(item1.capitalize())
                else:
                    if self.is_enthalten(item1, array2):
                        new_array.append(item1.capitalize())
                    if self.is_enthalten(item2, array1):
                        new_array.append(item2.capitalize())

        return self.delete_duplications(new_array)

    @staticmethod
    def is_enthalten(item, array):
        item = item.lower()
        valid = True
        for position in array:
            try:
                item_position = position.split(" ", 1)[1].lower()
            except:
                item_position = position.lower()
            if item_position == item or item_position.rstrip(item_position[-1]) == item or item_position == item.rstrip(
                    item[-1]):
                valid = False
        return valid

    @staticmethod
    def get_value_number(item):
        first_value = item.split(' ', 1)[0]
        value = ""
        number = -1
        if "kg" in first_value:
            try:
                first_value.replace("kg", "")
                value = "g"
                number = int(first_value) * 1000
            except:
                pass
        elif "g" in first_value:
            try:
                first_value1 = first_value.replace("g", "")
                value = "g"
                number = int(first_value1)
            except:
                pass
        elif "ml" in first_value:
            try:
                first_value = first_value.replace("ml", "")
                value = "ml"
                number = int(first_value)
            except:
                pass
        else:
            try:
                number = int(first_value)
            except:
                pass
        return value, number

    def assamble_array(self, array):
        # print(f"Beim Start von assamble_array: {array}")
        temp_array = []
        temp_array0 = array
        for item in temp_array0:
            item = item.replace('1', '')
            item = item.replace('2', '')
            item = item.replace('3', '')
            item = item.replace('4', '')
            item = item.replace('5', '')
            item = item.replace('6', '')
            item = item.replace('7', '')
            item = item.replace('8', '')
            item = item.replace('9', '')
            item = item.replace('0', '')
            item = item.strip()
            temp_array.append(item)
        duplications = self.delete_duplications(temp_array)
        temp3_array = []
        if len(duplications) >= 1:
            temp2_array = self.assamble_new_items(array, duplications)
            for item in temp2_array:
                try:
                    anz = int(item.split(' ', 1)[0])
                except:
                    anz = 1
                anz -= 1

                if anz == 1:
                    item = item.split(' ')[1]
                else:
                    item = str(anz) + " " + item.split(' ', 1)[1]
                temp3_array.append(item)

        return temp3_array

    @staticmethod
    def get_time(i):
        try:
            hour = i["hour"]
        except:
            hour = i.hour
        try:
            minute = i["minute"]
        except:
            minute = i.minute
        next_hour = hour + 1
        if next_hour == 24:
            next_hour = 0
        hour = str(hour) if hour > 9 else '0' + str(hour)
        minute = str(minute) if minute > 9 else '0' + str(minute)
        if minute == 0:
            output = hour + ' Uhr.'
        elif minute == 5:
            output = 'fünf nach ' + hour
        elif minute == 10:
            output = 'zehn nach ' + hour
        elif minute == 15:
            output = 'viertel nach ' + hour
        elif minute == 20:
            output = 'zwanzig nach ' + hour
        elif minute == 25:
            output = 'fünf vor halb ' + hour
        elif minute == 30:
            output = 'halb ' + next_hour
        elif minute == 35:
            output = 'fünf nach halb ' + next_hour
        elif minute == 40:
            output = 'zwanzig vor ' + next_hour
        elif minute == 45:
            output = 'viertel vor ' + next_hour
        elif minute == 50:
            output = 'zehn vor ' + next_hour
        elif minute == 55:
            output = 'fünf vor ' + next_hour
        else:
            output = hour + ':' + minute + ' Uhr'
        return output

    def get_time_differenz(self, start_time, time=None):
        aussage = []
        if time is None:
            dz = start_time
        else:
            dz = time - start_time
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
        return self.get_enumerate(aussage)

    @staticmethod
    def get_word_index(text, word):
        text = text.split(' ')
        for i in range(len(text)):
            if text[i] == word:
                return i
        return -1


    @staticmethod
    def is_desired(text):
        # returns True, if user want this option
        text = text.lower()
        if 'ja' in text or 'gern' in text or ('bitte' in text and 'nicht' not in text):
            return True
        elif 'bitte' in text and 'nicht' not in text:
            return True
        elif 'danke' in text and 'nein' not in text:
            return True
        return False

    class Statics:
        def __init__(self):
            pass

        # Colors
        color_ger_to_eng = {
            "schwarz": "black",
            "blau": "blue",
            "rot": "red",
            "gelb": "yellow",
            "grün": "green"
        }

        color_eng_to_ger = {
            "black": "schwarz",
            "blue": "blau",
            "red": "rot",
            "yellow": "gelb",
            "green": "grün"
        }

        # Weekdays
        weekdays = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
        weekdays_engl = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        weekdays_ger_to_eng = {
            'montag': 'monday',
            'dienstag': 'tuesday',
            'mittwoch': 'wednesday',
            'donnerstag': 'thursday',
            'freitag': 'friday',
            'samstag': 'saturday',
            'sonntag': 'sunday'
        }

        weekdays_eng_to_ger = {
            'monday': 'montag',
            'tuesday': 'dienstag',
            'wednesday': 'mittwoch',
            'thursday': 'donnerstag',
            'friday': 'freitag',
            'saturday': 'samstag',
            'sunday': 'sonntag'
        }

        numb_to_day = {
            "1": "monday",
            "2": "tuesday",
            "3": "wednesday",
            "4": "thursday",
            "5": "friday",
            "6": "saturday",
            "7": "sunday"}

        numb_to_day_numb = {'01': 'ersten', '02': 'zweiten', '03': 'dritten', '04': 'vierten', '05': 'fünften',
                            '06': 'sechsten', '07': 'siebten', '08': 'achten', '09': 'neunten', '10': 'zehnten',
                            '11': 'elften', '12': 'zwölften', '13': 'dreizehnten', '14': 'vierzehnten',
                            '15': 'fünfzehnten',
                            '16': 'sechzehnten', '17': 'siebzehnten', '18': 'achtzehnten', '19': 'neunzehnten',
                            '20': 'zwanzigsten',
                            '21': 'einundzwanzigsten', '22': 'zweiundzwanzigsten', '23': 'dreiundzwanzigsten',
                            '24': 'vierundzwanzigsten',
                            '25': 'fünfundzwanzigsten', '26': 'sechsundzwanzigsten', '27': 'siebenundzwanzigsten',
                            '28': 'achtundzwanzigsten',
                            '29': 'neunundzwanzigsten', '30': 'dreißigsten', '31': 'einunddreißigsten',
                            '32': 'zweiunddreißigsten'}

        numb_to_hour = {'01': 'ein', '02': 'zwei', '03': 'drei', '04': 'vier', '05': 'fünf', '06': 'sechs',
                        '07': 'sieben', '08': 'acht', '09': 'neun', '10': 'zehn', '11': 'elf', '12': 'zwölf',
                        '13': 'dreizehn', '14': 'vierzehn', '15': 'fünfzehn', '16': 'sechzehn', '17': 'siebzehn',
                        '18': 'achtzehn', '19': 'neunzehn', '20': 'zwanzig', '21': 'einundzwanzig',
                        '22': 'zweiundzwanzig',
                        '23': 'dreiundzwanzig', '24': 'vierundzwanzig'}

        numb_to_month = {'01': 'Januar', '02': 'Februar', '03': 'März', '04': 'April', '05': 'Mai', '06': 'Juni',
                         '07': 'Juli', '08': 'August', '09': 'September', '10': 'Oktober', '11': 'November',
                         '12': 'Dezember'}

        numb_to_ordinal = {"1": "erster", "2": "zweiter", "3": "dritter", "4": "vierter", "5": "fünfter",
                           "6": "sechster", "7": "siebter", "8": "achter", "9": "neunter", "10": "zehnter",
                           "11": "elfter", "12": "zwölfter", "13": "dreizehnter", "14": "vierzehnter",
                           "15": "fünfzehnter", "16": "sechzehnter", "17": "siebzehnter", "18": "achtzehnter",
                           "19": "neunzehnter", "20": "zwanzigster"}


class Audio_Input:
    def __init__(self):
        pass

    def listen(self):
        return input("Listen: ")


class Audio_Output:
    def __init__(self):
        pass

    def say(self, text):
        print(f"Saying: {text}")


class Modulewrapper:
    def __init__(self, core, text, analysis, messenger, user):
        self.text = text
        self.analysis = analysis
        # toDo: down below
        # self.analysis['town'] = core.local_storage['home_location'] if self.analysis['town'] is None else None

        self.Audio_Output = core.Audio_Output
        self.Audio_Input = core.Audio_Input

        self.messenger_call = messenger

        self.room = "messenger" if messenger else "raum"
        self.messenger = core.messenger

        self.core = core
        self.skills = core.skills
        self.Analyzer = core.analyzer
        self.local_storage = core.local_storage
        self.system_name = core.system_name
        self.path = core.path
        self.user = user

    def say(self, text, output='auto'):
        text = self.speechVariation(text)
        if output == 'auto':
            if self.messenger_call:
                output = 'messenger'
        if 'messenger' in output.lower() or self.messenger_call:
            self.messenger_say(text)
        else:
            text = self.correct_output_automate(text)
            self.Audio_Output.say(text)

    def messenger_say(self, text):
        try:
            self.messenger.say(text, self.user['telegram_id'])
        except KeyError:
            logging.warning(
                '[WARNING] Sending message "{}" to messenger failed, because there is no Telegram-ID for this user '
                '({}) '.format(text, self.user["name"]))
        except AttributeError:
            logging.info('[WARNING] Sending message to messenger failed,  because there is no key for it!')
        return

    def play(self, path=None, audiofile=None, next=False, notification=False):
        if path is not None:
            with open(path, "rb") as wav_file:
                input_wav = wav_file.read()
        if audiofile is not None:
            with open(audiofile, "rb"):
                input_wav = wav_file.read()
        data = io.BytesIO(input_wav)
        if notification:
            self.Audio_Output.play_notification(data, next)
        else:
            self.Audio_Output.play_playback(data, next)

    def play_music(self, by_name=None, url=None, path=None, next=None, now=None, playlist=None, announce=None):
        if by_name is not None:
            by_name = "'" + by_name + "'"
        # simply forward information
        self.Audio_Output.music_player.play(by_name=by_name, url=url, path=path, next=next, now=now, playlist=playlist,
                                            announce=announce)

    def listen(self, text=None, messenger=None):
        if messenger is None:
            messenger = self.messenger_call
        if text is not None:
            self.say(text)
        if messenger:
            return self.core.messenger_listen(self.user["first_name"].lower())
        else:
            return self.Audio_Input.recognize_input(listen=True)

    def recognize(self, audio_file):
        return self.Audio_Input.recognize_file(audio_file)

    @staticmethod
    def words_in_text(words, text):
        for word in words:
            if word not in text:
                return False
        return True

    def start_module(self, name=None, text=None, user=None):
        self.core.start_module(text, name, user, messenger=self.messenger)

    def start_module_and_confirm(self, name=None, text=None, user=None):
        return self.core.start_module(text, name, user)

    def module_storage(self, module_name=None):
        module_storage = self.core.local_storage.get("module_storage")
        if module_name is None:
            return module_storage
        # I am now just so free and lazy and assume that a module name is passed from a module that actually exists.
        else:
            return module_storage[module_name]

    @staticmethod
    def translate(text, target_lang='de'):
        try:
            request = Request(
                'https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=' + urllib.parse.quote(
                    target_lang) + '&dt=t&q=' + urllib.parse.quote(
                    text))
            response = urlopen(request)
            answer = json.loads(response.read())
            return answer[0][0][0]
        except:
            return text

    def correct_output(self, core_array, messenger_array):
        if self.messenger_call is True:
            return messenger_array
        else:
            return core_array

    def correct_output_automate(self, text):
        text = text.strip()
        # This function is to correct words that should always be corrected right away,
        # so that correct_output doesn't have to be called every time and corrected manually
        # must be corrected
        if self.messenger_call:
            pass
        else:
            correct_output = self.core.config_data["correct_output"]
            for item in correct_output:
                text = text.replace(item, correct_output[item])
        return text

    def start_hotword_detection(self):
        self.Audio_Input.start()

    def stopp_hotword_detection(self):
        self.Audio_Input.stop()

    def speechVariation(self, userInput):
        """
        if not isinstance(input, str):
            parse = random.choice(userInput)
        else:
            parse = userInput
        while "[" in parse and "]" in parse:
            sp0 = parse.split("[", 1)
            front = sp0[0]
            sp1 = sp0[1].split("]", 1)
            middle = sp1[0].split("|", 1)
            end = sp1[1]
            parse = front + random.choice(middle) + end
            """
        # toDo
        return userInput


def testValidationData(intent_wrapper):
    with open("validation_data.json", encoding='utf-8') as validation_file:
        print(validation_file.encoding)
        val_data = json.load(validation_file)
        for item in val_data["validation"]:
            response = intent_wrapper.test_module(item)
            if response != val_data["validation"][item]:
                print("FEHLER: " + item + " was not working, result: " + response + "\n")

def testIntentData (intent_wrapper):
    with open("intents.json", encoding='utf-8') as validation_file:
        data = json.load(validation_file)
        for item in data["intents"]:
            for sentence in item["patterns"]:
                response = intent_wrapper.test_module(sentence)
                if response != item["tag"]:
                    print("FEHLER: " + sentence + " was not working, result: " + response + "\n")


if __name__ == "__main__":

    print("Start System")
    intent_wrapper = IntentWrapper(Core())
    print("training...")
    intent_wrapper.train_model()
    print("Intent init!")
    testIntentData(intent_wrapper)
    print("Intent testing done")
    testValidationData(intent_wrapper)
    print("Validation data testing done")
    while True:
        print(intent_wrapper.proceed_with_user_input(input("Type in something: ")))
