import datetime

INTERVALL = 2


def run(core, profile):
    now = datetime.datetime.now()
    if 'Erinnerungen' in core.local_storage.keys():
        reminder = core.local_storage.get('Erinnerungen')
        for item in reminder:
            user = item['Benutzer']
            output = item['Text']
            zeit = item['Zeit']
            '''zeit = datetime.datetime.strptime(zeit, '%Y-%m-%d %H:%M:%S.%f')'''
            if 'dass ' in output:
                output = 'Ich sollte dir Bescheid sagen, ' + output + '.'
            else:
                output = 'Ich sollte dich ans ' + output + ' erinnern'
            time_diff = zeit - now
            dic = {'Text': output, 'Benutzer': user}
            if time_diff.total_seconds() <= 0:
                core.start_module(user=user, name='erinnerungsausgabe', text=dic)
                reminder.remove(item)
                core.local_storage['Erinnerungen'] = reminder
