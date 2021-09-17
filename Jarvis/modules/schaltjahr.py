import datetime


def isValid(text):
    text = text.lower()
    if 'ist' in text and 'schaltjahr' in text:
        return True
    elif 'wann' in text and 'schaltjahr' in text:
        return True


def handle(text, core, skills):
    text = text.lower()
    if 'wann' in text and ('nächste' in text or 'wieder' in text):
        year = datetime.date.today().year + 1
        while True:
            if leap_year(year) is True:
                core.say('Das nächste Schaltjahr ist {}'.format(year))
                break
            else:
                year += 1
    elif 'ist' in text and 'schaltjahr' in text:
        ist_schaltjahr = leap_year(get_year(text))
        output = 'vielleicht ein'
        if ist_schaltjahr is True:
            output = 'ein'
        else:
            output = 'kein'
        core.say('Das Jahr {} ist {} Schaltjahr.'.format(get_year(text), output))
    else:
        core.say('Ich habe nicht verstanden, was du im Zusammenhang mit Schaltjahren wissen möchtest.')


def get_year(text):
    year = -1
    text = text.split(' ')
    for item in text:
        try:
            year = int(item)
        except ValueError:
            pass

    return year


def leap_year(y):
    is_leap_year = False
    if y % 400 == 0:
        is_leap_year = True
    if y % 100 == 0:
        is_leap_year = False
    if y % 4 == 0:
        is_leap_year = True
    return is_leap_year
