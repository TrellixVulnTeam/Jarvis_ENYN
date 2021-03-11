#!/usr/bin/env python3

import urllib.request

SECURE = True

def isValid(text):
    text = text.lower()
    if 'qr' in text:
        return True
    else:
        return False

def handle(text, luna, profile):

    luna.say('Was möchtest du in den qr-code schreiben?')

    # Frage den Nutzer nach Inhalt
    antwort = luna.listen()
    if antwort == 'TIMEOUT_OR_INVALID':
        luna.say('Ich konnte dich leider nicht verstehen')
    else:
        url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={urllib.parse.quote(antwort)}"
        luna.say(url)

class Luna:
    def __init__(self):
        pass

    def say(self,text):
        print(text)

    def listen(self):
        input()

if __name__ == "__main__":
    luna = Luna()
    handle("", luna, "")