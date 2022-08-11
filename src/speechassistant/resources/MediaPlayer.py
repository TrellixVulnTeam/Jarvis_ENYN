import os
import time

import vlc


class MyMediaPlayer:
    def __init__(self):
        self.player: vlc.MediaPlayer = vlc.MediaPlayer()

    def play_tts(self, path: str) -> None:
        self.player.set_rate(1.5)
        try:
            media = vlc.Media(path)
            self.player.set_media(media)
            self.player.play()

            while self.player.is_playing():
                time.sleep(0.5)
            os.remove(path)
        except:
            pass
        self.player.set_rate(1)
