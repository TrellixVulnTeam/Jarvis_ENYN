import json
import os
import random
import time
import datetime
import urllib
import wave
from urllib.request import Request, urlopen
from Audio import AudioOutput, AudioInput
from analyze import Sentence_Analyzer
import pkgutil
from pathlib import Path
from threading import Thread
import traceback
from module_skills import skills
import gc
import io

class Modules:
    def __init__(self, local_storage):
        self.local_storage = local_storage
        self.modules = []
        self.continuous_modules = []

        self.Modulewrapper = Modulewrapper
        self.Modulewrapper_continuous = Modulewrapper_continuous

        self.continuous_stopped = False
        self.continuous_threads_running = 0

        self.load_modules()

    def load_modules(self):
        print('---------- MODULES...  ----------')
        self.modules = self.get_modules('modules')
        if self.modules == []:
            print('[INFO] -- (None present)')
        print('\n----- Continuous MODULES... -----')
        self.continuous_modules = self.get_modules('modules/continuous', continuous=True)
        if self.continuous_modules == []:
            print('[INFO] -- (None present)')

    def get_modules(self, directory, continuous = False):
        dirname = os.path.dirname(os.path.abspath(__file__))
        locations = [os.path.join(dirname, directory)]
        modules = []
        if "modules" not in Local_storage:
            Local_storage["modules"] = {}
        for finder, name, ispkg in pkgutil.walk_packages(locations):
            try:
                loader = finder.find_module(name)
                mod = loader.load_module(name)
            except:
                traceback.print_exc()
                self.local_storage["modules"][name] = {"name": name, "status": "error", type: "unknown"}
                print('[WARNING] Modul {} is incorrect and was skipped!'.format(name))
                continue
            else:
                if continuous == True:
                    print('[INFO] Continuous module {} loaded'.format(name))
                    modules.append(mod)
                else:
                    print('[INFO] Modul {} loaded'.format(name))
                    modules.append(mod)
        modules.sort(key=lambda mod: mod.PRIORITY if hasattr(mod, 'PRIORITY') else 0, reverse=True)
        return modules

    def query_threaded(self, name, text, direct, messenger=False):
        mod_skill = skills()
        if text == None:
            # generate a random text
            text = random.randint(0, 1000000000)
            analysis = {}
        else:
            # else there is a valid text -> analyze
            try:
                analysis = Luna.Analyzer.analyze(str(text))
            except:
                traceback.print_exc()
                print('[ERROR] Sentence analysis failed!')
                analysis = {}
        if not name == None:
            # Module was called via start_module
            for module in self.modules:
                if module.__name__ == name:
                    Luna.active_modules[str(text)] = self.Modulewrapper(text, analysis, messenger)
                    mt = Thread(target=self.run_threaded_module, args=(text, module, mod_skill))
                    mt.daemon = True
                    mt.start()
                    return True
            print('[ERROR] Modul {} could not be found!'.format(name))
        elif not text == None:
            # Search the modules normally
            for module in self.modules:
                try:
                    if module.isValid(text):
                        Luna.active_modules[str(text)] = self.Modulewrapper(text, analysis, messenger)
                        mt = Thread(target=self.run_threaded_module, args=(text, module, mod_skill))
                        mt.daemon = True
                        mt.start()
                        return True
                except:
                    traceback.print_exc()
                    print('[ERROR] Modul {} could not be queried!'.format(module.__name__))
        return False

    def start_continuous(self):
        self.continuous_threads_running = 0
        if not self.continuous_modules == []:
            cct = Thread(target=self.run_continuous)
            cct.daemon = True
            cct.start()
            self.continuous_threads_running += 1
        else:
            print('[INFO] -- (None present)')
        return

    def start_module(self, text=None, name=None, direct=True, messenger=False):
        self.query_threaded(name, text, direct, messenger=messenger)
        mod_skill = skills()
        analysis = {}
        if text == None:
            text = random.randint(0,1000000000)
        else:
            Log.write('ACTION', '{}'.format(text), conv_id=str(text), show=True)
            try:
                analysis = Luna.Analyzer.analyze(str(text))
                Log.write('ACTION', 'Analysis: ' + str(analysis), conv_id=str(text), show=True)
            except:
                traceback.print_exc()
                Log.write('ERROR', 'Sentence analysis failed!', conv_id=str(text), show=True)

        if name is not None:
            for module in self.modules:
                if module.__name__ == name:
                    Log.write('ACTION', '--Modul {} was called directly (Parameter: {})--'.format(name, text), conv_id=str(text), show=True)
                    Luna.active_modules[str(text)] = self.Modulewrapper(text, analysis, messenger)
        else:
            try:
                analysis = Luna.Analyzer.analyze(str(text))
            except:
                traceback.print_exc()
                print('[ERROR] Sentence analysis failed!')
                analysis = {}
        for module in self.modules:
            try:
                if module.isValid(text):
                    Luna.active_modules[str(text)] = self.Modulewrapper(text, analysis, messenger=messenger)
                    mt = Thread(target=self.run_threaded_module, args=(text, module, mod_skill))
                    mt.daemon = True
                    mt.start()
            except:
                traceback.print_exc()
                print('[ERROR] Modul {} could not be queried!'.format(module.__name__))
        return False

    def run_threaded_module(self, text, module, mod_skill):
        try:
            module.handle(text, Luna.active_modules[str(text)], mod_skill)
        except:
            traceback.print_exc()
            print('[ERROR] Runtime error in module {}. The module was terminated.\n'.format(module.__name__))
            Luna.active_modules[str(text)].say('Entschuldige, es gab ein Problem mit dem Modul {}.'.format(module.__name__))
        finally:
            del Luna.active_modules[str(text)]
            return

    def run_module(self, text, modulewrapper, mod_skill):
        for module in self.modules:
            if module.isValid(text):
                module.handle(text, modulewrapper, )

    def run_continuous(self):
        # Runs the continuous_modules. Continuous_modules always run in the background,
        # to wait for events other than voice commands (e.g. sensor values, data etc.).
        Luna.continuous_modules = {}
        for module in self.continuous_modules:
            intervalltime = module.INTERVALL if hasattr(module, 'INTERVALL') else 0
            if __name__ == '__main__':
                Luna.continuous_modules[module.__name__] = self.Modulewrapper_continuous(intervalltime)
            try:
                module.start(Luna.continuous_modules[module.__name__], Luna.local_storage)
                Log.write('INFO', 'Modul {} started'.format(module.__name__), show=True)
            except:
                # traceback.print_exc()
                continue
        Local_storage['module_counter'] = 0
        while not self.continuous_stopped:
            for module in self.continuous_modules:
                if time.time() - Luna.continuous_modules[module.__name__].last_call >= Luna.continuous_modules[module.__name__].intervall_time:
                    Luna.continuous_modules[module.__name__].last_call = time.time()
                    try:
                        module.run(Luna.continuous_modules[module.__name__], Luna.local_storage)
                    except:
                        traceback.print_exc()
                        print('[ERROR] Runtime-Error in Continuous-Module {}. The module is no longer executed.\n'.format(module.__name__))
                        del Luna.continuous_modules[module.__name__]
                        self.continuous_modules.remove(module)
            Local_storage['module_counter'] += 1
            time.sleep(0.01)
        self.continuous_threads_running -= 1


    def stop_continuous(self):
        # Stops the thread in which the continuous_modules are executed at the end of the run.
        # But gives the modules another opportunity to clean up afterwards...
        if self.continuous_threads_running > 0:
            Log.write('', '------ Modules are terminated...', show=True)
            self.continuous_stopped = True
            # Wait until all threads have returned
            while self.continuous_threads_running > 0:
                print('waiting...', end='\r')
                time.sleep(0.01)
            self.continuous_stopped = False
            # Call the stop() function of each module, if present
            no_stopped_modules = True
            for module in self.continuous_modules:
                try:
                    module.stop(Luna.continuous_modules[module.__name__], Luna.local_storage)
                    Log.write('INFO', 'Modul {} terminated'.format(module.__name__), show=True)
                    no_stopped_modules = False
                except:
                    continue
            # clean up
            Luna.continuous_modules = {}
            if no_stopped_modules == True:
                Log.write('INFO', '-- (None to finish)', show=True)
        return

    #toDo: run
class Logging:
    def __init__(self):
        self.log = []

    def write(self, typ, content, info=None, conv_id=None, show=False):
        if info is not None:
            logentry = info
        else:
            logentry = {}
        logentry['time'] = datetime.time
        logentry['type'] = typ
        logentry['content'] = content
        logentry['show'] = show
        logentry['conv_id'] = conv_id
        try:
            last_logentry = self.log[-1]
        except IndexError:
            last_logentry = logentry
        self.log.append(logentry)
        if show:
            print(self.format(logentry, last_logentry))

    def format(self, logentry, last_logentry):
        if logentry['type'] == 'ERROR' or logentry['type'] == 'WARNING' or logentry['type'] == 'DEBUG' or logentry[
            'type'] == 'INFO' or logentry['type'] == 'TRACE':
            spaces = ''
            if last_logentry['type'] == 'ACTION':
                spaces = '\n\n'
                if last_logentry['conv_id'] == logentry['conv_id']:
                    spaces = ''
            textline = spaces + '[{}] '.format(logentry['type']) + logentry['content']

        elif logentry['type'] == 'ACTION':
            spaces = ''
            if not last_logentry['type'] == 'ACTION':
                spaces = '\n\n'
                if last_logentry['conv_id'] == logentry['conv_id']:
                    spaces = ''
            else:
                if not last_logentry['conv_id'] == logentry['conv_id']:
                    # conversation_id will be original_command at the beginning, but in wise
                    # foresight I renamed it already...
                    spaces = '\n'
                if last_logentry['conv_id'] == 'HW_DETECTED':
                    spaces = ''
            textline = spaces + logentry['content']

        else:
            textline = logentry['content']
        return textline

class Modulewrapper:
    def __init__(self, text, analysis, messenger):
        self.text = text
        self.analysis = analysis

        self.telegram_call = messenger
        self.Audio_Output = Luna.Audio_Output
        self.Audio_Input = Luna.Audio_Input

        self.telegram_call = messenger
        self.telegram = Luna.telegram

        self.room = "telegram" if messenger else "raum"
        self.messenger = messenger

        self.core = Luna
        self.Analyzer = Luna.Analyzer
        self.local_storage = Luna.local_storage
        self.server_name = Luna.server_name
        self.system_name = Luna.system_name
        self.path = Luna.path
        self.user = self.local_storage["users"][self.local_storage["user"]]

    def say(self, text, output='auto'):
        text = self.speechVariation(text)
        if output == 'auto':
            if 'telegram' in output.lower() or self.messenger:
                self.telegram_say(text)
            else:
                text = self.correct_output_automate(text)
                print('\n--{}:-- {}'.format(self.system_name.upper(), text))
                self.Audio_Output.say(text)

    def telegram_say(self, text):
        try:
            self.telegram.say(text, self.local_storage["telegram_name_to_id_table"][self.user["name"]])
        except KeyError:
            Log.write('WARNING',
                      'Der Text "{}" konnte nicht gesendet werden, da für den Nutzer "{}" keine Telegram-ID angegeben wurde'.format(
                          text, self.user), show=True)
        return

    def play(self, path=None, audiofile=None, next=False, notification=False):
        if path != None:
            with open(path, "rb") as wavfile:
                input_wav = wavfile.read()
        if audiofile != None:
            with open(audiofile, "rb"):
                input_wav = wavfile.read()
        data = io.BytesIO(input_wav)
        if notification:
            self.Audio_Output.play_notification(data, next)
        else:
            self.Audio_Output.play_playback(data, next)

    def play_music(self, url=False, announce=False, next=False):
        # simply forward information
        self.Audio_Output.music_player.play(url=url, next=next, announce=announce)

    def listen(self, telegram=False):
        if telegram:
            return self.core.telegram_listen(self.user)
        else:
            return self.Audio_Input.recognize_input(listen=True)

    def recognize(self, audio_file):
        return self.Audio_Input.recognize_file(audio_file)

    def words_in_text(self, words, text):
        for word in words:
            if word not in text:
                return False
        return True

    def start_module(self, name, text):
        Luna.start_module(text, name)

    def start_module_and_confirm(self, name=None, text=None):
        return Luna.start_module(text, name)

    def module_storage(self, module_name=None):
        module_storage = Luna.local_storage.get("module_storage")
        if module_name is None:
            return module_storage
        # I am now just so free and lazy and assume that a module name is passed from a module that actually exists.
        else:
            return module_storage[module_name]

    def translate(self, text, targetLang='de'):
        try:
            request = Request(
                'https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=' + urllib.parse.quote(
                    targetLang) + '&dt=t&q=' + urllib.parse.quote(
                    text))
            response = urlopen(request)
            answer = json.loads(response.read())
            return answer[0][0][0]
        except:
            return text

    def correct_output(self, luna_array, telegram_array):
        if self.telegram_call is True:
            return telegram_array
        else:
            return luna_array

    def correct_output_automate(self, text):
        text = text.strip()
        # This function is to correct words that should always be corrected right away,
        # so that correct_output doesn't have to be called every time and corrected manually
        # must be corrected
        if self.telegram_call:
            text = text.replace(' Uhr ', '')
        else:
            #text = text.replace('Tiffany', 'Tiffanie')
            #text = text.replace('Timer', 'Teimer')
            text = text.replace('Entschuldige', 'Tut mir leid')
        return text

    def start_hotword_detection(self):
        self.Audio_Input.start()

    def stopp_hotword_detection(self):
        self.Audio_Input.stop()

    def speechVariation(self, input):
        """
        This function is the counterpiece to the batchGen-function. It compiles the same
        sentence-format as given there but it only picks one random variant and directly
        pushes it into tiane. It returns the generated sentence.
        """
        if not isinstance(input, str):
            parse = random.choice(input)
        else:
            parse = input
        while "[" in parse and "]" in parse:
            t_a = time.time()
            sp0 = parse.split("[", 1)
            front = sp0[0]
            sp1 = sp0[1].split("]", 1)
            middle = sp1[0].split("|", 1)
            end = sp1[1]
            t_b = time.time()
            parse = front + random.choice(middle) + end
        return parse


class Modulewrapper_continuous:
    # The same class for continuous_modules. The peculiarity: The say- and listen-functions
    # are missing (so exactly what the module wrapper was actually there for xD), because continuous_-
    # modules are not supposed to make calls to the outside. For this there is a
    # parameter for the time between two calls of the module.
    def __init__(self, intervalltime):
        self.intervall_time = intervalltime
        self.last_call = 0
        self.counter = 0
        self.telegram = Luna.telegram
        self.core = Luna
        self.Analyzer = Luna.Analyzer
        self.audio_Input = Luna.Audio_Input
        self.audio_Output = Luna.Audio_Output
        self.local_storage = Luna.local_storage
        self.server_name = Luna.server_name
        self.system_name = Luna.system_name
        self.path = Luna.path

    def start_module(self, name=None, text=None):
        Modules.start_module(text=text, name=name)

    def start_module_and_confirm(self, name=None, text=None):
        return Luna.start_module(name, text)

    def module_storage(self, module_name=None):
            module_storage = Luna.local_storage.get("module_storage")
            if module_name is None:
                return module_storage
            # I am now just so free and lazy and assume that a module name is passed from a module that actually exists.
            else:
                return module_storage[module_name]

    def translate(self, ttext, targetLang='de'):
        return Modulewrapper.translate(ttext, targetLang)


class LUNA:
    def __init__(self, local_storage):
        self.local_storage = local_storage
        self.Modules = Modules
        self.Log = Log
        self.Analyzer = Analyzer
        self.telegram = None
        self.telegram_queued_users = []  # These users are waiting for a response
        self.telegram_queue_output = {}

        self.users = Users()

        self.Audio_Input = Audio_Input
        self.Audio_Output = Audio_Output

        self.active_modules = {}
        self.continuous_modules = {}
        self.server_name = Server_name
        self.system_name = System_name
        self.path = Local_storage['LUNA_PATH']

    def telegram_thread(self):
        # Verarbeitet eingehende Telegram-Nachrichten, weist ihnen Nutzer zu etc.
        while True:
            for msg in self.telegram.messages.copy():
                # Load the user name from the corresponding table
                try:
                    user = msg['from']['first_name']
                except KeyError:
                    # Messages from strangers will not be tolerated. They are nevertheless stored.
                    self.local_storage['rejected_telegram_messages'].append(msg)
                    try:
                        Log.write('WARNING',
                                  'Nachricht von unbekanntem Telegram-Nutzer {} ({}). Zugriff verweigert.'.format(
                                      msg['from']['first_name'], msg['from']['id']), conv_id=msg['text'], show=True)
                    except KeyError:
                        Log.write('WARNING',
                                  'Nachricht von unbekanntem Telegram-Nutzer ({}). Zugriff verweigert.'.format(
                                      msg['from']['id']), conv_id=msg['text'], show=True)
                    self.telegram.say(
                        'Entschuldigung, aber ich darf leider zur Zeit nicht mit Fremden reden.',
                        msg['from']['id'], msg['text'])
                    self.telegram.messages.remove(msg)
                    continue

                response = True
                # Message is definitely a (possibly inserted) "new request" ("Jarvis,...").
                if msg['text'].lower().startswith("Jarvis"):
                    response = Modules.start_module(text=msg['text'], messenger=True, direct=False)
                # Message is not a request at all, but a response (or a module expects such a response)
                elif user in self.telegram_queued_users:
                    self.telegram_queue_output[user] = msg
                # Message is a normal request
                else:
                    response = Modules.start_module(text=msg['text'], messenger=True, direct=False)
                if response == False:
                    self.telegram.say('Das habe ich leider nicht verstanden.', self.users.get_user_by_name(user))
                self.telegram.messages.remove(msg)
            time.sleep(0.5)

    def telegram_listen(self, user):
        # Tell the Telegram thread that you are waiting for a reply,
        # But only when no one else is waiting
        while True:
            if not user in self.telegram_queued_users:
                self.telegram_queued_users.append(user)
                break
            time.sleep(0.03)

    def hotword_detected(self, text):
        if text == "Audio could not be recorded":
            """
            md = Modulewrapper(text, None, None)
            Modulewrapper.say(md, "Bitte wiederhole deine Frage.")
            self.Audio_Input.recognize_input()
            """
            pass
        elif text == "wrong assistant!":
            Audio_Output.say("Geh mir nicht fremd!")
        else:
            Modules.start_module(text)

    def start_module(self, text, name):
        Modules.query_threaded(name, text, direct=True)

    def play_bling_sound(self):
        # The name was deliberately chosen with regard to further reactions (such as lights, etc.)

        # playing Bling-Sound
        TOP_DIR = os.path.dirname(os.path.abspath(__file__))
        DETECT_DONG = os.path.join(TOP_DIR, "resources/bling.wav")

        with open(DETECT_DONG, "rb") as wavfile:
            input_wav = wavfile.read()
        data = io.BytesIO(input_wav)
        self.Audio_Output.play_notification(data, next=True)


class Users:
    def __init__(self):
        self.users = []
        self.load_users()

    def get_user_list(self):
        return self.users

    def load_users(self):
        # Load users separately from the users folder
        Log.write('', '---------- USERS ---------', show=True)
        location = os.path.join(absPath, 'users')
        subdirs = os.listdir(location)
        try:
            subdirs.remove("README.txt")
            subdirs.remove("README.md")
        except ValueError:
            pass
        # We will now go through the individual subfolders of server/users to set up the users.
        # users. The subfolders conveniently have the names of the users.
        for username in subdirs:
            userpath = os.path.join(location, username)
            self.add_user(userpath)
            Log.write('INFO', 'Nutzer {} geladen'.format(username), show=True)

    def add_user(self, path):
        with open(path + "/data.json") as user_file:
            user_data = json.load(config_file)
        with open(path + ("/resources/user_storage.json")) as user_storage_file:
            user_storage = json.load(user_storage_file)
        user_data["user_storage"] = user_storage
        self.users.append(user_data)

    def get_user_by_name(self, name):
        for user in self.users:
            if user["name"] == name:
                return user
        return None

    def get_user_by_id(self, id):
        for user in self.users:
            if user["id"] == id:
                return user
        return None

    def get_user_by_telegram_id(self, t_id):
        for user in self.users:
            if user["telegram_id"] == t_id:
                return user
        return None

"""def clear_momory():
    while True:
        time.sleep(60)
        gc.collect()"""

if __name__ == "__main__":
    relPath = str(Path(__file__).parent) + "/"
    absPath = os.path.dirname(os.path.abspath(__file__))

    Log = Logging()

    Log.write('', '--------- Start System ---------\n\n', show=True)

    with open(relPath + "config.json", "r") as config_file:
        config_data = json.load(config_file)

    System_name = config_data['System_name']
    Server_name = config_data['Server_name']
    Home_location = config_data["Local_storage"]["home_location"]
    Local_storage = config_data['Local_storage']
    Local_storage['LUNA_PATH'] = absPath
    Audio_Input = AudioInput()
    # clear unnececary warnings
    os.system('clear')
    print("\n\n\n\n\n\n")
    Modules = Modules(Local_storage)
    Analyzer = Sentence_Analyzer()
    Audio_Output = AudioOutput()
    Luna = LUNA(Local_storage)
    Luna.local_storage['LUNA_starttime'] = time.time()
    Audio_Input.set_luna(Luna)
    time.sleep(2)
    # -----------Starting-----------#
    Modules.start_continuous()
    Audio_Input.start()
    Audio_Output.start()
    time.sleep(0.75)

    if config_data['telegram']:
        Log.write('', '', show=True)
        Log.write('INFO', 'Starte Telegram...', show=True)
        if config_data['telegram_key'] == '':
            Log.write('ERROR', 'Kein Telegram-Bot-Token angegeben!', show=True)
        else:
            from resources.telegram import TelegramInterface

            Luna.telegram = TelegramInterface(config_data['telegram_key'], Luna)
            Luna.telegram.start()
            tgt = Thread(target=Luna.telegram_thread)
            tgt.daemon = True
            tgt.start()

    Log.write('', '--------- FERTIG ---------\n\n', show=True)
    Luna.Audio_Output.say("Jarvis wurde erfolgreich gestartet!")

    # Starting the main-loop
    # main_loop(Local_storage)
    """memory_control = Thread(target=clear_momory())
    memory_control.daemon = True
    memory_control.start()"""

    while True:
        try:
            time.sleep(10)
        except:
            Modules.stop_continuous()
            Audio_Input.stop()
            Audio_Output.stop()
            Log.write('', '\n[{}] Goodbye!\n'.format(System_name.upper()), show=True)
            break