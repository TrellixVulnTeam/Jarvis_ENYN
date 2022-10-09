from __future__ import annotations

import pathlib
import struct
import time
from datetime import datetime
from io import BytesIO
from pathlib import Path
from threading import Thread
from typing import Any
from typing import TYPE_CHECKING

import pvporcupine
import speech_recognition as sr
import toml
from pvrecorder import PvRecorder
from pyaudio import PyAudio, Stream, paInt16

from src import log
from src.models.audio.queue_item import (
    QueueItem,
    QueueType,
    AudioQueryType,
    MusicQueueItem,
)
from src.resources.TTS import TTS

if TYPE_CHECKING:
    from src.core import Core


def __load_configuration() -> dict[str, Any]:
    with open(__get_path_of_config_file()) as file:
        return toml.load(file)


def __get_path_of_config_file() -> Path:
    return pathlib.Path(__file__).parent.parent.joinpath("config.toml").absolute()


config: dict[str, Any] = __load_configuration()
audio_config: dict[str, Any] = config["audio"]


def play_audio_bytes(item: QueueItem) -> None:
    if type(item.value) != BytesIO:
        raise ValueError()
    item.value.seek(0)

    stream: Stream = __create_pyaudio_stream(item)

    data = item.value.read(1024)

    while data != "":
        stream.write(data)
        data = item.value.read(1024)

    stream.stop_stream()
    stream.close()


def __create_pyaudio_stream(item):
    stream = PyAudio()
    stream = stream.open(
        rate=item.sample_rate,
        channels=1,
        format=paInt16,
        output=True,
        frames_per_buffer=1024,
    )
    stream.start_stream()
    return stream


class AudioInput:
    def __init__(self, core: "Core") -> None:
        self.__core = core
        self.speech_engine: sr.Recognizer = sr.Recognizer()

        self.config = audio_config.get("input")

        self.__configure_microphone()

        self.running: bool = False
        self.recording: bool = False
        self.sensitivity: float = self.config.get("sensitivity")

        log.info("Audio Input initialized.")

    def start(self) -> None:
        log.action("Starting audio input module...")
        self.running = True

        audio_input_thread: Thread = Thread(target=self.run, args=())
        audio_input_thread.daemon = True
        audio_input_thread.start()

        log.info("Audio Input started.")

    def run(self) -> None:
        keywords: list[str] = self.config.get("keywords")
        porcupine: pvporcupine.Porcupine = pvporcupine.create(
            keywords=keywords,
            sensitivities=[self.sensitivity],
            access_key=config["api"]["porcupine"],
        )

        try:
            # pa: PyAudio = PyAudio()
            # audio_stream: Stream = self.__create_pyaudio_instance(pa, porcupine)
            recorder = PvRecorder(
                device_index=self.config["device_index"],
                frame_length=porcupine.frame_length,
            )
            self.__wait_for_calls(porcupine, recorder, keywords)
        except MemoryError:
            log.warning("Memory is full!")
            log.action("Restart porcupine...")
            porcupine.delete()
            self.start()

    def __wait_for_calls(
        self,
        porcupine: pvporcupine.Porcupine,
        recorder: PvRecorder,
        keywords: list[str],
    ) -> None:
        log.info("Listening {%s}" % keywords)

        recorder.start()

        while self.running:
            # input_bytes: bytes = audio_stream.read(round(porcupine.frame_length / 2))
            pcm = recorder.read()
            sp = struct.pack("h" * len(pcm), *pcm)
            keyword_index: int = porcupine.process(sp)
            if keyword_index >= 0 and not self.recording:
                self.recording = True
                log.info(
                    f"Detected {keywords[keyword_index]} at "
                    f"{datetime.now().hour}:{datetime.now().minute}"
                )
                self.__core.hotword_detected(self.recognize_input())

    def recognize_file(self, audio_file: any) -> str:
        with audio_file as source:
            audio = self.speech_engine.record(source)
            text = self.speech_engine.recognize_google(audio, language="de-DE")
            return text

    def recognize_input(self, play_bling_before_listen: bool = None) -> str:
        self.recording = True
        log.action("Listening for userinput...")

        self.__signalize_to_listen(play_bling_before_listen)

        try:
            return self.record_input_and_recognize()
        except Exception as e:
            log.debug(e)
            log.warning("Text could not be translated...")
            return "Das habe ich nicht verstanden."
        finally:
            self.recording = False

    def record_input_and_recognize(self):
        with sr.Microphone(device_index=None) as source:
            audio = self.speech_engine.listen(source)
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
        log.info("[USER INPUT]\t" + text)

    def __signalize_to_listen(self, play_bling_before_listen: bool = None) -> None:
        # toDo change name
        if play_bling_before_listen or (
            not play_bling_before_listen and self.config.get("play_bling_before_listen")
        ):
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

    def __configure_microphone(self) -> None:
        with sr.Microphone(device_index=None) as source:
            self.speech_engine.pause_threshold = self.config.get("pause_threshold")
            self.speech_engine.energy_threshold = self.config.get("energy_threshold")
            self.speech_engine.dynamic_energy_threshold = self.config.get(
                "dynamic_energy_threshold"
            )
            self.speech_engine.dynamic_energy_adjustment_damping = self.config.get(
                "dynamic_energy_adjustment_damping"
            )
            self.speech_engine.adjust_for_ambient_noise(source)

    @staticmethod
    def __create_pyaudio_instance(
        pyaudio_object: PyAudio, porcupine: pvporcupine.Porcupine
    ) -> Stream:
        return pyaudio_object.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=paInt16,
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
        item: QueueItem = QueueItem(
            value=PlayBlingSound.bling_sound.read(), type=QueueType.EFFECT
        )
        play_audio_bytes(item)

    @staticmethod
    def __load_bling_sound() -> None:
        bling_byte_array: BytesIO = BytesIO()
        with open(PlayBlingSound.__get_path_of_bling_file(), "r") as file:
            bling_byte_array.write(file.read())
        PlayBlingSound.bling_sound = bling_byte_array

    @staticmethod
    def __get_path_of_bling_file():
        return (
            pathlib.Path(__file__)
            .parent.joinpath("resources")
            .joinpath("sounds")
            .joinpath("bling.wav")
        )


class AudioOutput:
    def __init__(self) -> None:
        self.tts: TTS = TTS(play_audio_bytes)

        self.config = audio_config.get("output")

        self.queue: list[QueueItem] = list()
        self.priority_queue: list[QueueItem] = list()
        self.music_queue: list[QueueItem] = list()

        self.running: bool = False

    def start(self):
        log.action("Starting Audio Output....")

        self.running = True

        audio_output_thread: Thread = Thread(target=self.run, args=())
        audio_output_thread.daemon = True
        audio_output_thread.start()

        log.info("Audio Output started!")
        return self

    def run(self) -> None:
        while self.running:
            item: QueueItem = self.__get_next_item()
            if item is not None:
                print(f"-------->Next Item: {item}<-------")
                self.__choose_output_method(item)
            else:
                time.sleep(0.25)

    def __choose_output_method(self, item) -> None:
        match type(item.value).__class__:
            case str.__class__:
                self.tts.say(item.value)
            case BytesIO.__class__:
                play_audio_bytes(item.value)
            case _:
                pass

    def say(self, text: str) -> None:
        model: QueueItem = build_queue_item(
            self.priority_queue, QueueType.TTS, text, True, 44100
        )
        self.__insert_to_priority_queue(model)

    def play_music_from_name(
        self, name: str, as_next: bool = False, announce: bool = False
    ) -> None:
        pass

    def play_music_from_url(
        self, url: str, as_next: bool = False, announce: bool = False
    ) -> None:
        pass

    def play_music_from_bytes(
        self,
        buff: BytesIO,
        as_next: bool = False,
        sample_rate: int = 44100,
        announce: bool = False,
    ) -> None:
        pass

    def play(
        self,
        queue_type: QueueType,
        buff: BytesIO,
        as_next: bool,
        sample_rate: int = 44100,
    ) -> None:
        model: QueueItem = build_queue_item(
            self.priority_queue, QueueType.AUDIO, buff, as_next, sample_rate
        )

        match queue_type:
            case QueueType.EFFECT:
                play_audio_bytes(model)
            case QueueType.NOTIFICATION:
                self.__insert_to_priority_queue(model)
            case QueueType.AUDIO:
                self.__insert_to_queue(model)
            case QueueType.MUSIC:
                self.play_music_from_bytes(buff, as_next, sample_rate)

    @staticmethod
    def stop() -> None:
        pass

    def __get_next_item(self) -> QueueItem | None:
        if len(self.priority_queue) > 0:
            return self.priority_queue.pop(0)
        elif len(self.queue) > 0:
            return self.queue.pop(0)
        else:
            return None

    def __insert_to_queue(self, model: QueueItem) -> None:
        self.queue = self.__insert_to_given_queue(model, self.queue)

    def __insert_to_priority_queue(self, model: QueueItem) -> None:
        self.priority_queue = self.__insert_to_given_queue(model, self.priority_queue)

    @staticmethod
    def __insert_to_given_queue(model: QueueItem, queue: list) -> list:
        queue.append(model)
        # sort queue by type (ascending) and then by priority (descending)
        return sorted(queue, key=lambda x: (-x.queue_type.value, x.PRIORITY))

    def __build_music_queue_item(
        self,
        query_type: AudioQueryType,
        value: str | BytesIO,
        as_next: bool,
        sample_rate: int = None,
    ) -> MusicQueueItem:
        if not sample_rate:
            sample_rate = 44100
        model: MusicQueueItem = MusicQueueItem(
            query_type=query_type, value=value, sample_rate=sample_rate
        )
        if as_next:
            model.PRIORITY = get_highest_priority_plus_one(self.music_queue)
        return model


def build_queue_item(
    queue,
    queue_type: QueueType,
    value: str | BytesIO,
    as_next: bool,
    sample_rate: int = None,
    wait_until_done: bool = False,
) -> QueueItem:
    if not sample_rate:
        sample_rate = 44100
    model: QueueItem = QueueItem(
        queue_type=queue_type,
        value=value,
        wait_until_done=wait_until_done,
        sample_rate=sample_rate,
    )
    if as_next:
        model.PRIORITY = get_highest_priority_plus_one(queue)
    return model


def get_highest_priority_plus_one(queue) -> int:
    try:
        return queue.__getitem__(0).PRIORITY + 1
    except IndexError:
        return 1
