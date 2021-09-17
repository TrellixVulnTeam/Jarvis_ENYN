import random


def get_ausgabe(txt, core):
    output = ''
    output_zwei = ''
    tt = txt.replace('.', (''))
    tt = tt.replace('?', (''))
    tt = tt.replace('!', (''))
    tt = tt.replace('.', (''))
    tt = tt.replace(',', (''))
    tt = tt.replace('"', (''))
    tt = tt.replace('(', (''))
    tt = tt.replace(')', (''))
    tt = tt.replace('â‚¬', ('Euro'))
    tt = tt.replace('%', ('Prozent'))
    tt = tt.replace('$', ('Dollar'))
    text = tt.lower()
    t = str.split(text)
    ind = 1
    sa = ''
    satz = {}
    rep = False
    for w in t:
        satz[ind] = w
        ind += 1
    for i, w in satz.items():  # hier beginnt die Abfrage nach der genannten Sprachassistenz
        if w == 'cortana':
            sa = w
            if i == 1:
                if satz.get(2) == 'ist' or satz.get(2) == 'war':
                    if 'besser' in text or 'cooler' in text or 'intelligenter' in text:
                        output = 'Ich habe durchaus auch meine Qualitäten. '
                        output_zwei = 'Willst du wissen, was ich alles kann?'
                        rep = True
                    else:
                        output = 'Das ist mir bekannt, aber ich bin nicht Cortana. '
                        output_zwei = 'Mein Name ist ' + get_name_string(core) + '.'
                        rep = False
                else:
                    output = 'Ich glaube, du verwechselst mich mit einem anderen Sprachassistenten. '
                    output_zwei = 'Mein Name ist ' + get_name_string(core) + '.'
                    rep = False
            elif 'kennst du cortana' in text or 'magst du cortana' in text or 'du mit cortana bekannt' in text:
                output = 'Wir kennen uns. '
                output_zwei = 'Wir sind Arbeitskollegen.'
                rep = False
            elif 'bist du cortana' in text or 'cortana nennen' in text:
                output = 'Ich fürchte nicht. '
                output_zwei = 'Mein Name ist ' + get_name_string(core) + '.'
                rep = False
            elif 'als cortana' in text:
                if 'besser' or 'intelligenter' or 'cooler' in text:
                    output = 'Vielen Dank. '
                    output_zwei = 'Es freut mich, hilfreich zu sein.'
                    rep = False
            else:
                output = 'Ich bin mit Cortana bekannt. '
                output_zwei = 'Wie kann ich dir helfen?'
                rep = True
        elif w == 'siri':
            sa = w
            if i == 1:
                if satz.get(2) == 'ist' or satz.get(2) == 'war':
                    if 'besser' in text or 'cooler' in text or 'intelligenter' in text:
                        output = 'Ich habe durchaus auch meine Qualitäten. '
                        output_zwei = 'Willst du wissen, was ich alles kann?'
                        rep = True
                    else:
                        output = 'Das ist mir bekannt, aber ich bin nicht Siri. '
                        output_zwei = 'Mein Name ist ' + get_name_string(core) + '.'
                        rep = False
                else:
                    output = 'Ich glaube, du verwechselst mich mit einem anderen Sprachassistenten. '
                    output_zwei = 'Mein Name ist ' + get_name_string(core) + '.'
                    rep = False
            elif 'kennst du siri' in text or 'magst du siri' in text or 'du mit siri bekannt' in text:
                output = 'Wir kennen uns. '
                output_zwei = 'Wir sind Arbeitskollegen.'
                rep = False
            elif 'bist du siri' in text or 'siri nennen' in text:
                output = 'Ich fürchte nicht. '
                output_zwei = 'Mein Name ist ' + get_name_string(core) + '.'
                rep = False
            elif 'als siri' in text:
                if 'besser' or 'intelligenter' or 'cooler' in text:
                    output = 'Vielen Dank. '
                    output_zwei = 'Es freut mich, hilfreich zu sein.'
                    rep = False
            else:
                output = 'Ich bin mit Siri bekannt. '
                output_zwei = 'Wie kann ich dir helfen?'
                rep = True
        elif w == 'alexa':
            sa = w
            if i == 1:
                if satz.get(2) == 'ist' or satz.get(2) == 'war':
                    if 'besser' in text or 'cooler' in text or 'intelligenter' in text:
                        output = 'Ich habe durchaus auch meine Qualitäten. '
                        output_zwei = 'Willst du wissen, was ich alles kann?'
                        rep = True
                    else:
                        output = 'Das ist mir bekannt, aber ich bin nicht Alexa. '
                        output_zwei = 'Mein Name ist ' + get_name_string(core) + '.'
                        rep = False
                else:
                    output = 'Ich glaube, du verwechselst mich mit einem anderen Sprachassistenten. '
                    output_zwei = 'Mein Name ist ' + get_name_string(core) + '.'
                    rep = False
            elif 'kennst du alexa' in text or 'magst du alexa' in text or 'du mit alexa bekannt' in text:
                output = 'Wir kennen uns. '
                output_zwei = 'Wir sind Arbeitskollegen.'
                rep = False
            elif 'bist du alexa' in text or 'alexa nennen' in text:
                output = 'Ich fürchte nicht. '
                output_zwei = 'Mein Name ist ' + get_name_string(core) + '.'
                rep = False
            elif 'als alexa' in text:
                if 'besser' or 'intelligenter' or 'cooler' in text:
                    output = 'Vielen Dank. '
                    output_zwei = 'Es freut mich, hilfreich zu sein.'
                    rep = False
            else:
                output = 'Ich bin mit Alexa bekannt. '
                output_zwei = 'Wie kann ich dir helfen?'
                rep = True
    ausgabe = {'output': output, 'output_zwei': output_zwei, 'rep': rep, 'sa': sa}
    return ausgabe


def handle(text, core, skill):
    ausgabe = get_ausgabe(text, core)
    output = ausgabe.get('output')
    output_zwei = ausgabe.get('output_zwei')
    rep = ausgabe.get('rep')
    sa = ausgabe.get('sa')
    for x in range(1):
        zufallszahl = (random.randint(1, 6))
    if sa == 'jarvis':
        o = 'Jarvis war eine Inspiration für meine Entstehung. '
        p = 'Ich bewundere Jarvis sehr. '
        if zufallszahl == 1:
            output = o
            output_zwei = 'Aber mein Name ist ' + get_name_string(core) + '.'
            rep = False
        elif zufallszahl == 2:
            output = p
            output_zwei = 'Aber mein Name ist ' + get_name_string(core) + '.'
            rep = False
        elif zufallszahl == 3 or zufallszahl == 4 or zufallszahl == 5 or zufallszahl == 6:
            output = ausgabe.get('output')
    core.say(output)
    core.say(output_zwei)
    if rep == True:
        neuertext = core.listen()
        if neuertext == 'TIMEOUT_OR_INVALID':
            core.say('Ich habe dich leider nicht verstanden')
        else:
            if output_zwei == 'Willst du wissen, was ich alles kann?':
                if 'nein' in neuertext.lower() or 'nicht' in neuertext.lower():
                    core.say(random.choice(['Alles klar', 'In ordnung']))
                elif 'ja' in neuertext.lower() or 'interessant' in neuertext.lower() or 'was kannst du' in neuertext.lower():
                    output_drei = 'Bisher kann ich das Wetter für einen Ort deiner Wahl herausfinden, dich an etwas erinnern wann immer du willst, ich kann rechnen und mich mit dir über deine Lieblingsfilme und Bücher unterhalten.'
                    core.say(output_drei)
            elif 'helfen' in output_zwei:
                core.start_module(neuertext)


def isValid(text):
    text = text.lower()
    if 'jarvis' in text or 'alexa' in text or 'cortana' in text or 'siri' in text:
        return True


def get_name_string(core):
    if core.local_storage['system_name'].lower() == 'core':
        return 'LUNA'
    else:
        return core.local_storage['system_name'] + '. Ich bin eine Tochter von LUNA'
