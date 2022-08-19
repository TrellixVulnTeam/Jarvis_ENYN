#!/usr/bin/pythob
# -*- coding:utf-8 -*-

# Modul schickt ein Youtube-Video, das als url übergeben wird an Telegram.
# Daher nur für Telegram vorgesehen

import os
from pathlib import Path

import pytube

from src import log
from src.modules import ModuleWrapper


def isValid(text: str) -> bool:
    text = text.lower()

    if (
            ("schicke" in text or "schick" in text or "sende" in text)
            and "video" in text
            and "einkaufsliste" not in text
    ):
        return True
    elif "lade" in text and "video" in text and "herunter" in text:
        return True
    else:
        return False


def handle(text: str, core: ModuleWrapper):
    SAVE_PATH: Path = core.path.joinpath("modules").joinpath("resources")
    VIDEO_PATH: Path = SAVE_PATH

    core.say(
        "Wie lautet die URL von dem Youtube-Video, das ich dir schicken soll?",
        output="messenger",
    )

    response = core.listen(text="Wie lautet die URL von dem Youtube-Video, das ich dir schicken soll?", messenger=True)
    try:
        core.say("Video wird heruntergeladen. Bitte warte einen Moment.", output="messenger")
        youtube = pytube.YouTube(response)
        video = youtube.streams.get_highest_resolution()
        if not video:
            core.say("Der Link konnte keinem Video zugeordnet werden.")
        else:

            send_video_to_messenger(text, core, VIDEO_PATH)

    except Exception as e:
        core.say("Es gab einen Fehler. Bitte versuche es erneut.")
        log.exception(e)
        log.warning(f"There was a problem with the module '{Path(__file__).name.removesuffix('.py')}'!")
    try:
        # Video wird gelöscht, damit der Speicher nicht unnötig belastet wird
        os.remove(VIDEO_PATH)
    except Exception as e:
        log.exception(e)
        log.warning(f"Could not delete file '{VIDEO_PATH}'!")


def __download_video(core: ModuleWrapper, video, SAVE_PATH: str) -> None:
    core.say("Einen Moment bitte. Das Video wird heruntergeladen...")
    video.download(SAVE_PATH, filename="YouTube")


def send_video_to_messenger(text, core, VIDEO_PATH):
    try:
        # UID aus local_storage entnehmen und dann Video als file dem Nutzer schicken
        # Da Videos gerne auch mal länger als 10min gehen, wird auf das Senden
        # als Datei gesetzt, da es sonst zu Problemen kommen kann
        core.messenger.bot.send_file(core.user.messenger_id, video=open(VIDEO_PATH, "rb"), supports_streaming=True)
    except KeyError as e:
        log.warning(
            f"Der Text '{text}' konnte nicht gesendet werden, da für den Nutzer '{core.user.alias} (id: {core.user.uid})' keine Telegram-ID angegeben wurde")
        log.exception(e)
