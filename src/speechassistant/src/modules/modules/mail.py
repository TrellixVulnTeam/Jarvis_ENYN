import os
import tempfile

WORDS = ["mail", "e-mail"]


def isValid(text):
    text = text.lower().strip()
    if (
        text.startswith("mail ")
        or text.lower().startswith("e-mail ")
        or text.lower().startswith("email ")
        or text.lower().startswith("e mail ")
    ):
        return True
    return False


def handle(text, core, skills):
    text = text.strip()
    if (
        text.lower().startswith("mail ")
        or text.lower().startswith("e-mail ")
        or text.lower().startswith("email ")
        or text.lower().startswith("e mail ")
    ):
        subject = text[5:]
        core.say("Vertrau mir deine Mail an. Zum Beenden nutze das Wort fertig.")
        body = []
        text = core.listen().strip()
        while (
            text.lower() != "stop"
            and text.lower() != "stopp"
            and text.lower() != "fertig"
        ):
            if text != "" and text != "TIMEOUT_OR_INVALID":
                body.append(text)
            text = core.listen().strip()
        core.end_Conversation()
        try:
            file = tempfile.NamedTemporaryFile(mode="w", delete=False)
            file.write("To: \n")
            file.write("Subject: " + subject + "\n\n")
            for line in body:
                file.write(line + "\n\n")
            file.close()
            os.system('claws-mail --compose-from-file "' + file.name + '"')
        except IOError:
            core.say("Es ist ein Fehler aufgetreten.")
