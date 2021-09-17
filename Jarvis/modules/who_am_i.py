import random


def handle(text, core, skills):
    '''
    if core.user is not None:
        if not core.user == 'Unknown':
            responses = ['Wenn mich nicht alles täuscht bist du {}',
                         'Ich glaube du bist {}',
                         'Soweit ich das sehen kann bist du {}']
            response = random.choice(responses)
            core.say(response.format(core.user))
            return
    responses = ['Das kann ich gerade leider nicht sehen',
                 'Das musst du aktuell leider selbst wissen',
                 'Entschuldige, aber das kann ich leider gerade nicht beurteilen']
    core.say(random.choice(responses))'''
    core.say("Die Nutzererkennung ist leider derzeit in Arbeit, daher kann ich das noch nicht sagen.")


def isValid(text):
    text = text.lower()
    if 'wer' in text and 'bin' in text and 'ich' in text:
        return True
    if 'wie' in text and 'heiße' in text and 'ich' in text:
        return True
