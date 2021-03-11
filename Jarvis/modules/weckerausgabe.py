import os

SECURE = True # Damit es von fortlaufenden module naufgerufen werden kann

def handle(text, luna, profile):
    ton = text.get('Ton')
    path = luna.path + "/modules/resources/clock_sounds/" + ton
    
    if luna.local_storage['module_storage']['phillips_hue']['Bridge-IP'] != '':
        luna.start_module(name='phillips_hue', text='Mach das Licht weiß')
    luna.play(path=path)

def isValid(text):
    return False
