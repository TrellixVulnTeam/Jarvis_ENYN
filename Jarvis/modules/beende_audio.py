def isValid(text):
    text = text.lower()
    if 'stopp' in text:
        return True
    if ('beend' in text) and ('musik' in text or 'ausgabe' in text or 'wecker' in text):
        return True


def handle(text, core, skills):
    text = text.lower()
    if 'musik' in text:
        core.Audio_Output.music_player.stop()
    elif 'ausgabe' in text:
        core.Audio_Output.stop_notification()
        core.Audio_Output.stop_music()
        core.Audio_Output.stop_playback()
    elif 'wecker' in text:
        core.Audio_Output.stop_playback()
    else:
        core.Audio_Output.music_player.stop()
        core.Audio_Output.stop_notification()
        core.Audio_Output.stop_music()
        core.Audio_Output.stop_playback()
