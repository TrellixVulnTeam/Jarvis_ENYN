from __future__ import annotations

import io
import json
import logging
import random
from pathlib import Path
from random import random
from typing import AnyStr, Any
from urllib.request import Request, urlopen

from src.audio import AudioOutput, AudioInput
from src.models.audio.queue_item import QueueType
from src.models.user import User
from src.modules.module_skills import Skills
from src.resources.analyze import Sentence_Analyzer


class ModuleWrapper:
    def __init__(self, text: str, analysis: dict, messenger: bool, user: User) -> None:
        self.text: str = text
        self.analysis: dict = analysis
        # toDo: down below
        # self.analysis['town'] = core.local_storage['home_location'] if self.analysis['town'] is None else None

        from src.core import Core

        self.core: Core = Core.get_instance()

        self.audio_output: AudioOutput = self.core.audio_output
        self.audio_input: AudioInput = self.core.audio_input

        self.messenger_call: bool = messenger

        self.room: str = "messenger" if messenger else "raum"  # toDo when enabling rooms
        self.messenger = self.core.messenger

        self.skills: Skills = Skills()

        self.Analyzer: Sentence_Analyzer = self.core.analyzer

        self.local_storage: dict = self.core.local_storage
        self.system_name: str = self.core.system_name
        self.path: Path = self.core.path
        self.user: User = user

    def say(self, text: str | list, output: str = "auto") -> None:
        if type(text) is list:
            text = random.choice(text)
        text: str = self.speech_variation(text)

        if output == "messenger" or (self.__output_auto_and_messanger_call(output)):
            self.messenger_say(text)
        elif output == "text":
            text = self.correct_output_automate(text)
            self.audio_output.say(text)

    def __output_auto_and_messanger_call(self, output):
        return output == "auto" and self.messenger_call

    def messenger_say(self, text: str) -> None:
        try:
            self.messenger.say(text, self.user.messenger_id)
        except KeyError:
            logging.info(
                f'[WARNING] Sending message "{text}" to messenger failed, because there is no Messenger-ID for this '
                f'user ({self.user.alias}) '
            )
        except AttributeError:
            logging.info("[WARNING] Sending message to messenger failed, because there is no key for it!")
        return

    def play(
            self,
            path: str = None,
            audio_bytes: io.BytesIO = None,
            as_next: bool = False,
            notification: bool = False,
    ) -> None:
        data: io.BytesIO | None = None

        if path:
            with open(path, "rb") as wav_file:
                input_wav: AnyStr = wav_file.read()
                data = io.BytesIO(input_wav)
        elif audio_bytes:
            data = audio_bytes

        if notification:
            self.audio_output.play(QueueType.NOTIFICATION, data, as_next)
        else:
            self.audio_output.play(QueueType.AUDIO, data, as_next)

    def play_music_from_name(self, name: str, as_next: bool = False, announce: bool = False) -> None:
        self.audio_output.play_music_from_name(name, as_next, announce)

    def play_music_from_url(self, url: str, as_next: bool = False, announce: bool = False) -> None:
        self.audio_output.play_music_from_url(url, as_next, announce)

    def play_music_from_bytes(self, buff: io.BytesIO, as_next: bool = False, sample_rate: int = 44100,
                              announce: bool = False) -> None:
        self.audio_output.play_music_from_bytes(buff, as_next, sample_rate, announce)

    def listen(self, text: str = None, messenger: bool = None, play_sound: bool = False) -> str:
        if text:
            self.say(text)

        messenger = self.messenger_call if messenger is None else messenger
        if messenger:
            return self.core.messenger_listen(self.user.first_name.lower())
        else:
            return self.audio_input.recognize_input(play_bling_before_listen=play_sound)

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
        request = Request(
            "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl="
            + target_lang
            + "&dt=t&q="
            + text
        )
        response = urlopen(request)
        answer = json.loads(response.read())
        return answer[0][0][0]

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
        self.audio_input.start()

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
        self.services = core.servicesf
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
