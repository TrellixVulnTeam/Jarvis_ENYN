#!/usr/bin/pythob
# -*- coding:utf-8 -*-

# Modul schickt ein Youtube-Video, das als url übergeben wird an Telegram.
# Daher nur für Telegram vorgesehen

import os
import traceback

import pytube


def isValid(text):
    text = text.lower()

    if ('schicke' in text or 'schick' in text or 'sende' in text) and 'video' in text and not 'einkaufsliste' in text:
        return True
    elif 'lade' in text and 'video' in text and 'herunter' in text:
        return True
    else:
        return False


def handle(text, core, skills):
    # Festlegen der Zielpfade
    SAVE_PATH = core.path + '/modules/resources'
    VIDEO_PATH = SAVE_PATH + '/YouTube.mp4'
    core.say('Wie lautet die URL von dem Youtube-Video, das ich dir schicken soll?', output='messenger')
    # Holen der URL
    response = core.listen(input='messenger')
    try:
        core.say('Video wird heruntergeladen. Bitte warte einen Moment.', output='messenger')
        try:
            youtube = pytube.YouTube(response)
        except:
            core.say('Der Link konnte keinem Video zugeordnet werden.')

        # Die höchte Auflösung finden und dann herunterladen
        video = youtube.streams.get_highest_resolution()
        core.say("Einen Moment bitte. Das Video wird heruntergeladen...")
        video.download(SAVE_PATH, filename="YouTube")

        send_video_to_messenger(core, VIDEO_PATH)

    except Exception as e:
        core.say('Es gab einen Fehler. Bitte versuche es erneut.')
        traceback.print_exc()
    try:
        # Video wird gelöscht, damit der Speicher nicht unnötig belastet wird
        os.remove(VIDEO_PATH)
    except:
        traceback.print_exc()


def send_video_to_messenger(core, VIDEO_PATH):
    try:
        # UID aus local_storage entnehmen und dann VIdeo als file dem Nutzer schicken
        # Da Videos gerne auch mal länger als 10min gehen, wird auf das Senden
        # als Datei gesetzt, da es sonst zu Problemen kommen kann
        uid = core.local_storage['LUNA_messenger_name_to_id_table'][core.user]
        core.messenger.bot.send_file(uid, video=open(VIDEO_PATH, 'rb'), supports_streaming=True)
    except KeyError as e:
        print(
            '[WARNING] Der Text "{}" konnte nicht gesendet werden, da für den Nutzer "{}" keine Telegram-ID angegeben wurde'.format(
                text, user), conv_id=original_command, show=True)
        traceback.print_exc()
