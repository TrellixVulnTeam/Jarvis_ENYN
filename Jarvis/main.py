import json
import os
import random
import time
import datetime
import urllib
from urllib.request import Request, urlopen
from Audio import AudioOutput, AudioInput
from resources.analyze import Sentence_Analyzer
import pkgutil
from pathlib import Path
from threading import Thread
import traceback
from resources.module_skills import skills
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

    def get_modules(self, directory, continuous=False):
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
                if continuous:
                    print('[INFO] Continuous module {} loaded'.format(name))
                    modules.append(mod)
                else:
                    print('[INFO] Modul {} loaded'.format(name))
                    modules.append(mod)
        modules.sort(key=lambda mod: mod.PRIORITY if hasattr(mod, 'PRIORITY') else 0, reverse=True)
        return modules

    def query_threaded(self, name, text, user, direct, messenger=False):
        print(f'Messenger: {messenger}')
        mod_skill = skills()
        if text == None:
            # generate a random text
            text = random.randint(0, 1000000000)
            analysis = {}
        else:
            # else there is a valid text -> analyze
            try:
                analysis = Core.Analyzer.analyze(str(text))
            except:
                traceback.print_exc()
                print('[ERROR] Sentence analysis failed!')
                analysis = {}
        if not name == None:
            # Module was called via start_module
            for module in self.modules:
                if module.__name__ == name:
                    Core.active_modules[str(text)] = self.Modulewrapper(text, analysis, messenger, user)
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
                        Core.active_modules[str(text)] = self.Modulewrapper(text, analysis, messenger, user)
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

    def start_module(self, user=None, text=None, name=None, direct=True, messenger=False):
        print(f'Messenger: {messenger}')
        # self.query_threaded(name, text, direct, messenger=messenger)
        mod_skill = skills()
        analysis = {}
        if text == None:
            text = str(random.randint(0, 1000000000))
        else:
            Log.write('ACTION', '{}'.format(text), conv_id=str(text), show=True)
            try:
                analysis = Core.Analyzer.analyze(str(text))
                # Log.write('ACTION', 'Analysis: ' + str(analysis), conv_id=str(text), show=True)
            except:
                traceback.print_exc()
                Log.write('ERROR', 'Sentence analysis failed!', conv_id=str(text), show=True)

        if name is not None:
            for module in self.modules:
                if module.__name__ == name:
                    Log.write('ACTION', '--Modul {} was called directly (Parameter: {})--'.format(name, text),
                              conv_id=str(text), show=False)
                    Core.active_modules[str(text)] = self.Modulewrapper(text, analysis, messenger, user)
                    mt = Thread(target=self.run_threaded_module, args=(text, module, mod_skill))
                    mt.daemon = True
                    mt.start()
        else:
            try:
                analysis = Core.Analyzer.analyze(str(text))
            except:
                traceback.print_exc()
                print('[ERROR] Sentence analysis failed!')
                analysis = {}
            for module in self.modules:
                try:
                    if module.isValid(text):
                        Core.active_modules[str(text)] = self.Modulewrapper(text, analysis, messenger, user)
                        mt = Thread(target=self.run_threaded_module, args=(text, module, mod_skill))
                        mt.daemon = True
                        mt.start()
                except:
                    traceback.print_exc()
                    print('[ERROR] Modul {} could not be queried!'.format(module.__name__))
        return False

    @staticmethod
    def run_threaded_module(text, module, mod_skill):
        try:
            module.handle(text, Core.active_modules[str(text)], mod_skill)
        except:
            traceback.print_exc()
            print('[ERROR] Runtime error in module {}. The module was terminated.\n'.format(module.__name__))
            Core.active_modules[str(text)].say(
                'Entschuldige, es gab ein Problem mit dem Modul {}.'.format(module.__name__))
        finally:
            try:
                del Core.active_modules[str(text)]
            except:
                pass
            return

    def run_module(self, text, modulewrapper, mod_skill):
        for module in self.modules:
            if module.isValid(text):
                module.handle(text, modulewrapper, )

    def run_continuous(self):
        # Runs the continuous_modules. Continuous_modules always run in the background,
        # to wait for events other than voice commands (e.g. sensor values, data etc.).
        Core.continuous_modules = {}
        for module in self.continuous_modules:
            intervalltime = module.INTERVALL if hasattr(module, 'INTERVALL') else 0
            if __name__ == '__main__':
                Core.continuous_modules[module.__name__] = self.Modulewrapper_continuous(intervalltime)
            try:
                module.start(Core.continuous_modules[module.__name__], Core.local_storage)
                Log.write('INFO', 'Modul {} started'.format(module.__name__), show=False)
            except:
                # traceback.print_exc()
                continue
        Local_storage['module_counter'] = 0
        while not self.continuous_stopped:
            for module in self.continuous_modules:
                if time.time() - Core.continuous_modules[module.__name__].last_call >= Core.continuous_modules[
                    module.__name__].intervall_time:
                    Core.continuous_modules[module.__name__].last_call = time.time()
                    try:
                        module.run(Core.continuous_modules[module.__name__], Core.local_storage)
                    except:
                        traceback.print_exc()
                        print(
                            '[ERROR] Runtime-Error in Continuous-Module {}. The module is no longer executed.\n'.format(
                                module.__name__))
                        del Core.continuous_modules[module.__name__]
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
                    module.stop(Core.continuous_modules[module.__name__], Core.local_storage)
                    Log.write('INFO', 'Modul {} terminated'.format(module.__name__), show=True)
                    no_stopped_modules = False
                except:
                    continue
            # clean up
            Core.continuous_modules = {}
            if no_stopped_modules:
                Log.write('INFO', '-- (None to finish)', show=True)
        return

    # toDo: run


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
    def __init__(self, text, analysis, messenger, user):
        self.text = text
        self.analysis = analysis
        self.analysis['town'] = Core.local_storage['home_location'] if self.analysis['town'] is None else None

        self.Audio_Output = Core.Audio_Output
        self.Audio_Input = Core.Audio_Input

        self.messenger_call = messenger

        self.room = "messenger" if messenger else "raum"
        self.messenger = Core.messenger

        self.core = Core
        self.Analyzer = Core.Analyzer
        self.local_storage = Core.local_storage
        self.server_name = Core.server_name
        self.system_name = Core.system_name
        self.path = Core.path
        self.user = user

    def say(self, text, output='auto'):
        """
        for better performance you can use:
        Add a break
        Mary had a little lamb <break time="1s"/> Whose fleece was white as snow.
        Emphasizing words
        I already told you I <emphasis level="strong">really like </emphasis> that person.
        Speed
        For dramatic purposes, you might wish to <prosody rate="slow">slow down the speaking rate of your text.</prosody>
        Or if you are in a hurry <prosody rate="fast">your may want to speed it up a bit.</prosody>
        Pitch
        Do you like sythesized speech <prosody pitch="high">with a pitch that is higher than normal?</prosody>
        Or do you prefer your speech <prosody pitch="-20%">with a somewhat lower pitch?</prosody>
        Whisper
        <amazon:effect name="whispered">If you make any noise, </amazon:effect> she said, <amazon:effect name="whispered">they will hear us.</amazon:effect>
        """
        text = self.speechVariation(text)
        if output == 'auto':
            if self.messenger_call:
                output = 'messenger'
        if 'messenger' in output.lower() or self.messenger_call:
            self.messenger_say(text)
        else:
            text = self.correct_output_automate(text)
            self.Audio_Output.say(text)

    @staticmethod
    def corregate_voice_changes(text, output):
        skill = skills()
        times = 0
        if output == "messenger":
            for word in text.split(" "):
                if "<" in word and ">" and any(["break time", "emphasis level", "prosody rate", "prosody pitch", "amazon:effect"]) in word:
                    times += 1
            for i in range(times):
                text.replace(skill.get_text_beetween("<", text, end_word=">", output="String", split_text=False), '')

    def messenger_say(self, text):
        try:
            self.messenger.say(text, self.user['telegram_id'])
        except KeyError:
            Log.write('WARNING',
                      'Der Text "{}" konnte nicht gesendet werden, da für den Nutzer "{}" keine Telegram-ID angegeben '
                      'wurde'.format(text, self.user), show=True)
        return

    def play(self, path=None, audiofile=None, next=False, notification=False):
        if path != None:
            with open(path, "rb") as wavfile:
                input_wav = wavfile.read()
        if audiofile is not None:
            with open(audiofile, "rb"):
                input_wav = wavfile.read()
        data = io.BytesIO(input_wav)
        if notification:
            self.Audio_Output.play_notification(data, next)
        else:
            self.Audio_Output.play_playback(data, next)

    def play_music(self, by_name=None, url=None, path=None, next=None, now=None, playlist=None, announce=None):
        if by_name != None:
            by_name = "'" + by_name + "'"
        # simply forward information
        self.Audio_Output.music_player.play(by_name=by_name, url=url, path=path, next=next, now=now, playlist=playlist,
                                            announce=announce)

    def listen(self, messenger=False):
        if messenger:
            return self.core.messenger_listen(self.user)
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

    def start_module(self, name, text, user):
        Core.start_module(text, name, user)

    @staticmethod
    def start_module_and_confirm(name=None, text=None, user=None):
        return Core.start_module(text, name, user)

    @staticmethod
    def module_storage(module_name=None):
        module_storage = Core.local_storage.get("module_storage")
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
        self.messenger = Core.messenger
        self.core = Core
        self.Analyzer = Core.Analyzer
        self.audio_Input = Core.Audio_Input
        self.audio_Output = Core.Audio_Output
        self.local_storage = Core.local_storage
        self.server_name = Core.server_name
        self.system_name = Core.system_name
        self.path = Core.path

    def start_module(self, name=None, text=None, user=None):
        # user prediction is not implemented yet, therefore here the workaround
        # user = self.local_storage['user']
        Modules.start_module(text=text, user=user, name=name)

    def start_module_and_confirm(self, name=None, text=None, user=None):
        return Core.start_module(name, text, user)

    def module_storage(self, module_name=None):
        module_storage = Core.local_storage.get("module_storage")
        if module_name is None:
            return module_storage
        # I am now just so free and lazy and assume that a module name is passed from a module that actually exists.
        else:
            return module_storage[module_name]

    def translate(self, ttext, targetLang='de'):
        return Modulewrapper.translate(targetLang)


class LUNA:
    def __init__(self, local_storage):
        self.local_storage = local_storage
        self.Modules = Modules
        self.Log = Log
        self.Analyzer = Analyzer
        self.messenger = None
        self.messenger_queued_users = []  # These users are waiting for a response
        self.messenger_queue_output = {}

        self.users = Users()

        self.Audio_Input = Audio_Input
        self.Audio_Output = Audio_Output

        self.active_modules = {}
        self.continuous_modules = {}
        self.server_name = Server_name
        self.system_name = System_name
        self.path = Local_storage['LUNA_PATH']

    def messenger_thread(self):
        # Verarbeitet eingehende Telegram-Nachrichten, weist ihnen Nutzer zu etc.
        while True:
            for msg in self.messenger.messages.copy():
                # Load the user name from the corresponding table
                try:
                    user = self.users.get_user_by_name(msg['from']['first_name'])
                except KeyError:
                    # Messages from strangers will not be tolerated. They are nevertheless stored.
                    self.local_storage['rejected_messenger_messages'].append(msg)
                    try:
                        Log.write('WARNING',
                                  'Nachricht von unbekanntem Telegram-Nutzer {} ({}). Zugriff verweigert.'.format(
                                      msg['from']['first_name'], msg['from']['id']), conv_id=msg['text'], show=True)
                    except KeyError:
                        Log.write('WARNING',
                                  'Nachricht von unbekanntem Telegram-Nutzer ({}). Zugriff verweigert.'.format(
                                      msg['from']['id']), conv_id=msg['text'], show=True)
                    self.messenger.say(
                        'Entschuldigung, aber ich darf leider zur Zeit nicht mit Fremden reden.',
                        msg['from']['id'], msg['text'])
                    self.messenger.messages.remove(msg)
                    continue

                # no pictures available
                # if msg['type'] == "photo":
                #    self.messenger.say('Leider kann ich noch nichts mit Bildern anfangen.', self.users.get_user_by_name(user))
                # Message is definitely a (possibly inserted) "new request" ("Jarvis,...").
                if msg['text'].lower().startswith("Jarvis"):
                    Modules.start_module(text=msg['text'], user=user, messenger=True, direct=False)
                # Message is not a request at all, but a response (or a module expects such a response)
                elif user in self.messenger_queued_users:
                    self.messenger_queue_output[user] = msg
                # Message is a normal request
                else:
                    Modules.start_module(text=msg['text'], user=user, messenger=True, direct=False)
                '''if response == False:
                    self.messenger.say('Das habe ich leider nicht verstanden.', self.users.get_user_by_name(user)['messenger_id'])'''
                self.messenger.messages.remove(msg)
            time.sleep(0.5)

    def messenger_listen(self, user):
        # Tell the Telegram thread that you are waiting for a reply,
        # But only when no one else is waiting
        while True:
            if not user in self.messenger_queued_users:
                self.messenger_queued_users.append(user)
                break
            time.sleep(0.03)

    def hotword_detected(self, text):
        if text == "wrong assistant!":
            Audio_Output.say("Geh mir nicht fremd, du sau!")
        else:
            user = self.users.get_user_by_name(self.local_storage["user"])
            Modules.start_module(text=str(text), user=user)
            self.Audio_Output.continue_after_hotword()

    def start_module(self, text, name, user):
        # user prediction is not implemented yet, therefore here the workaround
        user = self.local_storage['user']
        Modules.query_threaded(name, text, user, direct=False)


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
            if not username == 'README.txt' and not username == 'README.md':
                userpath = os.path.join(location, username)
                self.add_user(userpath)
                Log.write('INFO', 'Nutzer {} geladen'.format(username), show=True)
        if self.users == []:
            Core.Audio_Output.say("Bitte richte zunächst einen Nutzer ein und starte dann das System wieder neu!")

    def add_user(self, path):
        with open(path + "/data.json") as user_file:
            user_data = json.load(user_file)["User_Info"]
        with open(path + ("/resources/user_storage.json")) as user_storage_file:
            user_storage = json.load(user_storage_file)
        user_data["user_storage"] = user_storage
        self.users.append(user_data)

    def get_user_by_name(self, name):
        for user in self.users:
            if user.get('first_name').lower() == name.lower():
                return user
        return None

    def get_user_by_i(self, id):
        for user in self.users:
            if user["id"] == id:
                return user
        return None

    def get_user_by_messenger_id(self, t_id):
        for user in self.users:
            if user["messenger_id"] == t_id:
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
    Modules = Modules(Local_storage)
    Analyzer = Sentence_Analyzer()
    Audio_Output = AudioOutput(voice=config_data["voice"])
    Core = LUNA(Local_storage)
    Core.local_storage['LUNA_starttime'] = time.time()
    Audio_Input.set_core(Core, Audio_Output)
    time.sleep(2)
    # -----------Starting-----------#
    Modules.start_continuous()
    Audio_Input.start()
    Audio_Output.start()
    time.sleep(0.75)

    if config_data['messenger']:
        Log.write('INFO', 'Start Telegram...', show=True)
        if config_data['messenger_key'] == '':
            Log.write('ERROR', 'No Telegram-Bot-Token entered!', show=True)
        else:
            from resources.messenger import TelegramInterface

            Core.messenger = TelegramInterface(config_data['messenger_key'], Core)
            Core.messenger.start()
            tgt = Thread(target=Core.messenger_thread)
            tgt.daemon = True
            tgt.start()

    Log.write('', '--------- FERTIG ---------\n\n', show=True)
    time.sleep(3)
    Core.Audio_Output.say("Jarvis wurde erfolgreich gestartet!")

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
