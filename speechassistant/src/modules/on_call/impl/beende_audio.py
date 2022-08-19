from src.modules import ModuleWrapper


# toDo: rework

def is_valid(text: str) -> bool:
    text = text.lower()
    if "stopp" in text:
        return True
    if ("beend" in text) and ("musik" in text or "ausgabe" in text or "wecker" in text):
        return True


def handle(text: str, wrapper: ModuleWrapper) -> None:
    text = text.lower()
    if "musik" in text:
        wrapper.audio_output.music_player.stop()
    elif "ausgabe" in text:
        wrapper.audio_output.stop_notification()
        wrapper.audio_output.stop_music()
        wrapper.audio_output.stop_playback()
    elif "wecker" in text or "wach" in text:
        wrapper.audio_output.stop_playback()
    else:
        wrapper.audio_output.music_player.stop()
        wrapper.audio_output.stop_notification()
        wrapper.audio_output.stop_music()
        wrapper.audio_output.stop_playback()
