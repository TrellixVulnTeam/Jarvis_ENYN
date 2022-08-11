def isValid(text):
    text = text.lower()
    if "stopp" in text:
        return True
    if ("beend" in text) and ("musik" in text or "ausgabe" in text or "wecker" in text):
        return True


def handle(text, core, skills):
    text = text.lower()
    if "musik" in text:
        core.audio_output.music_player.stop()
    elif "ausgabe" in text:
        core.audio_output.stop_notification()
        core.audio_output.stop_music()
        core.audio_output.stop_playback()
    elif "wecker" in text or "wach" in text:
        core.audio_output.stop_playback()
    else:
        core.audio_output.music_player.stop()
        core.audio_output.stop_notification()
        core.audio_output.stop_music()
        core.audio_output.stop_playback()
