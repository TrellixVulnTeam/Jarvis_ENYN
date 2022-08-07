from __future__ import annotations  # compatibility for < 3.10

import json
import logging
import time
from pathlib import Path
from threading import Thread

import requests

from src.speechassistant.Audio import AudioOutput, AudioInput
from src.speechassistant.Modules import Modules
from src.speechassistant.Services import ServiceWrapper
from src.speechassistant.Users import Users
from src.speechassistant.database.database_connection import DataBase
from src.speechassistant.models.user import User
from src.speechassistant.resources.analyze import Sentence_Analyzer
# from resources.intent.Wrapper import IntentWrapper as AIWrapper
from src.speechassistant.resources.module_skills import Skills


class Core:
    __instance = None

    @staticmethod
    def get_instance() -> Core:
        if Core.__instance is None:
            Core()
        return Core.__instance

    def __init__(self) -> None:
        if Core.__instance is not None:
            raise Exception("Singleton cannot be instantiated more than once!")
        self.relPath = str(Path(__file__).parent) + "/"
        self.local_storage: dict = {}
        self.config_data: dict = {}
        self.__load_config_data()
        self.use_ai = self.config_data["ai"]
        self.path: str = str(Path(__file__).parent) + "/"
        self.data: dict = self.config_data
        self.__fill_data()  # since the path is needed, __fill_data() is called only here
        self.modules: Modules = None
        self.analyzer: Sentence_Analyzer = Sentence_Analyzer()
        self.skills: Skills = Skills()
        self.data_base = DataBase()
        self.services: ServiceWrapper = ServiceWrapper(self, self.data)
        self.messenger = None
        self.messenger_queued_users: list = []
        self.messenger_queue_output: dict = {}

        self.users: Users = Users()

        self.audio_output: AudioOutput = AudioOutput.get_instance()
        self.audio_input: AudioInput = AudioInput.get_instance()

        self.active_modules: dict = {}
        self.continuous_modules: dict = {}
        self.system_name: str = self.config_data["system_name"]

        # self.ai: AIWrapper = AIWrapper()

        if self.local_storage["home_location"] == "":
            self.local_storage["home_location"] = requests.get(
                "https://ipinfo.io"
            ).json()["city"]

        Core.__instance = self

    def __fill_data(self) -> None:
        with open(self.relPath + "/data/api_keys.dat") as api_file:
            self.data["api_keys"] = json.load(api_file)

    def __load_config_data(self):
        with open(self.relPath + "config.json", "r") as config_file:
            logging.info("[INFO] loading configs...")
            self.config_data = json.load(config_file)
            self.local_storage = self.config_data["Local_storage"]

    def messenger_thread(self) -> None:
        # Verarbeitet eingehende Telegram-Nachrichten, weist ihnen Nutzer zu etc.
        while True:
            for msg in self.messenger.messages.copy():
                try:
                    user: User = self.users.get_user_by_name(
                        msg["from"]["first_name"].lower()
                    )
                except KeyError:
                    self.__reject_message(msg)
                    continue

                if msg["text"].lower().startswith("Jarvis"):
                    self.modules.start_module(
                        text=msg["text"], user=user, messenger=True
                    )
                elif msg["from"]["first_name"].lower() in self.messenger_queued_users:
                    self.messenger_queue_output[msg["from"]["first_name"].lower()] = msg
                else:
                    th: Thread = Thread(
                        target=self.modules.start_module,
                        args=(
                            user,
                            msg["text"],
                            None,
                            True,
                        ),
                    )
                    th.daemon = True
                    th.start()
                """if response == False: self.messenger.say('Das habe ich leider nicht verstanden.', 
                self.users.get_user_by_name(user)['messenger_id']) """
                self.messenger.messages.remove(msg)
            time.sleep(0.5)

    def __reject_message(self, msg):
        self.data_base.messenger_interface.add_rejected_message(msg)
        self.__log_message_from_unknown_user(msg)
        self.messenger.say(
            "Entschuldigung, aber ich darf leider zur Zeit nicht mit Fremden reden.",
            msg["from"]["id"],
            msg["text"],
        )
        self.messenger.messages.remove(msg)

    def __log_message_from_unknown_user(self, msg):
        try:
            logging.warning(
                "[WARNING] Message from unknown Telegram user {}. Access denied.".format(
                    msg["from"]["first_name"]
                )
            )
        except KeyError:
            logging.warning(
                "[WARNING] Message from unknown Telegram user {}. Access denied.".format(
                    msg["from"]["id"]
                )
            )

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
                logging.info(
                    "[ACTION] --{}-- (Messenger): {}".format(
                        user.upper(), response["text"]
                    )
                )
                return response["text"]
            time.sleep(0.03)

    @staticmethod
    def webserver_action(action: str) -> str:
        if action == "mute":
            return "ok"
        else:
            return "err"

    def reload_system(self) -> None:
        # reload(self)
        pass

    def hotword_detected(self, text: str) -> None:
        user: User = self.users.get_user_by_name(self.local_storage["user"])

        matching_routines: list[dict] = self.data_base.routine_interface.get_routines(
            on_command=text
        )
        if matching_routines:
            # if there are matching routines of this command, start the matching modules
            for routine in matching_routines:
                for command in routine["actions"]["commands"]:
                    for text in command["text"]:
                        self.modules.start_module(
                            user=user, text=text, name=command["module_name"]
                        )
        else:
            if not self.modules.start_module(text=str(text), user=user) and self.use_ai:
                # if isValid() functions does not found a matching module and the user wants to try with AI (use_ai),
                # start AI

                # response: str | dict = self.ai.proceed_with_user_input(text)
                # if response is None:
                #     # if the AI has not found a matching module, try to find one via isValid()
                #     self.modules.start_module(text=str(text), user=user)
                # elif type(response) is str:
                #     self.audio_output.say(response)
                # elif type(response) is dict:
                #     self.start_module(text, response["module"], user=user)
                # else:
                #     raise ValueError('Invalid type of attribute "text"!')
                print("AI not working at the moment!")

    def start_module(self, text: str, name: str, user: dict = None) -> bool:
        # user prediction is not implemented yet, therefore here the workaround
        if user is None:
            user: dict = self.local_storage["user"]
        return self.modules.query_threaded(name, text, user)


def start() -> None:
    core: Core = Core.get_instance()


# def start() -> None:
# """with open(relPath + "config.json", "r") as config_file:
#    config_data = json.load(config_file)
# if not config_data["established"]:
#    from setup.setup_wizard import FirstStart
#    print('[WARNING] System not yet set up. Setup is started...')
#    try:
#        setup_wizard = FirstStart()
#        setup_done = config_data = setup_wizard.run()
#        config_data["established"] = True
#        with open(relPath + 'config.json', 'w') as file:
#            json.dump(config_data, file)
#    except:
#        print("[WARNING] There was a problem with the Setup-Wizard!")
#        traceback.print_exc()"""

# logging.info('--------- Start System ---------\n\n')

# system_name: str = config_data['System_name']
# config_data['Local_storage']['CORE_PATH']: AnyStr = os.path.dirname(os.path.abspath(__file__))
## clear unnecessary warnings
# modules: Modules
# analyzer: Sentence_Analyzer = Sentence_Analyzer()
# audio_output: AudioOutput = AudioOutput(voice=config_data["voice"])
## os.system('clear')
# audio_input: AudioInput = AudioInput(audio_output.adjust_after_hot_word)
# core: Core = Core(config_data, analyzer, audio_input, audio_output, system_name)
# modules: Modules = Modules(core, core.local_storage)
# core.modules = modules
# core.local_storage['CORE_starttime']: float = time.time()
# time.sleep(1)
## -----------Starting-----------#
# modules.start_continuous()
# audio_input.start(config_data['wakeword_sentensivity'], core.hotword_detected)
# audio_output.start()
# core.routers.weather.start()
# time.sleep(0.75)

# start_telegram(core)

# web_thr: Thread = Thread(target=ws.Webserver, args=[core, ModuleWrapper(core, "", {}, False, {})])
# web_thr.daemon = True
# web_thr.start()

# logging.info('--------- DONE ---------\n\n')
# core.audio_output.say("Jarvis wurde erfolgreich gestartet!")

## Starting the main-loop
## main_loop(Local_storage)
# """memory_control = Thread(target=clear_momory())
# memory_control.daemon = True
# memory_control.start()"""

# while True:
#    try:
#        time.sleep(10)
#    except Exception:
#        traceback.print_exc()
#        break

# stop(core)


# def start_telegram(core: Core) -> None:
# if config_data['messenger']:
#    logging.info('[ACTION] Start Telegram...')
#    if config_data['messenger_key'] == '':
#        logging.error('[INFO] No Telegram-Bot-Token entered!')
#    else:
#        from resources.messenger import TelegramInterface

# core.messenger = TelegramInterface(config_data['messenger_key'], core)
# core.messenger.start()
# tgt: Thread = Thread(target=core.messenger_thread)
# tgt.daemon = True
# tgt.start()


# def reload(core: Core) -> None:
# logging.info('[ACTION] Reload System...\n')
# time.sleep(0.3)
# with open(relPath + "config.json", "r") as config_file:
#    logging.info('[INFO] loading configs...')
#    core.config_data = json.load(config_file)
#    core.local_storage = core.config_data["Local_storage"]

# with open(relPath + "resources/alias/correct_output.json") as correct_output:
#    # dont log loading file, because it is a config too
#    core.config_data["correct_output"]: dict = json.load(correct_output)

# time.sleep(0.3)
# if core.messenger is None:
# logging.info('[INFO] Load Telegram-API')
# start_telegram(core)

# time.sleep(0.3)
# logging.info('[ACTION] Reload modules')
# core.modules.load_modules()

# """logging.info('Stop Audio-Devices')
# core.Audio_Input.stop()
# core.Audio_Output.stop()"""

# """time.sleep(1)
# logging.info('Start Audio-Devices')
# core.Audio_Input.start()
# core.Audio_Output.start()"""

# time.sleep(0.3)
# logging.info('[ACTION] Reload Analyzer')
# core.analyzer = Sentence_Analyzer()

# time.sleep(0.9)
# logging.info('[INFO] System reloaded successfully!')
# """if webThr is not None:
#    if not webThr.is_alive():
#        webThr = Thread(target=ws.Webserver, args=[core])
#        webThr.daemon = True
#        webThr.start()"""

# """stop(core)
# with open(relPath + "config.json", "r") as reload_file:
#    reload_dat = json.load(reload_file)
# start(reload_dat)"""


# def stop(core: Core) -> None:
# logging.info('[ACTION] Stop System...')
# core.local_storage["users"]: dict = {}
# config_data["Local_storage"]: dict = core.local_storage
# core.modules.stop_continuous()
# core.audio_input.stop()
# core.audio_output.stop()
# logging.info('\n[{}] Goodbye!\n'.format(config_data['System_name'].upper()))

## with open(str(Path(__file__).parent) + '/config.json', 'w') as file:
##    json.dump(config_data, file, indent=4)


global config_data
global relPath
