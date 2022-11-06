from __future__ import annotations  # compatibility for < 3.10

import datetime
import time
from pathlib import Path
from threading import Thread
from typing import TYPE_CHECKING

import requests
import toml

from src import log
from src.audio import AudioOutput, AudioInput
from src.database.connection import *
from src.models import User
from src.modules.analyze import Sentence_Analyzer

# from .resources.intent.Wrapper import IntentWrapper as AIWrapper
from src.modules.modules import Modules
from src.services import ServiceWrapper

if TYPE_CHECKING:
    from src.models import Routine


class Core:
    __instance = None

    @staticmethod
    def get_instance() -> Core:
        if Core.__instance is None:
            Core()
        return Core.__instance

    def __init__(self) -> None:
        self.__configure_logger()

        if Core.__instance is not None:
            raise Exception("Singleton cannot be instantiated more than once!")
        self.relPath = Path(__file__).parent
        self.local_storage: dict = {}
        self.config_data: dict = {}
        self.__load_config_data()
        self.use_ai = self.config_data["services"]["activation"]["ai"]
        self.path: Path = Path(__file__).parent
        self.modules: Modules = Modules.get_instance(self)  # todo
        self.analyzer: Sentence_Analyzer = Sentence_Analyzer()
        self.services: ServiceWrapper = ServiceWrapper(self, self.config_data)
        self.messenger = None
        self.messenger_queued_users: list = []
        self.messenger_queue_output: dict = {}

        self.audio_output: AudioOutput = AudioOutput()
        self.audio_input: AudioInput = AudioInput(self)

        self.active_modules: dict = {}
        self.continuous_modules: dict = {}
        self.system_name: str = self.config_data["system_name"]

        # self.ai: AIWrapper = AIWrapper()

        self.__prepare_local_storage()

        self.__start_audio()

        self.audio_output.say("Jarvis wurde erfolgreich gestartet!")

        Core.__instance = self

    def __prepare_local_storage(self):
        self.local_storage["modules"] = {}
        if (
            self.local_storage["home_location"] == ""
            and self.local_storage["HasInternetConnection"]
        ):
            self.local_storage["home_location"] = requests.get(
                "https://ipinfo.io"
            ).json()["city"]

    def __configure_logger(self) -> None:
        pass

    def __start_audio(self) -> None:
        self.audio_input.start()
        self.audio_output.start()

    def __load_config_data(self):
        with open(
            Path(__file__).parent.absolute().joinpath("config.toml").absolute(), "r"
        ) as config_file:
            log.info("loading configs...")
            self.config_data = toml.load(config_file)
            self.local_storage = self.config_data["local_storage"]

        self.local_storage["HasInternetConnection"] = False  # todo

    def messenger_thread(self) -> None:
        while True:
            for msg in self.messenger.messages.copy():
                user: User = UserInterface().get_user_by_alias(
                    msg["from"]["first_name"].lower()
                )
                if not user:
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
                self.messenger.messages.remove(msg)
            time.sleep(0.5)

    def __reject_message(self, msg):
        # toDo
        # messenger_interface.add_rejected_message(msg)
        self.__log_message_from_unknown_user(msg)
        self.messenger.say(
            "Entschuldigung, aber ich darf leider zur Zeit nicht mit Fremden reden.",
            msg["from"]["id"],
            msg["text"],
        )
        self.messenger.messages.remove(msg)

    @staticmethod
    def __log_message_from_unknown_user(msg):
        user_identification: str = (
            msg["from"]["first_name"]
            if "first_name" in msg["from"]
            else msg["from"]["id"]
        )
        log.warning(
            f"Message from unknown Telegram user {user_identification}. Access denied."
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
                log.info(f"--{user.upper()}-- (Messenger): {response['text']}")
                return response["text"]
            time.sleep(0.03)

    @staticmethod
    def webserver_action(action: str) -> str:
        if action == "mute":
            return "ok"
        else:
            return "err"

    def reload_system(self) -> None:
        raise NotImplementedError()

    def hotword_detected(self, text: str) -> None:
        user: User = UserInterface().get_user_by_alias(self.config_data["default_user"])

        matching_routines: list["Routine"] = RoutineInterface().get_all_on_command(text)
        if matching_routines:
            # TODO
            # if there are matching routines of this command, start the matching modules
            for routine in matching_routines:
                for command in routine["actions"]["commands"]:
                    for text in command["text"]:
                        self.modules.start_module(
                            user=user, text=text, name=command["module_name"]
                        )
        else:
            if not self.modules.start_module(text=str(text), user=user) and self.use_ai:
                # TODO: fix AI
                # if is_valid() functions does not found a matching module and the user wants to try with AI (use_ai),
                # start AI

                # response: str | dict = self.ai.proceed_with_user_input(text)
                # if response is None:
                #     # if the AI has not found a matching module, try to find one via is_valid()
                #     self.modules.start_module(text=str(text), user=user)
                # elif type(response) is str:
                #     self.audio_output.say(response)
                # elif type(response) is dict:
                #     self.start_module(text, response["module"], user=user)
                # else:
                #     raise ValueError('Invalid type of attribute "text"!')
                log.warning("AI is not working at the moment!")

    def start_module(self, text: str, name: str, user: dict = None) -> bool:
        # user prediction is not implemented yet, therefore here the workaround
        if user is None:
            user: str = self.local_storage["user"]
        return self.modules.query_threaded(
            name,
            text,
            User(
                alias=user,
                first_name="",
                last_name="",
                birthday=datetime.date(2020, 1, 1),
                messenger_id=1,
                song_name="standard.wav",
                waiting_notifications=[],
            ),
        )


global config_data
global relPath
