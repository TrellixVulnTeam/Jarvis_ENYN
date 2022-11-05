from io import BytesIO
from pathlib import Path
from threading import Thread
from typing import TYPE_CHECKING

from src import log
from src.models import AudioQueryType, MusicQueueItem, QueueType, QueueItem
from .utils import get_highest_priority_plus_one, build_queue_item

if TYPE_CHECKING:
    from src.core import Core


def __get_path_of_config_file() -> Path:
    return Path(__file__).parent.parent.joinpath("config.toml").absolute()


def play_audio_bytes(item: QueueItem) -> None:
    if type(item.value) != BytesIO:
        raise ValueError()
    print("Playing some audio")


class AudioInput:
    def __init__(self, core: "Core") -> None:
        self.__core = core

        self.running: bool = False
        self.recording: bool = False

        log.info("Audio Input initialized.")

    def start(self) -> None:
        log.action("Starting audio input module...")
        self.running = True

        audio_input_thread: Thread = Thread(target=self.run, args=())
        audio_input_thread.daemon = True
        audio_input_thread.start()

        log.info("Audio Input started.")

    def run(self) -> None:
        try:
            self.__wait_for_calls()
        except MemoryError:
            log.warning("Memory is full!")
            log.action("Restart porcupine...")
            self.start()

    def __wait_for_calls(self) -> None:
        log.info("Listening...")
        # self.__core.hotword_detected(input("Please enter something: "))

    def py_error_handler(self, filename, line, function, err, fmt) -> None:
        # This function suppress warnings from Alsa, which are totally useless
        pass

    def stop(self) -> None:
        pass


class AudioOutput:
    def __init__(self) -> None:
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
            try:
                item: QueueItem = self.__get_next_item()
                print(f"-------->Next Item: {item}<-------")
                self.__choose_output_method(item)
            except IndexError:
                import time

                time.sleep(0.25)

    @staticmethod
    def __choose_output_method(item):
        match type(item.value).__class__:
            case str.__class__:
                print("JARVIS -> " + item.value)
            case BytesIO.__class__:
                print("Playing audio...")
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

    def __get_next_item(self) -> QueueItem:
        try:
            return self.priority_queue.pop(0)
        except IndexError:
            return self.queue.pop(0)

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
