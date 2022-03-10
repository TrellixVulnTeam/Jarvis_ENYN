import datetime

def isValid(text):
    # toDo
    return False

def handle(text, core, skills):
    ts = datetime.datetime.now()
    if not has_dateutil:
        heute = ts.strftime('%d %b %Y')
        diff = datetime.datetime.strptime(heute, '%d %b %Y') - datetime.datetime.strptime('6 Feb 2020',
                                                                                          '%d %b %Y')
        daynr = diff.days
        answer = ['{} Tage seit den ersten Tests.'.format(daynr)]
    else:
        geburtsdatum = datetime.datetime.strptime('6 Mai 2020', '%d %b %Y')
        heute = datetime.datetime.strptime(ts.strftime('%d %b %Y'), '%d %b %Y')
        diff = relativedelta.relativedelta(heute, geburtsdatum)
        output_year = ''
        if diff.years == 1:
            output_year = 'Ein Jahr'
        elif diff.years > 0:
            output_year = '{} Jahre'.format(diff.years)

        output_month = ''
        if diff.months == 1:
            output_month = 'Einen Monat'
        elif diff.months > 0:
            output_month = '{} Monate'.format(diff.months)

        output_days = ''
        if diff.days == 1:
            output_days = 'Einen Tag'
        elif diff.days > 0:
            output_days = '{} Tage'.format(diff.days)

        output = ''
        if output_year != '':
            output = output + output_year

        if output_month != '':
            if output != '':
                if (output_days == ''):
                    output = output + ' und '
                else:
                    output = output + ', '
            output = output + output_month

        if output_days != '':
            if output != '':
                output = output + ' und '
            output = output + output_days

        if (output == ''):
            answer = ['Hast du deine Systemzeit verstellt? Heute sind nicht die ersten Tests.']
        else:
            answer = ['{} seit den ersten Tests.'.format(output)]