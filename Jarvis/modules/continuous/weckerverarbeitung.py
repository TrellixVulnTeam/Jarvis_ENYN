import datetime

INTERVALL = 2

def run(core, profile):
    now = datetime.datetime.now()
    if 'Wecker' in core.local_storage.keys():
        erinnerungen = core.local_storage.get('Wecker')
        for item in erinnerungen:
            zeit = item['Zeit']
            '''zeit = datetime.datetime.strptime(zeit, '%Y-%m-%d %H:%M:%S.%f')'''
            differenz = zeit - now
            if differenz.total_seconds() <= 0:
                ausgabe = 'Guten Morgen. Ich hoffe, du hast gut geschlafen'
                """
                try:
                    geburtsdatum = core.local_storage['geburtstage']['date']
                    month = int(geburtsdatum['month'])
                    day = int(geburtsdatum['day'])
                    now = datetime.datetime.now()
                    if now.month == month and now.day == day:
                        ausgabe = 'Herzlichen Glückwunsch zum Geburtstag. Ich hoffe, du hast einen großartigen Tag.'
                except KeyError:
                    '''Do nothing'''
                """
                ton = "morgen_ihr_luschen.wav"
                dic = {'Text': ausgabe, 'Ton': ton, 'User': core.user}
                core.start_module(name='weckerausgabe', text=dic)
                erinnerungen.remove(item)
                core.local_storage['Wecker'] = erinnerungen
