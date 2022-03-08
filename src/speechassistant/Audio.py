from __future__ import annotations  # compatibility for < 3.10

import io
import logging
import os
import random
import re
import struct
import time
import traceback
import urllib.request
from datetime import datetime
from threading import Thread
from typing import IO, Callable


import pafy
import pvporcupine
import pyaudio
import speech_recognition as sr
import vlc
from pygame import mixer as mixer

from src.speechassistant.resources.tts import TTS


class AudioInput:
    """
    -------------------------
    AudioInput:
        - responsible for the whole audio input
    -------------------------
    """

    def __init__(self, _adjust_after_hot_word: Callable) -> None:
        self.audio_output: AudioOutput = None
        self.adjust_after_hot_word: Callable = _adjust_after_hot_word
        logging.getLogger().setLevel(logging.INFO)
        self.stopped: bool = False
        # load microphone
        self.speech_engine: sr.Recognizer = sr.Recognizer()
        self.speech_engine.pause_threshold = 0.5

        with sr.Microphone(device_index=None) as source:
            self.speech_engine.pause_threshold = 1
            self.speech_engine.energy_threshold = 50
            self.speech_engine.adjust_for_ambient_noise(source)
        self.audio_output: AudioOutput
        self.recording: bool = False
        self.sentensivity: float = 0.5

    def start(self, sentensivity: float, _hot_word_detected: Callable) -> None:
        # starts the hotword detection
        logging.info("[ACTION] Starting audio input module...")
        self.sentensivity = sentensivity
        self.stopped = False
        audio_input_thread: Thread = Thread(target=self.run, args=(sentensivity, _hot_word_detected,))
        audio_input_thread.daemon = True
        audio_input_thread.start()

    def run(self, sentensivity: float, _hot_word_detected: Callable) -> None:
        porcupine: any = None
        try:
            keywords: list = ["jarvis"]
            porcupine = pvporcupine.create(keywords=keywords, sensitivities=[sentensivity])
            pa = pyaudio.PyAudio()
            audio_stream: IO = pa.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length)

            logging.info('\nListening {%s}' % keywords)

            while not self.stopped:
                pcm: tuple[any, ...] = audio_stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
                keyword_index = porcupine.process(pcm)
                if keyword_index >= 0 and not self.recording:
                    self.recording = True
                    logging.info(
                        f'[ACTION] Detected {keywords[keyword_index]} at '
                        f'{datetime.now().hour}:{datetime.now().minute}')
                    self.recognize_input(_hot_word_detected)

        except MemoryError:
            porcupine.delete()
            self.start(self.sentensivity, _hot_word_detected)
        except Exception:
            logging.error(f"[ERROR] {traceback.print_exc()}")

    def recognize_file(self, audio_file) -> str:
        with audio_file as source:
            audio = self.speech_engine.record(source)
            text = self.speech_engine.recognize_google(audio, language="de-DE")
            return text

    def recognize_input(self, _hot_word_detected: Callable, listen: bool = False, play_bling_before_listen: bool = False) -> str:
        self.recording = True
        logging.info('[Listening] for user-input')
        # recognize user input through the microphone
        try:
            with sr.Microphone(device_index=None) as source:
                # record user input
                self.adjust_after_hot_word()

                # duration was the last change ---------------------------------------------------------
                audio = self.speech_engine.listen(source)
                # self.speech_engine.record(source)
                try:
                    # translate audio to text
                    text: str = self.speech_engine.recognize_google(audio, language="de-DE")
                    logging.info("[USER INPUT]\t" + text)
                except sr.UnknownValueError:
                    try:
                        # if it didn't worked, adjust the ambient-noise and try again
                        self.__adjusting()
                        text: str = self.speech_engine.recognize_google(audio, language="de-DE")
                        logging.info('[USER INPUT]\t' + text)
                    except sr.UnknownValueError:
                        text: str = "Audio could not be recorded"
            if not listen and not play_bling_before_listen:
                self.recording = False
                _hot_word_detected(text)
            else:
                # if the function was called by listen(), the text must be returned
                self.recording = False
                return text
        except Exception:
            traceback.print_exc()
            logging.warning("Text could not be translated...")
            self.recording = False
            return "Das habe ich nicht verstanden."

    def play_bling_sound(self, listen: bool) -> None:
        if not listen:
            # if there is no conservation, play a bling sound
            self.audio_output.play_bling_sound()

    def __adjusting(self) -> None:
        with sr.Microphone(device_index=None) as source:
            self.speech_engine.adjust_for_ambient_noise(source)

    def py_error_handler(self, filename, line, function, err, fmt) -> None:
        # This function suppress warnings from Alsa, which are totally useless
        pass

    def stop(self) -> None:
        # ends the hotword detection
        self.stopped = True


class MusicPlayer:
    """
    -------------------------
    Music-Player:
        - responsible for any music playback
        - can search a given topic on youtube (also bands or music genres) and then stream them
        - in no case to use for notifications or similar audio like e.g. for playing the news
          in the "tagesthemen" module
    -------------------------
    """

    def __init__(self, _audio_output: AudioOutput) -> None:
        self.music_thread: Thread = None
        self.playlist: list = []
        self.instance: vlc.Instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.audio_output: AudioOutput = _audio_output
        self.player_alive: bool = True
        self.is_playing: bool = False
        self.stopped: bool = False
        self.paused: bool = False
        self.skip: bool = False
        self.old_volume: int = 50

    def start(self) -> MusicPlayer:
        self.music_thread: Thread = Thread(target=self.run)
        self.music_thread.daemon = True
        self.music_thread.start()
        return self

    def run(self) -> None:
        self.player = self.instance.media_player_new()
        # wait until song is loaded in playlist
        while not self.playlist:
            time.sleep(0.2)
        while self.playlist:
            self.player.set_media(self.playlist[0])
            self.player.play()
            self.playlist.pop(0)
            # wait a second so that the player values are correct
            time.sleep(1)
            while self.player.is_playing() or self.paused:
                if self.skip:
                    # if skip is True, the next medium is loaded, skip is set to False and then by ending the
                    # loop the old video is stopped and in the next step the next one is loaded
                    self.skip = False
                    break
                time.sleep(2)

        self.is_playing = False
        self.player.stop()

    def play(self, by_name: str = None, url: str = False, path: str = False, as_next: bool = False, now: bool = False,
             playlist: bool = False, announce: bool = False) -> None:
        self.stopped = False
        if not self.is_playing and not self.paused:
            self.is_playing = True
            self.start()
        media = None
        """if playlist:
            self.add_playlist(url, by_name, next)"""
        if by_name is not None:
            _url = f'https://www.youtube.com/results?search_query={str(by_name)}'.replace("'", "").replace(' ',
                                                                                                           '+').rstrip(
                '+')
            html = urllib.request.urlopen(_url)
            video_ids: list = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            while True:
                try:
                    video: pafy = pafy.new(random.choice(video_ids))
                    duration: list = str(video.duration).split(":")
                    if int(duration[0]) == 0 and int(duration[1]) < 10:
                        best = video.getbest()
                        media = self.instance.media_new(best.url)
                        break
                    else:
                        continue
                except Exception:
                    continue
        elif url:
            media = self.instance.media_new(url)
        elif path:
            media = self.instance.media_new(path)
        else:
            return
        if media is not None:
            media.get_mrl()
        if as_next:
            self.playlist.insert(0, media)
        elif now:
            self.playlist.insert(0, media)
            self.skip_actual()
        else:
            self.playlist.append(media)

    def add_playlist(self, url: str, by_name: str, as_next: bool) -> None:
        playlist_ = pafy.get_playlist2(url)
        for item in playlist_:
            best = item.getbest()
            media = self.instance.media_new(item)
            media.get_mrl()
            if as_next:
                self.playlist.insert(0, media)
            else:
                self.playlist.append(media)

    def skip_actual(self) -> None:
        self.skip = True

    def clear(self) -> None:
        self.is_playing = False
        self.playlist.clear()
        self.player.stop()

    def pause(self) -> None:
        # when the player is paused, it is still playing in the sense of is_playing. Therefore the value of
        # is_playing remains at True
        self.paused = True
        self.player.pause()

    def resume(self) -> None:
        self.paused = False
        self.player.play()

    def set_volume(self, volume: float) -> None:
        if 0 < volume < 1:
            volume *= 100
        self.old_volume = self.player.audio_get_volume()
        self.player.audio_set_volume(int(volume))

    def stop(self) -> None:
        self.playlist = []
        self.is_playing = False
        self.player.stop()
        self.skip = True

    def stop_player(self) -> None:
        self.is_playing = False
        self.player_alive = False


class AudioOutput:
    """
    -------------------------
    AudioOutput:
        - responsible for the "normal" audio output
        - don´t use it for playing music (this is the task of the "MusicPlayer" class)
    -------------------------
    """

    def __init__(self, voice: str) -> None:
        # The channel are splittet on the buffers:
        # Channel(0): notification
        # Channel(1): music
        # Channel(2): playback

        self.listen: bool = False

        # music means "Backgroundmusic" or something like that
        self.music: list = []
        # playback are similar to music, but don´t contain "music"
        self.playback: list = []
        # notifications reduce the loudness from music but don´t pause it
        self.notification: list = []
        # mixer0: notification, mixer1: music
        self.mixer: list = []

        self.music_player: MusicPlayer = MusicPlayer(self)
        mixer.pre_init(44100, -16, 1, 512)
        self.tts: TTS = TTS()
        self.tts.start(voice)

        self.stopped: bool = True

    def start(self) -> AudioOutput:
        logging.info("[ACTION] Starting audio output module...")
        self.stopped = False
        mixer.init()
        time.sleep(2)
        ot: Thread = Thread(target=self.run)
        ot.daemon = True
        ot.start()
        return self

    def run(self) -> None:
        while not self.stopped:
            try:
                if self.listen:
                    mixer.Channel(0).set_volume(0.1)
                    mixer.Channel(1).set_volume(0.1)
                    mixer.Channel(2).set_volume(0.1)
                    self.music_player.set_volume(0.1)
                if not self.notification == [] and mixer.Channel(0).get_busy() == 0 and not self.tts.is_reading:
                    if mixer.Channel(0).get_busy() == 1:
                        mixer.Channel(1).set_volume(0.10)
                        mixer.Channel(2).set_volume(0.10)
                    if isinstance(self.notification[0], str):
                        logging.info(f'Saying "{self.notification[0]}"')
                        # if the notification is a string (a message to say), pass through to tts
                        self.tts.say(self.notification[0])
                        self.notification.pop(0)
                    else:
                        logging.info(f'Playing the track "{self.notification[0]}"')
                        # else pass through to mixer-manager
                        track: mixer.Sound = mixer.Sound(self.notification[0])
                        self.notification.pop(0)
                        mixer.Channel(0).play(track)
                if not self.music == [] and mixer.Channel(2).get_busy() == 0:
                    if isinstance(self.music[0], str):
                        logging.info(f'Play music with name {self.music[0]}')
                        topic = self.music[0]
                        self.music.pop(0)
                        self.music_player.play(by_name=topic)
                    else:
                        logging.info(f'Play track with path {self.music[0]}')
                        track = mixer.Sound(self.music[0])
                        mixer.Channel(2).play(track)
                        self.playback.pop(0)
                if not self.playback == [] and mixer.Channel(1).get_busy() == 0:
                    track = mixer.Sound(self.playback[0])
                    self.playback.pop(0)
                    mixer.Channel(1).play(track)
                if not mixer.Channel(0).get_busy() is 1 and mixer.Channel(1).get_volume != 1 and mixer.Channel(
                        2).get_volume != 1:
                    mixer.Channel(1).set_volume(1)
                    mixer.Channel(2).set_volume(1)
                time.sleep(0.2)
            except Exception:
                traceback.print_exc()

    def say(self, text: str) -> None:
        # Forwards the given text to the text-to-speech function and waits
        # until the announcement has ended.
        if text == '' or text is None:
            text: str = 'Das sollte nicht passieren. Eines meiner internen Module antwortet nicht mehr.'
        self.notification.append(text)
        # block while not done
        while text in self.notification:
            time.sleep(0.2)

    def adjust_after_hot_word(self) -> None:
        self.listen = True
        self.music_player.set_volume(10)

    def continue_after_hotword(self) -> None:
        self.listen = False
        self.music_player.set_volume(100)

    def play_music(self, name: str, as_next: bool = False) -> None:
        if as_next:
            self.music.insert(0, name)
        else:
            self.music.append(name)

    def play_playback(self, buff: io.BytesIO, as_next: bool) -> None:
        if not as_next:
            self.playback.append(buff)
        else:
            self.playback.insert(0, buff)

    def play_notification(self, buff: io.BytesIO, as_next: bool) -> None:
        if not as_next:
            self.notification.append(buff)
        else:
            self.notification.insert(0, buff)

    def play_bling_sound(self) -> None:
        TOP_DIR: str = os.path.dirname(os.path.abspath(__file__))
        DETECT_DONG: str = os.path.join(TOP_DIR, "resources/sounds/bling.wav")

        with open(DETECT_DONG, "rb") as wavfile:
            input_wav: bytes = wavfile.read()
        data: io.BytesIO = io.BytesIO(input_wav)
        self.play_notification(data, as_next=True)

    @staticmethod
    def pause(channel: int) -> None:
        mixer.Channel(channel).pause()

    @staticmethod
    def resume(channel: int) -> None:
        mixer.Channel(channel).unpause()

    @staticmethod
    def set_volume(channel: int, volume: float) -> None:
        mixer.Channel(channel).set_volume(volume)

    @staticmethod
    def stop_notification() -> None:
        mixer.Channel(0).stop()

    @staticmethod
    def stop_music() -> None:
        mixer.Channel(1).stop()

    @staticmethod
    def stop_playback() -> None:
        mixer.Channel(2).stop()

    def stop(self) -> None:
        self.stopped = True
        self.music_player.stop()
        mixer.stop()
        self.tts.stop()
