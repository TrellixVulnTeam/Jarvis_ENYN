from __future__ import annotations

from datetime import datetime
import logging
import re
from geopy.geocoders import Nominatim


class Skills:
    def __init__(self):
        self.geo_location = Nominatim(user_agent="my_app")

    """ turns an array into an enumeration separated by "," and finally by an "und" ["a", "b", "c"] -> "a, b und c"

    Args:
        array (list): Array to be converted into an enumeration

    Returns:
        string: enumerated text
    """

    @staticmethod
    def get_enumerate(array: list) -> str:
        if type(array) != list:
            logging.warning(f'Get the wrong data type: {type(array)} -> {array}')
            raise ValueError
        result = ''
        for i in range(len(array) - 1):
            result += array[i] + ', '
        return result[0:len(result) - 2] + ' und ' + array[len(array) - 1]

    """ Returns a text starting from one word or between 2 words as array or string

    Args:
        start_word  (string): Word from which the string should start
        text        (string): user input
        end_word    (string): Word up to which the text should go
        output      (string): (string | array) -> Specifies in which format the result should be returned.
        included    (bool)  : if True, the start- and end-word will be included, otherwise excluded

    Returns:
        list: If output is set to "array"
        str:  If output is set to "string"
    """

    @staticmethod
    def get_text_between(start_word: str, text: str, end_word: str = '', output: str = 'array',
                         could_included: bool = True) -> str | list:
        if not start_word in text:
            start_index = 0
        else:
            temp_start = re.search(f'{start_word}', text)
            if could_included:
                start_index = temp_start.start()
            else:
                start_index = temp_start.end() + 1  # the space character should also be deleted

        if end_word == '' or not end_word in text:
            end_index = len(text)
        else:
            temp_end = re.search(f'{end_word}', text)
            if could_included:
                end_index = temp_end.start()
            else:
                end_index = temp_end.end() + 1  # the space character should also be deleted
        result_string = text[start_index:end_index]
        if output == 'string':
            return result_string
        else:
            return result_string.split(' ')

    """ Returns an array without duplicate elements
    Args:
        array   (list): Array to be filtered

    Returns:
        list: filtered array
    """

    @staticmethod
    def delete_duplications(array: list) -> list:
        return list(set(array))

    """ returns the time of a DateTime object as a string respecting the German grammar
    Args:
        time    (datetime.time | dict): time to be transcribed

    Returns:
        str: time as string
    """

    @staticmethod
    def get_time(time: datetime | dict) -> str:
        if isinstance(time, datetime):
            hour = time.hour
            minute = time.minute
        else:
            hour = time["hour"]
            minute = time["minute"]

        hour_str = str(hour % 12)
        next_hour_str = str((hour + 1) % 12)

        if minute == 0:
            output = str(hour) + ' Uhr.'
        elif minute == 5:
            output = 'fünf nach ' + hour_str
        elif minute == 10:
            output = 'zehn nach ' + hour_str
        elif minute == 15:
            output = 'viertel nach ' + hour_str
        elif minute == 20:
            output = 'zwanzig nach ' + hour_str
        elif minute == 25:
            output = 'fünf vor halb ' + hour_str
        elif minute == 30:
            output = 'halb ' + next_hour_str
        elif minute == 35:
            output = 'fünf nach halb ' + next_hour_str
        elif minute == 40:
            output = 'zwanzig vor ' + next_hour_str
        elif minute == 45:
            output = 'viertel vor ' + next_hour_str
        elif minute == 50:
            output = 'zehn vor ' + next_hour_str
        elif minute == 55:
            output = 'fünf vor ' + next_hour_str
        else:
            hour = str(hour) if hour > 9 else '0' + str(hour)
            minute = str(minute) if minute > 9 else '0' + str(minute)
            output = hour + ':' + minute + ' Uhr'

        return output

    """ Returns the difference between 2 timestamps as string
    Args:
        start_time  (datetime.time): Timestamp from which the difference is to start
        time    (datetime.time): optional timestamp up to which the time difference should go. If not specified, then it is the current time

    Returns:
        str: time difference
    """

    def get_time_differenz(self, start_time: datetime, time: datetime = datetime.now()) -> str:
        aussage = []

        time_difference = time - start_time
        days = time_difference.days
        seconds = time_difference.seconds
        microseconds = time_difference.microseconds

        years = 0
        hours = 0
        minutes = 0

        if days >= 365:
            years = int(days / 365)
            days = days % 365
        if seconds >= 3600:
            hours = int(seconds / 3600)
            seconds = seconds % 3600
        if seconds >= 60:
            minutes = int(seconds / 60)
            seconds = seconds % 60
        if microseconds >= 5:
            seconds += 1

        if years == 1:
            aussage.append('einem Jahr')
        elif years > 1:
            aussage.append(str(years) + ' Jahren')
        if days == 1:
            aussage.append('einem Tag')
        elif days > 1:
            aussage.append(str(days) + ' Tagen')
        if hours == 1:
            aussage.append('einer Stunde')
        elif hours > 1:
            aussage.append(str(hours) + ' Stunden')
        if minutes == 1:
            aussage.append('einer Minute')
        elif minutes > 1:
            aussage.append(str(minutes) + ' Minuten')
        if seconds == 1:
            aussage.append('einer Sekunde')
        elif seconds > 1:
            aussage.append(str(seconds) + ' Sekunden')
        return self.get_enumerate(aussage)

    """ Checks whether a user has answered in the affirmative or in the negative

    Args:
        text (string): user input

    Returns:
        bool: True if the user has given hints of consent, otherwise False
    """

    @staticmethod
    def is_desired(text: str) -> bool:
        text = text.lower()
        if 'ja' in text or 'gern' in text or ('bitte' in text and 'nicht' not in text):
            return True
        elif 'bitte' in text and 'nicht' not in text:
            return True
        elif 'danke' in text and 'nein' not in text:
            return True
        return False

    """ Returns geological data of a city
    Args:
        city    (str): name of the city from which the data are required
    Returns:
        dict: Dictionary with the values of the city
    """

    def get_data_of_city(self, city: str) -> dict:
        location = self.geo_location.geocode(city)
        return self.__location_to_json(location.raw)

    """ Returns geological data of a city
    Args:
        lat    (int): latutude of the city from which the data are required
        lon    (int): longitude of the city from which the data are required
    Returns:
        dict: Dictionary with the values of the city
    """

    def get_data_of_lat_lon(self, lat: int, lon: int) -> dict:
        location = self.geo_location.reverse((lat, lon))
        return self.__location_to_json(location)

    @staticmethod
    def __location_to_json(location: dict) -> dict:
        display_name = location["display_name"].split(', ')
        return {
            "city": display_name[0],
            "state": display_name[1],
            "county": display_name[2],
            "lat": location["lat"],
            "lon": location["lon"],
        }

    class Statics:
        def __init__(self) -> None:
            # Colors
            self.color_ger_to_eng = {
                "schwarz": "black",
                "blau": "blue",
                "rot": "red",
                "gelb": "yellow",
                "grün": "green"
            }

            self.color_eng_to_ger = {
                "black": "schwarz",
                "blue": "blau",
                "red": "rot",
                "yellow": "gelb",
                "green": "grün"
            }

            # Weekdays
            self.weekdays = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
            self.weekdays_engl = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

            self.weekdays_ger_to_eng = {
                'montag': 'monday',
                'dienstag': 'tuesday',
                'mittwoch': 'wednesday',
                'donnerstag': 'thursday',
                'freitag': 'friday',
                'samstag': 'saturday',
                'sonntag': 'sunday'
            }

            self.weekdays_eng_to_ger = {
                'monday': 'montag',
                'tuesday': 'dienstag',
                'wednesday': 'mittwoch',
                'thursday': 'donnerstag',
                'friday': 'freitag',
                'saturday': 'samstag',
                'sunday': 'sonntag'
            }

            self.numb_to_day = {
                "1": "monday",
                "2": "tuesday",
                "3": "wednesday",
                "4": "thursday",
                "5": "friday",
                "6": "saturday",
                "7": "sunday"}

            self.numb_to_day_numb = {'01': 'ersten', '02': 'zweiten', '03': 'dritten', '04': 'vierten', '05': 'fünften',
                                '06': 'sechsten', '07': 'siebten', '08': 'achten', '09': 'neunten', '10': 'zehnten',
                                '11': 'elften', '12': 'zwölften', '13': 'dreizehnten', '14': 'vierzehnten',
                                '15': 'fünfzehnten',
                                '16': 'sechzehnten', '17': 'siebzehnten', '18': 'achtzehnten', '19': 'neunzehnten',
                                '20': 'zwanzigsten',
                                '21': 'einundzwanzigsten', '22': 'zweiundzwanzigsten', '23': 'dreiundzwanzigsten',
                                '24': 'vierundzwanzigsten',
                                '25': 'fünfundzwanzigsten', '26': 'sechsundzwanzigsten', '27': 'siebenundzwanzigsten',
                                '28': 'achtundzwanzigsten',
                                '29': 'neunundzwanzigsten', '30': 'dreißigsten', '31': 'einunddreißigsten',
                                '32': 'zweiunddreißigsten'}

            self.numb_to_hour = {'01': 'ein', '02': 'zwei', '03': 'drei', '04': 'vier', '05': 'fünf', '06': 'sechs',
                            '07': 'sieben', '08': 'acht', '09': 'neun', '10': 'zehn', '11': 'elf', '12': 'zwölf',
                            '13': 'dreizehn', '14': 'vierzehn', '15': 'fünfzehn', '16': 'sechzehn', '17': 'siebzehn',
                            '18': 'achtzehn', '19': 'neunzehn', '20': 'zwanzig', '21': 'einundzwanzig',
                            '22': 'zweiundzwanzig',
                            '23': 'dreiundzwanzig', '24': 'vierundzwanzig'}

            self.numb_to_month = {'01': 'Januar', '02': 'Februar', '03': 'März', '04': 'April', '05': 'Mai', '06': 'Juni',
                             '07': 'Juli', '08': 'August', '09': 'September', '10': 'Oktober', '11': 'November',
                             '12': 'Dezember'}

            self.numb_to_ordinal = {"1": "erster", "2": "zweiter", "3": "dritter", "4": "vierter", "5": "fünfter",
                               "6": "sechster", "7": "siebter", "8": "achter", "9": "neunter", "10": "zehnter",
                               "11": "elfter", "12": "zwölfter", "13": "dreizehnter", "14": "vierzehnter",
                               "15": "fünfzehnter", "16": "sechzehnter", "17": "siebzehnter", "18": "achtzehnter",
                               "19": "neunzehnter", "20": "zwanzigster"}


if __name__ == "__main__":
    skills = Skills()
