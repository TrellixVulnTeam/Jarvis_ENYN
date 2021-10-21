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

import pafy
import pvporcupine
import pyaudio
import speech_recognition as sr
import vlc
from pygame import mixer as audio

from resources.tts import Text_to_Speech


class AudioInput:
    """
    -------------------------
    AudioInput:
        - responsible for the whole audio input
    -------------------------
    """

    def __init__(self):
        logging.getLogger().setLevel(logging.INFO)
        self.stopped = False
        # load microphone
        self.speech_engine = sr.Recognizer()
        self.speech_engine.pause_threshold = 0.5

        with sr.Microphone(device_index=None) as source:
            # terminate noise
            self.speech_engine.adjust_for_ambient_noise(source)
        self.core = None
        self.Audio_Output = None
        self.recording = False

    def start(self):
        # starts the hotword detection
        self.stopped = False
        snsrt = Thread(target=self.run)
        snsrt.daemon = True
        snsrt.start()

    def stop(self):
        # ends the hotword detection
        self.stopped = True

    def set_core(self, core, Audio_Output):
        self.core = core
        self.Audio_Output = Audio_Output

    def recognize_file(self, audio_file):
        with audio_file as source:
            audio = self.speech_engine.record(source)
            text = self.speech_engine.recognize_google(audio, language="de-DE")
            return text

    def recognize_input(self, listen=False, play_bling_before_listen=False):
        self.recording = True
        logging.info('[Listening] for user-input')
        # recognize user input through the microphone
        try:
            with sr.Microphone(device_index=None) as source:
                # record user input
                self.Audio_Output.detected_hotword()

                # duration was the last change ---------------------------------------------------------
                audio = self.speech_engine.listen(source, duration=0.2, )
                # self.speech_engine.record(source)
                try:
                    # translate audio to text
                    text = self.speech_engine.recognize_google(audio, language="de-DE")
                    logging.info("[USER INPUT]\t" + text)
                except:
                    try:
                        # if it didn´t worked, adjust the ambient-noise and try again
                        self.adjusting()
                        text = self.speech_engine.recognize_google(audio, language="de-DE")
                        logging.info('[USER INPUT]\t' + text)
                    except:
                        text = "Audio could not be recorded"
            if not listen and not play_bling_before_listen:
                self.recording = False
                self.core.hotword_detected(text)
            else:
                # if the function was called by listen(), the text must be returned
                self.recording = False
                return text
        except:
            traceback.print_exc()
            logging.warning("Text could not be translated...")
            self.recording = False
            return "Das habe ich nicht verstanden."

    def play_bling_sound(self, listen):
        if not listen:
            # if there is no conservation, play a bling sound
            self.Audio_Output.play_bling_sound()

    def run(self):
        porcupine = None
        try:
            keywords = ["jarvis", "hey siri"]
            porcupine = pvporcupine.create(keywords=keywords, sensitivities=[0.5, 0.2])
            pa = pyaudio.PyAudio()
            audio_stream = pa.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length)

            logging.info('\nListening {%s}' % keywords)

            while not self.stopped and not self.recording:
                pcm = audio_stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
                keyword_index = porcupine.process(pcm)
                if keyword_index >= 0:
                    if keyword_index > 0:
                        self.core.hotword_detected("wrong assistant!")
                    else:
                        self.recording = True
                        logging.info(
                            f'[ACTION] Detected {keywords[keyword_index]} at {datetime.now().hour}:{datetime.now().minute}')
                        self.recognize_input()

        except MemoryError:
            porcupine.delete()
            self.start()
        except:
            logging.error(f"[ERROR] {traceback.print_exc()}")

    def adjusting(self):
        with sr.Microphone(device_index=None) as source:
            self.speech_engine.adjust_for_ambient_noise(source)

    def py_error_handler(self, filename, line, function, err, fmt):
        # This function suppress warnings from Alsa, which are totally useless
        pass


class AudioOutput:
    """
    -------------------------
    AudioOutput:
        - responsible for the "normal" audio output
        - don´t use it for playing music (this is the task of the "MusicPlayer" class)
    -------------------------
    """

    def __init__(self, voice):
        # The channel are splittet on the buffers:
        # Channel(0): notification
        # Channel(1): music
        # Channel(2): playback

        self.listen = False

        # music means "Backgroundmusic" or something like that
        self.music = []
        # playback are similar to music, but don´t contain "music"
        self.playback = []
        # notifications reduce the loudness from music but don´t pause it
        self.notification = []
        # mixer0: notification, mixer1: music
        self.mixer = []

        self.music_player = MusicPlayer(self)
        # audio.pre_init(44100, -16, 1, 512)
        self.tts = Text_to_Speech()
        self.tts.start(voice)

    def start(self):
        audio.init()
        ot = Thread(target=self.run)
        ot.daemon = True
        ot.start()
        return self

    def run(self):
        while True:
            try:
                if self.listen:
                    audio.Channel(0).set_volume(0.1)
                    audio.Channel(1).set_volume(0.1)
                    audio.Channel(2).set_volume(0.1)
                if not self.notification == [] and audio.Channel(0).get_busy() == 0 and not self.tts.is_reading:
                    if audio.Channel(0).get_busy() == 1:
                        audio.Channel(1).set_volume(0.10)
                        audio.Channel(2).set_volume(0.10)
                    if type(self.notification[0]) == type("string"):
                        logging.info(f'Saying "{self.notification[0]}"')
                        # if the notification is a string (a message to say), pass through to tts
                        self.tts.say(self.notification[0])
                        self.notification.pop(0)
                    else:
                        logging.info(f'Playing the track "{self.notification[0]}"')
                        # else pass through to audio-manager
                        track = audio.Sound(self.notification[0])
                        self.notification.pop(0)
                        audio.Channel(0).play(track)
                if not self.music == [] and audio.Channel(2).get_busy() == 0:
                    if type(self.music[0]) == type("string"):
                        logging.info(f'Play music with name {self.music[0]}')
                        topic = self.music[0]
                        self.music.pop(0)
                        self.music_player.play(by_name=topic)
                    else:
                        logging.info(f'Play track with path {self.music[0]}')
                        track = audio.Sound(self.music[0])
                        audio.Channel(2).play(track)
                        self.playback.pop(0)
                if not self.playback == [] and audio.Channel(1).get_busy() == 0:
                    track = audio.Sound(self.playback[0])
                    self.playback.pop(0)
                    audio.Channel(1).play(track)
                if not audio.Channel(0).get_busy() == 1 and audio.Channel(1).get_volume != 1 and audio.Channel(
                        2).get_volume != 1:
                    audio.Channel(1).set_volume(1)
                    audio.Channel(2).set_volume(1)
                time.sleep(0.2)
            except:
                traceback.print_exc()

    def say(self, text):
        # Forwards the given text to the text-to-speech function and waits
        # until the announcement has ended.
        if text == '' or text == None:
            text = 'Das sollte nicht passieren. Eines meiner internen Module antwortet nicht mehr.'
        self.notification.append(text)
        while text in self.notification:
            time.sleep(0.2)

    def detected_hotword(self):
        self.listen = True
        self.music_player.set_volume(10)

    def continue_after_hotword(self):
        self.listen = False
        self.music_player.set_volume(100)

    def play_music(self, name, next=False):
        if next:
            self.music.insert(0, name)
        else:
            self.music.append(name)

    def play_playback(self, buff, next):
        if not next:
            self.playback.append(buff)
        else:
            self.playback.insert(0, buff)

    def play_notification(self, buff, next):
        if not next:
            self.notification.append(buff)
        else:
            self.notification.insert(0, buff)

    def play_bling_sound(self):
        # playing Bling-Sound
        TOP_DIR = os.path.dirname(os.path.abspath(__file__))
        DETECT_DONG = os.path.join(TOP_DIR, "resources/sounds/bling.wav")

        with open(DETECT_DONG, "rb") as wavfile:
            input_wav = wavfile.read()
        data = io.BytesIO(input_wav)
        self.play_notification(data, next=True)

    def pause(self, channel):
        audio.Channel(channel).pause()

    def resume(self, channel):
        audio.Channel(channel).unpause()

    def set_volume(self, channel, volume):
        audio.Channel(channel).set_volume(volume)

    def stop_notification(self):
        audio.Channel(0).stop()

    def stop_music(self):
        audio.Channel(1).stop()

    def stop_playback(self):
        audio.Channel(2).stop()

    def stop(self):
        self.tts.stop()
        audio.stop()
        self.music_player.stop()


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

    def __init__(self, Audio_Output):
        self.music_thread = None
        self.playlist = []
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.Audio_Output = Audio_Output
        self.player_alive = True
        self.is_playing = False
        self.stopped = False
        self.paused = False
        self.skip = False
        self.old_volume = 50

    def start(self):
        self.music_thread = Thread(target=self.run)
        self.music_thread.daemon = True
        self.music_thread.start()
        return self

    def run(self):
        self.player = self.instance.media_player_new()
        while self.playlist == []:
            # wait until song is loaded in playlist
            time.sleep(0.2)
        while self.playlist != []:
            self.player.set_media(self.playlist[0])
            self.player.play()
            self.playlist.pop(0)
            # wait a second so that the player values are correct
            time.sleep(2)
            while self.player.is_playing() or self.paused:
                # while song is played
                if self.skip:
                    # if skip is True, the next medium is loaded, skip is set to False and then by ending the
                    # loop the old video is stopped and in the next step the next one is loaded
                    self.skip = False
                    break
                time.sleep(2)

        self.is_playing = False
        self.player.stop()

    def play(self, by_name=None, url=False, path=False, next=False, now=False, playlist=False, announce=False):
        self.stopped = False
        if not self.is_playing and not self.paused:
            self.is_playing = True
            self.start()
        media = None
        """if playlist:
            self.add_playlist(url, by_name, next)"""
        if not by_name == None:
            _url = f'https://www.youtube.com/results?search_query={str(by_name)}'.replace("'", "").replace(' ',
                                                                                                           '+').rstrip(
                '+')
            html = urllib.request.urlopen(_url)
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            while True:
                try:
                    video = pafy.new(random.choice(video_ids))
                    duration = str(video.duration).split(":")
                    if int(duration[0]) == 0 and int(duration[1]) < 10:
                        best = video.getbest()
                        media = self.instance.media_new(best.url)
                        break
                    else:
                        continue
                except:
                    continue

        elif not url == False:
            media = self.instance.media_new(url)
        elif not path == False:
            media = self.instance.media_new(path)
        else:
            return
        if media is not None:
            media.get_mrl()
        if next:
            self.playlist.insert(0, media)
        elif now:
            self.playlist.insert(0, media)
            self.next()
        else:
            self.playlist.append(media)

    def add_playlist(self, url, by_name, next):
        playlist_ = pafy.get_playlist2(url)
        for item in playlist_:
            best = item.getbest()
            media = self.instance.media_new(item)
            media.get_mrl()
            self.playlist.append(media)

    def next(self):
        self.skip = True

    def clear(self):
        self.is_playing = False
        self.playlist.clear()
        self.player.stop()

    def pause(self):
        # when the player is paused, it is still playing in the sense of is_playing. Therefore the value of
        # is_playing remains at True
        self.paused = True
        self.player.pause()

    def resume(self):
        self.paused = False
        self.player.play()

    def set_volume(self, volume):
        self.old_volume = self.player.audio_get_volume()
        self.player.audio_set_volume(volume)

    def stop(self):
        self.playlist = []
        self.is_playing = False
        self.player.stop()
        self.skip = True

    def stop_player(self):
        self.is_playing = False
        self.player_alive = False
