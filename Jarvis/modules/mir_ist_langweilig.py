import random


def handle(text, core, skills):
    core.say('Soll ich dir was interessantes erzählen?')
    response = core.listen()
    if 'ja' in response or 'sehr gerne' in response:
        options = ['witz', 'fun fact', 'zungenbrecher', 'phobie', 'gedicht']
        text = 'erzähl mir einen ' + random.choice(options)
        handle(text, core, skills)
    else:
        answer = ['Alles klar, vielleicht findest du ja eine Beschäftigung.']
    core.say(answer)
