import random


def handle(text, core, skills):
    answers = ['Danke, gut!',
               'Mir gehts gut, {}.'.format(core.user["name"]),
               'Alles gut, {}.'.format(core.user["name"])]
    reply = core.listen(text=random.choice(answers) + 'Und wie geht es dir?').lower()
    if 'nicht so' in reply or 'schlecht' in reply or 'müde' in reply or 'mies' in reply or 'suboptimal' in reply:
        answer = ['Das ist blöd, aber denk immer daran: Alles hat ein Ende nur die Wurst hat zwei!']
    elif 'gut' in reply or 'besser' in reply or 'bestens' in reply or 'super' in reply or 'wundervoll' in reply or 'glücklich' in reply or 'froh' in reply:
        answer = ['Das freut mich!']
    else:
        answer = ['Ich fürchte, ich konnte dich nicht verstehen. Geht es dir so schlecht?']
    core.say(random.choice(answer))