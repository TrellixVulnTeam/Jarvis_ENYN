from __future__ import annotations

import io
import json
import logging
import random
import urllib
from random import random
from typing import AnyStr, Any
from urllib.request import Request, urlopen

from src.speechassistant.Audio import AudioOutput, AudioInput
from src.speechassistant.database.database_connection import DataBase
from src.speechassistant.models.user import User
from src.speechassistant.resources.analyze import Sentence_Analyzer
from src.speechassistant.resources.module_skills import Skills


class ModuleWrapper:
    def __init__(self, text: str, analysis: dict, messenger: bool, user: User) -> None:
        self.text: str = text
        self.analysis: dict = analysis
        # toDo: down below
        # self.analysis['town'] = core.local_storage['home_location'] if self.analysis['town'] is None else None

        from core import Core

        self.core: Core = Core.get_instance()

        self.audio_output: AudioOutput = AudioOutput.get_instance()
        self.audio_input: AudioInput = AudioInput.get_instance()

        self.messenger_call: bool = messenger

        self.room: str = "messenger" if messenger else "raum"
        self.messenger = self.core.messenger

        self.skills: Skills = Skills()
        self.data_base = DataBase()

        self.Analyzer: Sentence_Analyzer = self.core.analyzer

        self.local_storage: dict = self.core.local_storage
        self.system_name: str = self.core.system_name
        self.path: str = self.core.path
        self.user: User = user

    def say(self, text: str | list, output: str = "auto") -> None:
        if type(text) is list:
            text = random.choice(text)
        text: str = self.speech_variation(text)
        if output == "auto":
            if self.messenger_call:
                output = "messenger"
        if "messenger" in output.lower() or self.messenger_call:
            self.messenger_say(text)
        else:
            text = self.correct_output_automate(text)
            self.audio_output.say(text)

    def messenger_say(self, text: str) -> None:
        try:
            self.messenger.say(text, self.user.messenger_id)
        except KeyError:
            logging.warning(
                '[WARNING] Sending message "{}" to messenger failed, because there is no Telegram-ID for this user '
                "({}) ".format(text, self.user.alias)
            )
        except AttributeError:
            logging.info(
                "[WARNING] Sending message to messenger failed,  because there is no key for it!"
            )
        return

    def play(
            self,
            path: str = None,
            audiofile: str = None,
            as_next: bool = False,
            notification: bool = False,
    ) -> None:
        if path is not None:
            with open(path, "rb") as wav_file:
                input_wav: AnyStr = wav_file.read()
        if audiofile is not None:
            with open(audiofile, "rb"):
                input_wav: AnyStr = wav_file.read()
        data: io.BytesIO = io.BytesIO(input_wav)
        if notification:
            self.audio_output.play_notification(data, as_next)
        else:
            self.audio_output.play_playback(data, as_next)

    def play_music(
            self,
            by_name: str = None,
            url: str = None,
            path: str = None,
            as_next: bool = False,
            now: bool = False,
            playlist: bool = False,
            announce: bool = False,
    ) -> None:
        if by_name is not None:
            by_name = "'" + by_name + "'"
        # simply forward information
        self.audio_output.music_player.play(
            by_name=by_name,
            url=url,
            path=path,
            as_next=as_next,
            now=now,
            playlist=playlist,
            announce=announce,
        )

    def listen(
            self, text: str = None, messenger: bool = None, play_sound: bool = False
    ) -> str:
        if messenger is None:
            messenger: bool = self.messenger_call
        if text is not None:
            self.say(text)
        if messenger:
            return self.core.messenger_listen(self.user["first_name"].lower())
        else:
            return self.audio_input.recognize_input(
                self.core.hotword_detected,
                listen=True,
                play_bling_before_listen=play_sound,
            )

    def recognize(self, audio_file: Any) -> str:
        return self.audio_input.recognize_file(audio_file)

    @staticmethod
    def words_in_text(words: list, text: str) -> bool:
        for word in words:
            if word not in text:
                return False
        return True

    def start_module(
            self, name: str = None, text: str = None, user: dict = None
    ) -> None:
        self.core.start_module(text, name, user)

    def start_module_and_confirm(
            self, name: str = None, text: str = None, user: dict = None
    ) -> bool:
        return self.core.start_module(text, name, user)

    def module_storage(self, module_name=None):
        module_storage = self.core.local_storage.get("module_storage")
        if module_name is None:
            return module_storage
        # I am now just so free and lazy and assume that a module name is passed from a module that actually exists.
        else:
            return module_storage[module_name]

    @staticmethod
    def translate(text, target_lang="de"):
        try:
            request = Request(
                "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl="
                + urllib.parse.quote(target_lang)
                + "&dt=t&q="
                + urllib.parse.quote(text)
            )
            response = urlopen(request)
            answer = json.loads(response.read())
            return answer[0][0][0]
        except Exception:
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
        self.audio_input.start(
            self.local_storage["wakeword_sentensivity"], self.core.hotword_detected
        )

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


def translate(text, target_lang="de"):
    return ModuleWrapper.translate(text, target_lang)


class ModuleWrapperContinuous:
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
        self.data_base: DataBase = core.data_base
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
