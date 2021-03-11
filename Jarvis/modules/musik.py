def isValid(text):
    text = text.lower()
    if 'spiel' in text:
        return True
    return False

def handle(text, luna, skills):
    luna.say("Alles klar.")
    startword = "spiele" if "spiele" in text else "spiel"
    song = skills.get_text_beetween(startword, text, output="String")
    print(song)
    luna.play_music(song, youtube=True)
