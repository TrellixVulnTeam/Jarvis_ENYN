PRIORITY = -2

def isValid(text):
    text = text.lower()
    if 'danke' in text or 'thx' in text or 'thanks' in text:
        return True

def handle(text, luna, skills):
    luna.say('[Gerne doch|Keine Ursache].')
