def isValid(text):
    text = text.lower()
    if 'spiel' in text:
        return True
    return False

def handle(text, luna, skills):
    luna.say("Alles klar.")
    startword = "spiele" if "spiele" in text else "spiel"
    until = ''
    until_words = ['nächstes', 'danach', 'gleich']
    for word in until_words:
        if word in text:
            until = word
            break
    song = skills.get_text_beetween(startword, text, end_word=until, output="String")
    next = False
    if 'nächstes' in text or 'danach' in text or 'gleich' in text:
        next = True

    luna.play_music(by_name=song, url=False, path=False, next=next, now=False, playlist=False, announce=False)
