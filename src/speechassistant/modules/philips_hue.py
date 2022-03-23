from src.speechassistant.resources.services.light_systems.Phue import PhilipsWrapper

# !!! When a color is added, it is essential that it is also added to Intents.json !!!
colors = ['blau', 'rot', 'gelb', 'grün', 'pink', 'lila', 'türkis', 'weiß', 'orange', 'warmweiß']
# color_code = ['0000ff', 'ff0000', 'ffff00', '00FF00', 'ff1493', '9400d3', '00ffff', 'ffffff', '006400', '8b4513', 'ff8c00',
#        'F5DA81']
color_code = [[0.1548, 0.1117], [0.6778, 0.3017], [0.439, 0.4446], [0.2015, 0.6763], [0.5623, 0.2457], [0.2398, 0.1197],
              [0.1581, 0.2367], [0.3146, 0.3304], [0.588, 0.386], [0.4689, 0.4124]]


def isValid(text):
    text = text.lower()
    colors = ['blau', 'rot', 'gelb', 'grün', 'pink', 'lila', 'türkis', 'weiss', 'dunkelgrün', 'braun', 'orange',
              'warmweiss']
    if ('mach' in text or 'licht' in text) and (
            'an' in text or 'aus' in text or 'heller' in text or 'dunkler' in text or '%' in text or 'prozent' in text) \
            and not 'fernseh' in text:
        return True
    for item in colors:
        if item in text and 'licht' in text:
            return True


def handle(text, core, skills):
    # toDo
    pw = PhilipsWrapper(core)
    pw.wrapper(text)

