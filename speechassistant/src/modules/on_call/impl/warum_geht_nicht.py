def is_valid(text):
    text = text.lower()
    if (
            "warum" in text
            and ("funktioniert" in text or "geht" in text)
            and "nicht" in text
    ):
        return True


def handle(text, core):
    text = text.lower()
    core.say(
        "Tut mir leid, dieses Modul ist noch in der Entwicklung. Bitte versuche es später erneut."
    )


def in_progress(text, core, skills):
    if "einkaufsliste" in text:
        core.say(
            'Die Einkaufsliste trennt die einzelnen Items bei jedem "und". Daher musst du diese auch mit und '
            + "trennen, ansonsten werden diese zusammengezogen. Versuch doch mal folgende Syntax: Core, setz Butter "
            + "und 500g Rinderhack und Marmelade auf die Einkaufsliste."
        )

    elif "akinator" in text or "ratespiel" in text or "wer bin ich" in text:
        core.say(
            "Um dieses Spiel zu beginnen, musst du zunächst sagen: Jarvis, starte wer bin ich! Anschließend wird "
            + "dir das Modul weitere Instruktionen geben."
        )
