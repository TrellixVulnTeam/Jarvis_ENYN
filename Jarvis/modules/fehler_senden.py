import os
import re
import subprocess
import tempfile


def isValid(text):
    text = text.lower()
    if 'fehler' in text and ('senden' in text or 'schicken' in text):
        return True
    elif 'fehlermeldung' in text:
        return True


def handle(text, core, skills):
    core.say(
        "Wilkommen in dem Modul, um einen Fehler zu senden. Wenn du nicht mehr weiter machen möchtest, dann sag einfach 'abbruch'.")
    core.say("Bitte nenn deinen Namen.")
    name = core.listen()
    if name is 'abbruch':
        name = 'UNDO'
        core.say('Alles klar, der Vorgang wird abgebrochen!')
    else:
        core.say("Alles klar, {}. Anschließend nenn bitte in einem Schlagwort den Anwendungsbereich ".format(name))
        modul_name = core.listen()
        if modul_name is 'abbruch':
            modul_name = 'UNDO'
            core.say('Alles klar, der Vorgang wird abgebrochen!')
        else:
            core.say('Bitte nenn deine E-Mail-Adresse oder eine andere Möglichkeit, wie man dich erreichen kann.')
            mail = core.listen()
            if mail is 'abbruch':
                mail = 'UNDO'
                core.say('Alles klar, der Vorgang wird abgebrochen!')
            else:
                core.say(
                    "Okay gut. Nun beschreib den Fehler bitte ausführlicher. Ab jetzt kannst du leider den Vorgang nicht mehr abbrechen. ")
                description = core.listen()

            sendIssu(name, modul_name, mail, description)
            core.say(
                'Vielen Dank! Ich werde den Fehler an Jakob weiterleiten. Bitte schick auch in Zukunft Fehler, damit Core weiterhin gut genutzt werden kann.')
            core.end_Conversation()


def sendIssu(name, modul_name, mail, description):
    from simplemail import Email
    Email(
        from_address="core_issus@outlook.de",
        to_address="jakob.priesner@outlook.de",
        subject="LUNA - Fehler!",
        message="Name: {}\nModul-Name: {}\nMail: {}\nNachricht: {}".format(name, modul_name, mail, description)
    ).send()
