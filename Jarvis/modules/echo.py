SECURE = True

def isValid(text):
    return text.lower().startswith('wiederhole')

def handle(text, luna, skill):
    luna.say(str(' '.join(text.split(' ')[1:])), output='telegram_speech')
