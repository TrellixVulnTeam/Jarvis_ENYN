SECURE = True


def isValid(text):
    return text.lower().startswith('wiederhole')


def handle(text, core, skill):
    core.say(str(' '.join(text.split(' ')[1:])), output='messenger_speech')
