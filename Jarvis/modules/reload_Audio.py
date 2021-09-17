def isValid(text):
    if 'lad' in text and 'audio' in text:
        return True


def handle(text, core, skills):
    if 'output' in text or 'ausgabe' in text:
        restart_output(core)
        output = 'Die Audioausgabe wurde neu gestartet.'
    elif 'input' in text or 'eingabe' in text:
        restart_input(core)
        output = 'Die Audioeingabe wurde neu gestartet.'
    else:
        restart_input(core)
        restart_output(core)
        output = 'Die Audiotreiber wurden neu gestartet.'

    core.say(output)


def restart_output(core):
    core.core.Audio_Output.stop()
    core.core.Audio_Output.start()


def restart_input(core):
    core.core.Audio_Input.stop()
    core.core.Audio_Input.start()
