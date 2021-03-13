import struct
import time
import traceback
from datetime import datetime
from threading import Thread

import requests
import vlc
import pafy

from tts import Text_to_Speech
import speech_recognition as sr
import pyaudio
import pvporcupine
from pygame import mixer as audio


class AudioInput:
    def __init__(self):
        self.stopped = False
        # load microphone
        self.speech_engine = sr.Recognizer()
        self.speech_engine.pause_threshold = 0.5

        with sr.Microphone(device_index=None) as source:
            # terminate noise
            self.speech_engine.adjust_for_ambient_noise(source)
        self.luna = None

    def start(self):
        # starts the hotword detection
        self.stopped = False
        snsrt = Thread(target=self.run)
        snsrt.daemon = True
        snsrt.start()

    def stop(self):
        # ends the hotword detection
        self.stopped = True

    def set_luna(self, luna):
        self.luna = luna

    def recognize_file(self, audio_file):
        with audio_file as source:
            audio = self.speech_engine.record(source, offset=10)
            text = self.speech_engine.recognize_google_cloud(audio, language="de-DE", )
            return text

    def recognize_input(self, listen=False):
        # recognize user input through the microphone
        try:
            if not listen:
                # if there is no conservation, play a bling sound
                self.luna.play_bling_sound()
            with sr.Microphone(device_index=None) as source:
                # record user input
                audio = self.speech_engine.listen(source, timeout=3, phrase_time_limit=5)
                try:
                    # translate audio to text
                    text = self.speech_engine.recognize_google(audio, language="de-DE")
                    print("[USER INPUT] ", text)
                except:
                    text = "Audio could not be recorded"
            if not listen:
                self.luna.hotword_detected(text)
            else:
                return text
        except:
            traceback.print_exc()
            print("[WARNING] Text could not be translated...")
            return "Das habe ich nicht verstanden."

    def run(self):
        porcupine = None

        try:
            keywords = ["jarvis", "hey siri"]
            porcupine = pvporcupine.create(keywords=keywords, sensitivities=[0.4, 0.2])
            pa = pyaudio.PyAudio()

            audio_stream = pa.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length)

            print('[INFO] Listening {')
            for keyword in keywords:
                print('  %s' % (keyword))
            print('}')

            while True:
                pcm = audio_stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
                keyword_index = porcupine.process(pcm)
                if keyword_index >= 0:
                    if(keyword_index > 0):
                        self.luna.hotword_detected("wrong assistant!")
                    else:
                        print('[%s] Detected %s' % (str(datetime.now()), keywords[keyword_index]))
                        self.recognize_input()

        except MemoryError:
            porcupine.delete()
            self.start()
        except:
            print(f"[ERROR] {traceback.print_exc()}")

    def py_error_handler(self, filename, line, function, err, fmt):
        # This function suppress warnings from Alsa, which are totally useless
        pass


class AudioOutput:
    def __init__(self):
        # The channel are splittet on the buffers:
        # Channel(0): notification
        # Channel(1): music
        # Channel(2): playback

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
        audio.init()
        self.tts = Text_to_Speech()
        self.tts.start('male')
        self.tts.start('male')

    def start(self):
        ot = Thread(target=self.run)
        ot.daemon = True
        ot.start()
        return self

    def run(self):
        while True:
            try:
                if not self.notification == [] and audio.Channel(0).get_busy() == 0 and not self.tts.is_reading:
                    if audio.Channel(1).get_busy() == 1:
                        audio.Channel(1).set_volume(0.25)
                    if type(self.notification[0]) == type("string"):
                        self.tts.say(self.notification[0])
                        self.notification.pop(0)
                    else:
                        track = audio.Sound(self.notification[0])
                        self.notification.pop(0)
                        audio.Channel(0).play(track)
                        while audio.Channel(0).get_busy() == 1:
                            time.sleep(0.25)
                    audio.Channel(1).set_volume(1)
                if not self.music == [] and audio.Channel(2).get_busy() == 0:
                    if type(self.music[0]) == type("string"):
                        topic = self.music[0]
                        self.music.pop(0)
                        self.music_player.play(by_name=topic)
                    else:
                        track = audio.Sound(self.music[0])
                        audio.Channel(2).play(track)
                        self.playback.pop(0)
                if not self.playback == [] and audio.Channel(1).get_busy() == 0:
                    track = audio.Sound(self.music[0])
                    self.music.pop(0)
                    audio.Channel(1).play(track)
                time.sleep(0.1)
            except:
                traceback.print_exc()

    def say(self, text):
        # Forwards the given text to the text-to-speech function and waits
        # until the announcement has ended.
        if text == '' or text == None:
            text = 'Das sollte nicht passieren. Eines meiner internen Module antwortet nicht mehr.'
        self.notification.append(text)

    def play_music(self, name, next=False):
        if next:
            self.music.insert(0, name)
        else:
            self.music.append(name)

    def play_playback(self, buff, next=False):
        if not next:
            self.playback.append(buff)
        else:
            self.playback.insert(0, buff)

    def play_notification(self, buff, next=False):
        if not next:
            self.notification.append(buff)
        else:
            self.notification.insert(0, buff)

    def pause(self, channel):
        audio.Channel(channel).pause()

    def resume(self, channel):
        audio.Channel(channel).unpause()

    def set_volume(self, channel, volume):
        audio.Channel(channel).set_volume(volume)

    def stopp_notification(self):
        audio.Channel(0).stop()

    def stopp_music(self):
        audio.Channel(1).stop()

    def stopp_playback(self):
        audio.Channel(2).stop()

    def stop(self):
        self.tts.stop()
        audio.stop()


class MusicPlayer:

    """
    -------------------------
    Music-Player:
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
        time.sleep(2)
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

    def play(self, by_name=False, url=False, path=False, next=False, announce=False):
        if not self.is_playing and not self.paused:
            self.is_playing = True
            self.start()
        if not by_name == False:
            _url = 'https://www.youtube.com/results?q=' + str(by_name)
            count = 0
            data = str(requests.get(_url).content).split('"')
            for i in data:
                count += 1
                if i == 'WEB_PAGE_TYPE_WATCH':
                    break
            print(data)
            if data[count - 5] == "/results":
                #toDo: find new video
                raise Exception("No video found.")
            _url = "https://www.youtube.com" + data[count - 5]
            video = pafy.new(_url)
            best = video.getbest()
            media = self.instance.media_new(best.url)
        elif not url == False:
            media = self.instance.media_new(url)
        elif not path == False:
            media = self.instance.media_new(path)
        else:
            return

        if announce:
            title = media.get_title()
            text = "Alles klar. Ich spiele für dich " + title
            #toDo: Adio_Output.tts(...)
            pass

        media.get_mrl()
        if next:
            self.playlist.insert(0, media)
        else:
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
        self.player.audio_set_volume(volume)

    def stop(self):
        self.is_playing = False
        self.player.stop()

    def stop_player(self):
        self.is_playing = False
        self.player_alive = False