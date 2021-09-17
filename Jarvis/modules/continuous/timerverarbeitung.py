import datetime

INTERVALL = 2


def run(core, profile):
    now = datetime.datetime.now()
    if 'Timer' in core.local_storage.keys():
        timer = core.local_storage.get('Timer')
        try:
            for item in timer:
                benutzer = item['Benutzer']
                zeit = item['Zeit']
                differenz = zeit - now
                if differenz.total_seconds() <= 0:
                    output = item['Text']
                    ausgabe = output
                    dic = {'Text': ausgabe, 'Benutzer': benutzer, 'Dauer': item['Dauer']}
                    core.start_module(user=benutzer, name='timerausgabe', text=dic)
                    timer.remove(item)
                    core.local_storage['Timer'] = timer
        except RuntimeError:
            core.local_storage['Timer'] = []
