import io
import json
import logging
import os
import pkgutil
import random
import time
import traceback
from threading import Thread
from typing import AnyStr, Any

import requests

import src.speechassistant.wb_server as ws
from src.speechassistant.Audio import AudioOutput, AudioInput
from src.speechassistant.resources.analyze import Sentence_Analyzer
from src.speechassistant.resources.module_skills import Skills
from src.speechassistant.resources.intent.Wrapper import IntentWrapper as AIWrapper
from src.speechassistant.database.database_connection import DataBase
from src.speechassistant.services import *


class Core:
    def __init__(self, conf_dat: dict, analyzer: Sentence_Analyzer, audio_input: AudioInput, audio_output: AudioOutput,
                 system_name: str) -> None:
        self.local_storage: dict = conf_dat["Local_storage"]
        self.config_data: dict = conf_dat
        self.use_ai = conf_dat["ai"]
        self.path: str = conf_dat["Local_storage"]['CORE_PATH']
        self.data_base = DataBase(f'{self.path}/database')
        self.data_base.user_interface.add_user('Jakob', 'Jakob', 'Priesner', {'day': 5, 'month': 9, 'year': 2002})
        self.skills: Skills = Skills()
        self.__data: dict = conf_dat
        self.__fill_data()  # since the path is needed, __fill_data() is called only here
        self.modules: Modules = None
        self.analyzer: Sentence_Analyzer = analyzer
        self.services: Services = Services(self, self.__data, conf_dat)
        self.messenger = None
        self.messenger_queued_users: list = []  # These users are waiting for a response
        self.messenger_queue_output: dict = {}

        self.users: Users = Users(self)

        self.audio_input: AudioInput = audio_input
        self.audio_output: AudioOutput = audio_output

        self.active_modules: dict = {}
        self.continuous_modules: dict = {}
        self.system_name: str = system_name

        self.ai: AIWrapper = AIWrapper(self)
        self.skills: Skills = Skills()

        if self.local_storage["home_location"] == "":
            self.local_storage["home_location"] = requests.get("https://ipinfo.io").json()["city"]

    def __fill_data(self) -> None:
        with open(relPath + '/data/api_keys.dat') as api_file:
            self.__data["api_keys"] = json.load(api_file)

    def messenger_thread(self) -> None:
        # Verarbeitet eingehende Telegram-Nachrichten, weist ihnen Nutzer zu etc.
        while True:
            for msg in self.messenger.messages.copy():
                # Load the user name from the corresponding table
                try:
                    user: dict = self.users.get_user_by_name(msg['from']['first_name'].lower())
                except KeyError:
                    # Messages from strangers will not be tolerated. They are nevertheless stored.
                    self.local_storage['rejected_messenger_messages'].append(msg)
                    try:
                        logging.warning('[WARNING] Message from unknown Telegram user {}. Access denied.'.format(
                            msg['from']['first_name']))
                    except KeyError:
                        logging.warning('[WARNING] Message from unknown Telegram user {}. Access denied.'.format(
                            msg['from']['id']))
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
                    self.modules.start_module(text=msg['text'], user=user, messenger=True)
                # Message is not a request at all, but a response (or a module expects such a response)
                elif msg['from']['first_name'].lower() in self.messenger_queued_users:
                    self.messenger_queue_output[msg['from']['first_name'].lower()] = msg
                # Message is a normal request
                else:
                    # self.modules.start_module(text=msg['text'], user=user, messenger=True)
                    th: Thread = Thread(target=self.modules.start_module, args=(user, msg['text'], None, True,))
                    th.daemon = True
                    th.start()
                '''if response == False:
                    self.messenger.say('Das habe ich leider nicht verstanden.', self.users.get_user_by_name(user)['messenger_id'])'''
                self.messenger.messages.remove(msg)
            time.sleep(0.5)

    def messenger_listen(self, user: str):
        # Tell the Telegram thread that you are waiting for a reply,
        # But only when no one else is waiting
        if user not in self.messenger_queued_users:
            self.messenger_queued_users.append(user)

        while True:
            # Schauen, ob die Telegram-Antwort eingegangen ist
            response = self.messenger_queue_output.pop(user, None)
            if response is not None:
                self.messenger_queued_users.remove(user)
                logging.info('[ACTION] --{}-- (Messenger): {}'.format(user.upper(), response['text']))
                return response["text"]
            time.sleep(0.03)

    def webserver_action(self, action: str) -> str:
        if action == 'mute':
            return 'ok'
        else:
            return 'err'

    def reload_system(self) -> None:
        reload(self)

    def hotword_detected(self, text: str) -> None:
        user: dict = self.users.get_user_by_name(self.local_storage["user"])
        if self.use_ai:
            response: str | dict = self.ai.proceed_with_user_input(text)
            if response is None:
                # if the AI has not found a matching module, try to find one via isValid()
                self.modules.start_module(text=str(text), user=user)
            elif type(response) is str:
                self.audio_output.say(response)
            elif type(response) is dict:
                self.start_module(text, response["module"], user=user)
            else:
                raise ValueError('Invalid type of attribute "text"!')
        else:
            self.modules.start_module(text=str(text), user=user)

    def start_module(self, text: str, name: str, user: dict = None) -> bool:
        # user prediction is not implemented yet, therefore here the workaround
        user: dict = self.local_storage['user']
        return self.modules.query_threaded(name, text, user)


class ModuleWrapper:
    def __init__(self, core: Core, text: str, analysis: dict, messenger: bool, user: dict) -> None:
        self.text: str = text
        self.analysis: dict = analysis
        # toDo: down below
        # self.analysis['town'] = core.local_storage['home_location'] if self.analysis['town'] is None else None

        self.audio_output: AudioOutput = core.audio_output
        self.audio_input: AudioInput = core.audio_input

        self.messenger_call: bool = messenger

        self.room: str = "messenger" if messenger else "raum"
        self.messenger = core.messenger

        self.core: Core = core
        self.skills: Skills = core.skills
        self.services: Services = core.services
        self.data_base = core.data_base

        self.Analyzer: Sentence_Analyzer = core.analyzer

        self.local_storage: dict = core.local_storage
        self.system_name: str = core.system_name
        self.path: str = core.path
        self.user: dict = user

    def say(self, text: str | list, output: str = 'auto') -> None:
        if type(text) is list:
            text = random.choice(text)
        text: str = self.speech_variation(text)
        if output == 'auto':
            if self.messenger_call:
                output = 'messenger'
        if 'messenger' in output.lower() or self.messenger_call:
            self.messenger_say(text)
        else:
            text = self.correct_output_automate(text)
            self.audio_output.say(text)

    def messenger_say(self, text: str) -> None:
        try:
            self.messenger.say(text, self.user['telegram_id'])
        except KeyError:
            logging.warning(
                '[WARNING] Sending message "{}" to messenger failed, because there is no Telegram-ID for this user '
                '({}) '.format(text, self.user["name"]))
        except AttributeError:
            logging.info('[WARNING] Sending message to messenger failed,  because there is no key for it!')
        return

    def play(self, path: str = None, audiofile: str = None, next: bool = False,
             notification: bool = False) -> None:
        if path is not None:
            with open(path, "rb") as wav_file:
                input_wav: AnyStr = wav_file.read()
        if audiofile is not None:
            with open(audiofile, "rb"):
                input_wav: AnyStr = wav_file.read()
        data: io.BytesIO = io.BytesIO(input_wav)
        if notification:
            self.audio_output.play_notification(data, next)
        else:
            self.audio_output.play_playback(data, next)

    def play_music(self, by_name: str = None, url: str = None, path: str = None, as_next: bool = False,
                   now: bool = False, playlist: bool = False, announce: bool = False) -> None:
        if by_name is not None:
            by_name = "'" + by_name + "'"
        # simply forward information
        self.audio_output.music_player.play(by_name=by_name, url=url, path=path, as_next=as_next, now=now,
                                            playlist=playlist,
                                            announce=announce)

    def listen(self, text: str = None, messenger: bool = None) -> str:
        if messenger is None:
            messenger: bool = self.messenger_call
        if text is not None:
            self.say(text)
        if messenger:
            return self.core.messenger_listen(self.user["first_name"].lower())
        else:
            return self.audio_input.recognize_input(self.core.hotword_detected, listen=True)

    def recognize(self, audio_file: Any) -> str:
        return self.audio_input.recognize_file(audio_file)

    @staticmethod
    def words_in_text(words: list, text: str) -> bool:
        for word in words:
            if word not in text:
                return False
        return True

    def start_module(self, name: str = None, text: str = None, user: dict = None) -> None:
        self.core.start_module(text, name, user)

    def start_module_and_confirm(self, name: str = None, text: str = None, user: dict = None) -> bool:
        return self.core.start_module(text, name, user)

    def module_storage(self, module_name=None):
        module_storage = self.core.local_storage.get("module_storage")
        if module_name is None:
            return module_storage
        # I am now just so free and lazy and assume that a module name is passed from a module that actually exists.
        else:
            return module_storage[module_name]

    """
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
        except Exception:
            return text
    """

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
        self.audio_input.start(config_data['Local_storage']['wakeword_sentensivity'], self.core.hotword_detected)

    def stopp_hotword_detection(self):
        self.audio_input.stop()

    @staticmethod
    def speech_variation(user_input):
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
        return user_input


class Modulewrapper_continuous:
    # The same class for continuous_modules. The peculiarity: The say- and listen-functions
    # are missing (so exactly what the module wrapper was actually there for xD), because continuous_-
    # modules are not supposed to make calls to the outside. For this there is a
    # parameter for the time between two calls of the module.
    def __init__(self, core, intervall_time, modules):
        self.intervall_time = intervall_time
        self.last_call = 0
        self.counter = 0
        self.messenger = core.messenger
        self.core = core
        self.Analyzer = core.analyzer
        self.services = core.services
        self.data_base = core.data_base
        self.audio_Input = core.audio_input
        self.audio_output = core.audio_output
        self.local_storage = core.local_storage
        self.system_name = core.system_name
        self.path = core.path
        self.modules = modules

    def start_module(self, name=None, text=None, user=None):
        # user prediction is not implemented yet, therefore here the workaround
        # user = self.local_storage['user']
        self.modules.start_module(text=text, user=user, name=name)

    def start_module_and_confirm(self, name=None, text=None, user=None):
        return self.core.start_module(name, text, user)

    def module_storage(self, module_name=None):
        module_storage = self.core.local_storage.get("module_storage")
        if module_name is None:
            return module_storage
        # I am now just so free and lazy and assume that a module name is passed from a module that actually exists.
        else:
            return module_storage[module_name]

    def translate(self, ttext, targetLang='de'):
        return ModuleWrapper.translate(targetLang)


class Modules:
    def __init__(self, core: Core, local_storage: dict) -> None:
        logging.getLogger().setLevel(logging.INFO)
        self.core: Core = core
        self.local_storage: dict = local_storage
        self.modules: list = []
        self.continuous_modules: list = []

        self.module_wrapper = ModuleWrapper
        self.module_wrapper_continuous = Modulewrapper_continuous

        self.continuous_stopped: bool = False
        self.continuous_threads_running: int = 0

        self.load_modules()

    def load_modules(self) -> None:
        self.local_storage["modules"]: dict = {}
        time.sleep(1)
        print('---------- MODULES...  ----------')
        self.modules: list = self.get_modules('modules')
        if self.modules is []:
            print('[INFO] -- (None present)')
        print('\n----- Continuous MODULES... -----')
        self.continuous_modules: list = self.get_modules('modules/continuous', continuous=True)
        if self.continuous_modules is []:
            print('[INFO] -- (None present)')

    def get_modules(self, directory: str, continuous: bool = False) -> list:
        dirname: str = os.path.dirname(os.path.abspath(__file__))
        locations: list = [os.path.join(dirname, directory)]
        modules: list = []
        if "modules" not in self.local_storage:
            self.local_storage["modules"]: dict = {}
        for finder, name, ispkg in pkgutil.walk_packages(locations):
            try:
                loader = finder.find_module(name)
                mod = loader.load_module(name)
                self.local_storage["modules"][name]: dict = {"name": name, "status": "loaded"}
            except:
                traceback.print_exc()
                self.local_storage["modules"][name]: dict = {"name": name, "status": "error"}
                print('[WARNING] Module {} is incorrect and was skipped!'.format(name))
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

    def query_threaded(self, name: str, text: str, user: dict, messenger: bool = False) -> bool:
        mod_skill: Skills = self.core.skills
        if text is None:
            # generate a random text
            text: str = str(random.randint(0, 1000000000))
            analysis: dict = {}
        else:
            # else there is a valid text -> analyze
            try:
                analysis: dict = self.core.analyzer.analyze(str(text))
            except Exception:
                traceback.print_exc()
                print('[ERROR] Sentence analysis failed!')
                analysis: dict = {}
        if name is not None:
            # Module was called via start_module
            for module in self.modules:
                if module.__name__ == name:
                    self.core.active_modules[str(text)]: ModuleWrapper = self.module_wrapper(self.core, text, analysis,
                                                                                             messenger,
                                                                                             user)
                    mt: Thread = Thread(target=self.run_threaded_module, args=(text, module, mod_skill))
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
                        mt: Thread = Thread(target=self.run_threaded_module, args=(text, module, mod_skill))
                        mt.daemon = True
                        mt.start()
                        return True
                except Exception:
                    traceback.print_exc()
                    print('[ERROR] Modul {} could not be queried!'.format(module.__name__))
        return False

    def start_continuous(self) -> None:
        self.continuous_threads_running: int = 0
        if not self.continuous_modules == []:
            cct: Thread = Thread(target=self.run_continuous)
            cct.daemon = True
            cct.start()
            self.continuous_threads_running += 1
        else:
            print('[INFO] -- (None present)')
        return

    def start_module(self, user: dict = None, text: str = None, name: str = None,
                     messenger: bool = False) -> bool:
        # self.query_threaded(name, text, direct, messenger=messenger)
        mod_skill: Skills = self.core.skills
        analysis: dict = {}
        if text is None:
            text: str = str(random.randint(0, 1000000000))
        else:
            try:
                analysis: dict = self.core.analyzer.analyze(str(text))
                # logging.info('Analysis: ' + str(analysis))
            except Exception:
                traceback.print_exc()
                logging.warning('[WARNING] Sentence analysis failed!')

        if name is not None:
            for module in self.modules:
                if module.__name__ == name:
                    logging.info('[ACTION] --Modul {} was called directly (Parameter: {})--'.format(name, text))
                    self.core.active_modules[str(text)]: ModuleWrapper = self.module_wrapper(self.core, text, analysis,
                                                                                             messenger,
                                                                                             user)
                    mt: Thread = Thread(target=self.run_threaded_module, args=(text, module, mod_skill))
                    mt.daemon = True
                    mt.start()
                    break
        else:
            try:
                analysis: dict = self.core.analyzer.analyze(str(text))
            except:
                traceback.print_exc()
                print('[ERROR] Sentence analysis failed!')
                analysis: dict = {}
            for module in self.modules:
                try:
                    if module.isValid(text.lower()):
                        self.core.active_modules[str(text)]: ModuleWrapper = self.module_wrapper(
                            self.core, text, analysis, messenger, user)
                        mt: Thread = Thread(target=self.run_threaded_module, args=(text, module, mod_skill))
                        mt.daemon = True
                        mt.start()
                        mt.join()  # wait until Module is done...
                        self.start_module(user=user, name='wartende_benachrichtigung')
                        break
                except Exception:
                    traceback.print_exc()
                    print('[ERROR] Modul {} could not be queried!'.format(module.__name__))
        return False

    def run_threaded_module(self, text: str, module: Any, mod_skill: Skills) -> None:
        try:
            module.handle(text, self.core.active_modules[str(text)], mod_skill)
        except Exception:
            traceback.print_exc()
            print('[ERROR] Runtime error in module {}. The module was terminated.\n'.format(module.__name__))
            self.core.active_modules[str(text)].say(
                'Entschuldige, es gab ein Problem mit dem Modul {}.'.format(module.__name__))
        finally:
            # Maybe a try catch is acquired
            del self.core.active_modules[str(text)]
            return

    def run_module(self, text: str, module_wrapper: ModuleWrapper, mod_skill: Skills) -> None:
        for module in self.modules:
            if module.isValid(text):
                module.handle(text, module_wrapper, mod_skill)

    def run_continuous(self) -> None:
        # Runs the continuous_modules. Continuous_modules always run in the background,
        # to wait for events other than voice commands (e.g. sensor values, data etc.).
        self.core.continuous_modules = {}
        for module in self.continuous_modules:
            interval_time: int = module.INTERVALL if hasattr(module, 'INTERVAL') else 0
            if __name__ == '__main__':
                self.core.continuous_modules[module.__name__] = self.module_wrapper_continuous(self.core,
                                                                                               interval_time,
                                                                                               self)
            try:
                module.start(self.core.continuous_modules[module.__name__], self.core.local_storage)
                logging.info('[ACTION] Modul {} started'.format(module.__name__))
            except Exception:
                # traceback.print_exc()
                continue
        self.local_storage['module_counter']: int = 0
        while not self.continuous_stopped:
            for module in self.continuous_modules:
                if time.time() - self.core.continuous_modules[module.__name__].last_call >= \
                        self.core.continuous_modules[module.__name__].intervall_time:
                    self.core.continuous_modules[module.__name__].last_call = time.time()
                    try:
                        module.run(self.core.continuous_modules[module.__name__], self.core.skills)
                    except Exception:
                        traceback.print_exc()
                        print(
                            '[ERROR] Runtime-Error in Continuous-Module {}. The module is no longer executed.\n'.format(
                                module.__name__))
                        del self.core.continuous_modules[module.__name__]
                        self.continuous_modules.remove(module)
            self.local_storage['module_counter'] += 1
            time.sleep(0.05)
        self.continuous_threads_running -= 1

    def stop_continuous(self) -> None:
        # Stops the thread in which the continuous_modules are executed at the end of the run.
        # But gives the modules another opportunity to clean up afterwards...
        if self.continuous_threads_running > 0:
            logging.info('------ Modules are terminated...')
            self.continuous_stopped = True
            # Wait until all threads have returned
            while self.continuous_threads_running > 0:
                print('waiting...', end='\r')
                time.sleep(0.05)
            self.continuous_stopped = False
            # Call the stop() function of each module, if present
            no_stopped_modules: bool = True
            for module in self.continuous_modules:
                try:
                    module.stop(self.core.continuous_modules[module.__name__], self.core.local_storage)
                    logging.info('[ACTION] Modul {} terminated'.format(module.__name__))
                    no_stopped_modules = False
                except Exception:
                    continue
            # clean up
            self.core.continuous_modules = {}
            if no_stopped_modules:
                logging.info('-- (None to finish)')
        return


class Services:
    def __init__(self, core: Core, __data: dict, configuration_data: dict) -> None:
        self.weather: Weather = Weather(__data["api_keys"]["open_weather_map"],
                                        configuration_data["Local_storage"]["home_location"],
                                        core.skills)
        self.light_system: LightController = LightController(core)


class Users:
    def __init__(self, core: Core) -> None:
        self.core: Core = core
        self.database_connection = core.data_base.user_interface

    def get_user_list(self) -> list:
        return self.database_connection.get_users()

    def add_user(self, alias: str, first_name: str, last_name: str, birthday: dict, messenger_id: int,
                 song_id: int = 1) -> None:
        self.database_connection.add_user(alias, first_name, last_name, birthday, messenger_id, song_id)

    def get_user_by_name(self, name: str) -> dict:
        return self.database_connection.get_user(name)

    def get_user_by_id(self, user_id: int) -> dict:
        return self.database_connection.get_user(user_id)

    def get_user_by_messenger_id(self, messenger_id: int) -> dict:
        return self.database_connection.get_user_by_messenger_id(messenger_id)


def start(conf_dat: dict) -> None:
    """with open(relPath + "config.json", "r") as config_file:
        config_data = json.load(config_file)
    if not config_data["established"]:
        from setup.setup_wizard import FirstStart
        print('[WARNING] System not yet set up. Setup is started...')
        try:
            setup_wizard = FirstStart()
            setup_done = config_data = setup_wizard.run()
            config_data["established"] = True
            with open(relPath + 'config.json', 'w') as file:
                json.dump(config_data, file)
        except:
            print("[WARNING] There was a problem with the Setup-Wizard!")
            traceback.print_exc()"""

    logging.info('--------- Start System ---------\n\n')

    system_name: str = config_data['System_name']
    config_data['Local_storage']['CORE_PATH']: AnyStr = os.path.dirname(os.path.abspath(__file__))
    # clear unnecessary warnings
    modules: Modules
    analyzer: Sentence_Analyzer = Sentence_Analyzer()
    audio_output: AudioOutput = AudioOutput(voice=config_data["voice"])
    # os.system('clear')
    audio_input: AudioInput = AudioInput(audio_output.adjust_after_hot_word)
    core: Core = Core(config_data, analyzer, audio_input, audio_output, system_name)
    modules: Modules = Modules(core, core.local_storage)
    core.modules = modules
    core.local_storage['CORE_starttime']: float = time.time()
    time.sleep(1)
    # -----------Starting-----------#
    modules.start_continuous()
    audio_input.start(config_data['wakeword_sentensivity'], core.hotword_detected)
    audio_output.start()
    core.services.weather.start()
    time.sleep(0.75)

    start_telegram(core)

    web_thr: Thread = Thread(target=ws.Webserver, args=[core, ModuleWrapper(core, "", {}, False, {})])
    web_thr.daemon = True
    web_thr.start()

    logging.info('--------- DONE ---------\n\n')
    core.audio_output.say("Jarvis wurde erfolgreich gestartet!")

    # Starting the main-loop
    # main_loop(Local_storage)
    """memory_control = Thread(target=clear_momory())
    memory_control.daemon = True
    memory_control.start()"""

    while True:
        try:
            time.sleep(10)
        except Exception:
            traceback.print_exc()
            break

    stop(core)


def start_telegram(core: Core) -> None:
    if config_data['messenger']:
        logging.info('[ACTION] Start Telegram...')
        if config_data['messenger_key'] == '':
            logging.error('[INFO] No Telegram-Bot-Token entered!')
        else:
            from resources.messenger import TelegramInterface

            core.messenger = TelegramInterface(config_data['messenger_key'], core)
            core.messenger.start()
            tgt: Thread = Thread(target=core.messenger_thread)
            tgt.daemon = True
            tgt.start()


def reload(core: Core) -> None:
    logging.info('[ACTION] Reload System...\n')
    time.sleep(0.3)
    with open(relPath + "config.json", "r") as config_file:
        logging.info('[INFO] loading configs...')
        core.config_data = json.load(config_file)
        core.local_storage = core.config_data["Local_storage"]

    with open(relPath + "resources/alias/correct_output.json") as correct_output:
        # dont log loading file, because it is a config too
        core.config_data["correct_output"]: dict = json.load(correct_output)

    time.sleep(0.3)
    if core.messenger is None:
        logging.info('[INFO] Load Telegram-API')
        start_telegram(core)

    time.sleep(0.3)
    logging.info('[ACTION] Reload modules')
    core.modules.load_modules()

    """logging.info('Stop Audio-Devices')
    core.Audio_Input.stop()
    core.Audio_Output.stop()"""

    """time.sleep(1)
    logging.info('Start Audio-Devices')
    core.Audio_Input.start()
    core.Audio_Output.start()"""

    time.sleep(0.3)
    logging.info('[ACTION] Reload Analyzer')
    core.analyzer = Sentence_Analyzer()

    time.sleep(0.9)
    logging.info('[INFO] System reloaded successfully!')
    """if webThr is not None:
        if not webThr.is_alive():
            webThr = Thread(target=ws.Webserver, args=[core])
            webThr.daemon = True
            webThr.start()"""

    """stop(core)
    with open(relPath + "config.json", "r") as reload_file:
        reload_dat = json.load(reload_file)
    start(reload_dat)"""


def stop(core: Core) -> None:
    logging.info('[ACTION] Stop System...')
    core.local_storage["users"]: dict = {}
    core.local_storage["rejected_messenger_messages"]: list = []
    config_data["Local_storage"]: dict = core.local_storage
    core.modules.stop_continuous()
    core.audio_input.stop()
    core.audio_output.stop()
    logging.info('\n[{}] Goodbye!\n'.format(config_data['System_name'].upper()))

    # with open(str(Path(__file__).parent) + '/config.json', 'w') as file:
    #    json.dump(config_data, file, indent=4)


global config_data
global relPath
