import os
import time

import vlc

from src import log


class MyMediaPlayer:
    def __init__(self):
        self.instance: vlc.Instance = vlc.Instance(
            "-I dummy --no-video --aout=alsa --file-logging --logfile=vlc-log.txt --verbose 3"
        )
        self.player: vlc.MediaPlayer = self.instance.media_player_new()

    def play_tts(self, path: str) -> None:
        self.player.set_rate(1.5)
        try:
            log.debug(f"Create new media from path '{path}'")
            media = self.instance.media_new(path)
            self.player.set_media(media)
            log.debug("Play audio...")
            self.player.play()

            while self.player.is_playing():
                time.sleep(0.5)
            log.debug("Playing done! Removing file...")
            os.remove(path)
            log.debug("File removed!")
        except:
            log.warning("Error while playing tts!")
        self.player.set_rate(1)
