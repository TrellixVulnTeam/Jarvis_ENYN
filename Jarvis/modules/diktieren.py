import os
import re
import subprocess
import tempfile

TEXT_EDITOR = 'xdotool'

DELETE = re.compile(
    r'(lösch|entfern)e?n? (\d+|eins?|zwei|drei|vier|fünf|sechs|sieben|acht|neun|zehn|elf|zwölf) zeichen', re.I)

WORDS = ['diktier', 'text']


def isValid(text):
    text = text.lower().strip()
    if TEXT_EDITOR is 'xdotool':
        try:
            installedStr = subprocess.check_output(
                "dpkg-query --show --showformat='${db:Status-Status}\n' 'xdotool'", shell=True).decode(
                'utf-8').lower()
            if not 'installed' in installedStr or 'not' in installedStr:
                return False
        except subprocess.CalledProcessError:
            return False
    if ('text' in text and 'diktier' in text):
        return True
    else:
        return False


def getnum(str):
    map = {
        'ein': '1',
        'eins': '1',
        'zwei': '2',
        'drei': '3',
        'vier': '4',
        'fünf': '5',
        'sechs': '6',
        'sieben': '7',
        'acht': '8',
        'neun': '9',
        'zehn': '10',
        'elf': '11',
        'zwölf': '12'
    }
    return map.get(str.lower(), str)


def handle(text, core, skill):
    core.say('Dann leg mal los.')
    body = []
    text = core.listen().strip()
    while (text.lower() != 'stop' and text.lower() != 'stopp' and text.lower() != 'fertig'):
        if text != '' and text != 'TIMEOUT_OR_INVALID':
            if TEXT_EDITOR is 'xdotool':
                match = DELETE.match(text)
                if match is not None:
                    subprocess.call(['xdotool', 'key', '--repeat', getnum(match.group(2)), '--delay', '0', 'BackSpace'])
                elif (text.lower() == 'neue zeile' or text.lower() == 'enter'):
                    subprocess.call(['xdotool', 'key', '--delay', '0', 'Return'])
                else:
                    if text[-1].isalpha() or text[-1].isdigit():
                        text = text + '.'
                    text = text + ' '
                    if text[0].isalpha():
                        text = text[0].upper() + text[1:]
                    subprocess.call(['xdotool', 'type', '--delay', '0', text])
        else:
            body.append(text)
        text = core.listen().strip()
    if TEXT_EDITOR is 'xdotool':
        core.say('Es war mir eine Freude, dir zu helfen.')
    else:
        core.end_Conversation()
        try:
            file = tempfile.NamedTemporaryFile(mode='w', delete=False)
            for line in body:
                file.write(line + '\n')
            file.close()
            os.system(TEXT_EDITOR + ' "' + file.name + '"')
        except IOError:
            core.say('Es ist ein Fehler aufgetreten.')
