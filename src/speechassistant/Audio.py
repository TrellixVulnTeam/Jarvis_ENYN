import logging
import pathlib
import struct
import time
import traceback
from datetime import datetime
from io import BytesIO
from typing import Any

import pvporcupine
import simpleaudio as sa
import speech_recognition as sr
import toml
from pvporcupine import Porcupine
from pyaudio import PyAudio, Stream

from src.speechassistant.models.audio.QueueItem import QueueItem, QueueType, AudioQueryType, MusicQueueItem
from src.speechassistant.resources.tts import TTS


def play_audio_bytes(item: QueueItem) -> None:
    if type(item.value) != BytesIO:
        raise ValueError()
    audio = sa.play_buffer(item.value, 2, 2, item.sample_rate)
    play_obj = audio.play()
    if item.wait_until_done:
        play_obj.wait_done()


class AudioInput:

    def __init__(self) -> None:
        self.speech_engine: sr.Recognizer = sr.Recognizer()

        self.config = self.__load_configuration()
        self.__configure_microphone()

        self.running: bool = False
        self.recording: bool = False
        self.sensitivity: float = self.config.get("sensitivity")

        logging.info("[SUCCESS] Audio Input initialized!")

    def start(self) -> None:
        logging.info("[ACTION] Starting audio input module...")
        self.running = True
        self.run()

    async def run(self) -> None:
        keywords: list[str] = self.config.get("keywords")
        # toDo: access key
        porcupine: Porcupine = pvporcupine.create(keywords, sensitivities=[self.sensitivity * len(keywords)])

        try:
            pa: PyAudio = PyAudio()
            audio_stream: Stream = self.__create_pyaudio_instance(pa, porcupine)
            self.__wait_for_calls(porcupine, audio_stream, keywords)
        except MemoryError:
            logging.error(f"[ERROR] {traceback.print_exc()}")
            porcupine.delete()
            self.start()

    def __wait_for_calls(self, porcupine: Porcupine, audio_stream: Stream, keywords: list[str]) -> None:
        logging.info("\nListening {%s}" % keywords)

        while self.running:
            input_bytes: bytes = audio_stream.read(porcupine.frame_length)
            pcm: tuple = struct.unpack_from("h" * porcupine.frame_length, input_bytes)
            keyword_index: int = porcupine.process(pcm)
            if keyword_index >= 0 and not self.recording:
                self.recording = True
                logging.info(
                    f"[ACTION] Detected {keywords[keyword_index]} at "
                    f"{datetime.now().hour}:{datetime.now().minute}"
                )
                self.__handle_input()

    def recognize_file(self, audio_file: str) -> str:
        with audio_file as source:
            audio = self.speech_engine.record(source)
            text = self.speech_engine.recognize_google(audio, language="de-DE")
            return text

    def __handle_input(self, listen: bool = False, play_bling_before_listen: bool = None) -> str:
        self.recording = True
        logging.info("[ACTION] listening for userinput")

        try:
            return self.__recognize_input()
        except Exception as e:
            logging.debug(e)
            logging.info("Text could not be translated...")
            return "Das habe ich nicht verstanden."
        finally:
            self.recording = False

    def __recognize_input(self):
        with sr.Microphone(device_index=None) as source:
            audio = self.speech_engine.listen()
            return self.__recognize_input_from_audio_data(audio)

    def __recognize_input_from_audio_data(self, audio: any):
        # toDo: audio type
        text: str = ""
        try:
            self.__translate_audio_to_text(audio)
        except sr.UnknownValueError:
            try:
                self.__adjusting()
                self.__translate_audio_to_text(audio)
            except sr.UnknownValueError:
                text = "Audio could not be recorded"
        finally:
            return text

    def __translate_audio_to_text(self, audio: any):
        text = self.speech_engine.recognize_goole(
            audio, language=self.config.get("language")
        )
        logging.info("[USER INPUT]\t" + text)

    def __signalize_to_listen(self, play_bling_before_listen: bool) -> None:
        # toDo change name
        if play_bling_before_listen or (not play_bling_before_listen and self.config.get("play_bling_before_listen")):
            self.play_bling_sound()

    def play_bling_sound(self) -> None:
        if not self.recording:
            PlayBlingSound.play()

    def __adjusting(self) -> None:
        with sr.Microphone(device_index=None) as source:
            self.speech_engine.adjust_for_ambient_noise(source)

    def py_error_handler(self, filename, line, function, err, fmt) -> None:
        # This function suppress warnings from Alsa, which are totally useless
        pass

    def stop(self) -> None:
        pass

    def __load_configuration(self) -> dict[str, any]:
        raise NotImplemented

    def __configure_microphone(self) -> None:
        with sr.Microphone(device_index=None) as source:
            self.speech_engine.pause_threshold = self.config.get("pause_threshold")
            self.speech_engine.energy_threshold = self.config.get("energy_threshold")
            self.speech_engine.dynamic_energy_threshold = self.config.get("dynamic_energy_threshold")
            self.speech_engine.dynamic_energy_adjustment_damping = self.config.get("dynamic_energy_adjustment_damping")
            self.speech_engine.adjust_for_ambient_noise(source)

    @staticmethod
    def __create_pyaudio_instance(pyaudio: PyAudio, porcupine: Porcupine) -> Stream:
        return pyaudio.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length,
        )


class PlayBlingSound:
    bling_sound: BytesIO

    def __new__(cls, *args, **kwargs):
        PlayBlingSound.__load_bling_sound()
        return cls

    @staticmethod
    def play() -> None:
        audio = sa.play_buffer(PlayBlingSound.bling_sound, 2, 2, 44100)
        audio.play()

    @staticmethod
    def __load_bling_sound() -> None:
        bling_byte_array: BytesIO = BytesIO()
        with open(PlayBlingSound.__get_path_of_bling_file(), 'r') as file:
            bling_byte_array.write(file.read())
        PlayBlingSound.bling_sound = bling_byte_array

    @staticmethod
    def __get_path_of_bling_file():
        return pathlib.Path(__file__).parent.joinpath("resources").joinpath("sounds").joinpath("bling.wav")


class AudioOutput:

    def __init__(self) -> None:
        self.configuration: dict[str, any] = self.__load_configuration()

        self.tts: TTS = TTS()

        self.queue: list[QueueItem] = list()
        self.priority_queue: list[QueueItem] = list()
        self.music_queue: list[QueueItem] = list()

        self.running: bool = False

    def start(self):
        self.running = True
        self.run()
        return self

    async def run(self) -> None:
        while self.running:
            try:
                item: QueueItem = self.__get_next_item()
                self.__choose_output_method(item)
            except IndexError:
                time.sleep(0.25)

    def __choose_output_method(self, item):
        match type(item.value):
            case str.__class__:
                self.tts.say(item.value)
            case BytesIO.__class__:
                play_audio_bytes(item.value)
            case _:
                pass

    def say(self, text: str) -> None:
        model: QueueItem = self.__build_queue_item(self.priority_queue, QueueType.TTS, text, True, 44100)
        self.__insert_to_priority_queue(model)

    def play_music(self, name: str, as_next: bool = False) -> None:
        pass

    def play_notification(self, buff: BytesIO, as_next: bool, sample_rate: int = 44100) -> None:
        model: QueueItem = self.__build_queue_item(self.priority_queue, QueueType.AUDIO, buff, as_next, sample_rate)
        self.__insert_to_priority_queue(model)

    @staticmethod
    def stop() -> None:
        sa.close()

    def __get_next_item(self) -> QueueItem:
        try:
            return self.priority_queue.pop(0)
        except IndexError:
            return self.queue.pop(0)

    def __load_configuration(self) -> dict[str, Any]:
        with open(self.__get_path_of_config_file()) as file:
            return toml.load(file)

    def __get_path_of_config_file(self) -> str:
        raise NotImplemented

    def __insert_to_queue(self, model: QueueItem) -> None:
        self.queue = self.__insert_to_given_queue(model, self.queue)

    def __insert_to_priority_queue(self, model: QueueItem) -> None:
        self.priority_queue = self.__insert_to_given_queue(model, self.priority_queue)

    @staticmethod
    def __insert_to_given_queue(model: QueueItem, queue: list) -> list:
        queue.append(model)
        # sort queue by type (ascending) and then by priority (descending)
        return sorted(queue, key=lambda x: (- x.type, x.PRIORITY))

    def __build_queue_item(self, queue, queue_type: QueueType, value: str | BytesIO, as_next: bool,
                           sample_rate: int = None,
                           wait_until_done: bool = False) -> QueueItem:
        if not sample_rate:
            sample_rate = 44100
        model: QueueItem = QueueItem(type=queue_type, value=value, wait_until_done=wait_until_done,
                                     sample_rate=sample_rate)
        if as_next:
            model.PRIORITY = self.__get_highest_priority_plus_one(queue)
        return model

    def __build_music_queue_item(self, query_type: AudioQueryType, value: str | BytesIO, as_next: bool,
                                 sample_rate: int = None) -> MusicQueueItem:
        if not sample_rate:
            sample_rate = 44100
        model: MusicQueueItem = MusicQueueItem(query_type=query_type, value=value, sample_rate=sample_rate)
        if as_next:
            model.PRIORITY = self.__get_highest_priority_plus_one(self.music_queue)
        return model

    @staticmethod
    def __get_highest_priority_plus_one(queue) -> int:
        return queue.__getitem__(1).PRIORITY + 1
