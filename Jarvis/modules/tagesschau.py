import os
from pathlib import Path

import requests
from bs4 import BeautifulSoup
# PRIORITY = 6
from pydub import AudioSegment

TAGESSCHAU_URL = "https://www.internetradio-horen.de/podcasts/tagesschau-in-100-sekunden"


def isValid(text):
    text = text.lower()
    if 'was' in text and ("gibt's" in text or 'gibts' in text) and 'neues' in text:
        return True
    if ('sage' in text or 'erzähl' in text or 'erzähle' in text or 'sprich' in text) and 'nachrichten' in text:
        return True


def handle(text, core, skills):
    DOWNLOAD_PATH = Path(core.path + "/modules/resources")
    try:
        DOWNLOAD_PATH = Path(core.path + "/modules/resources")
        url = get_audio_url()
        path = download_audio(url, DOWNLOAD_PATH)

        sound = AudioSegment.from_mp3(core.path + "/modules/resources" + "/tagesschau_100sec.mp3")
        sound.export(core.path + "/modules/resources/tagesschau_100sec.wav", format="wav")
        # wav = wave.open(core.path + "/modules/resources/tagesschau_100sec.wav", 'rb')
        core.play(path=core.path + "/modules/resources/tagesschau_100sec.wav")
        # text = core.recognize(wav)
        os.remove(path)
        # core.say(text)

    except Exception as e:
        print(f"Abbruch durch Fehler: {e}")


def get_content(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def get_audio_url():
    soup = BeautifulSoup(get_content(TAGESSCHAU_URL), "html.parser")
    meta = soup.find('audio', id='audio_player_podcasts')
    if not meta or not meta.has_attr("src"):
        raise ValueError("Konnte keine Infos zur Audio-URL finden")
    return meta["src"]


def download_audio(url, DOWNLOAD_PATH):
    filename = 'tagesschau_100sec.mp3'
    path = DOWNLOAD_PATH / filename
    try:
        path.write_bytes(get_content(url))
    except:
        pass
    return path
