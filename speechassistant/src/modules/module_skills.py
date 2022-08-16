from __future__ import annotations

import logging
import re
from datetime import datetime, timedelta

from geopy.geocoders import Nominatim
from geopy.location import Location

from src.enums import OutputTypes


class Statics:
    def __init__(self) -> None:
        # Colors
        self.color_ger_to_eng = {
            "schwarz": "black",
            "blau": "blue",
            "rot": "red",
            "gelb": "yellow",
            "grün": "green",
        }

        self.color_eng_to_ger = {
            "black": "schwarz",
            "blue": "blau",
            "red": "rot",
            "yellow": "gelb",
            "green": "grün",
        }

        # Weekdays
        self.weekdays = [
            "Montag",
            "Dienstag",
            "Mittwoch",
            "Donnerstag",
            "Freitag",
            "Samstag",
            "Sonntag",
        ]
        self.weekdays_engl = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        self.weekdays_ger_to_eng = {
            "montag": "monday",
            "dienstag": "tuesday",
            "mittwoch": "wednesday",
            "donnerstag": "thursday",
            "freitag": "friday",
            "samstag": "saturday",
            "sonntag": "sunday",
        }

        self.weekdays_eng_to_ger = {
            "monday": "montag",
            "tuesday": "dienstag",
            "wednesday": "mittwoch",
            "thursday": "donnerstag",
            "friday": "freitag",
            "saturday": "samstag",
            "sunday": "sonntag",
        }

        self.numb_to_day = {
            "1": "monday",
            "2": "tuesday",
            "3": "wednesday",
            "4": "thursday",
            "5": "friday",
            "6": "saturday",
            "7": "sunday",
        }

        self.numb_to_day_numb = {
            "01": "ersten",
            "02": "zweiten",
            "03": "dritten",
            "04": "vierten",
            "05": "fünften",
            "06": "sechsten",
            "07": "siebten",
            "08": "achten",
            "09": "neunten",
            "10": "zehnten",
            "11": "elften",
            "12": "zwölften",
            "13": "dreizehnten",
            "14": "vierzehnten",
            "15": "fünfzehnten",
            "16": "sechzehnten",
            "17": "siebzehnten",
            "18": "achtzehnten",
            "19": "neunzehnten",
            "20": "zwanzigsten",
            "21": "einundzwanzigsten",
            "22": "zweiundzwanzigsten",
            "23": "dreiundzwanzigsten",
            "24": "vierundzwanzigsten",
            "25": "fünfundzwanzigsten",
            "26": "sechsundzwanzigsten",
            "27": "siebenundzwanzigsten",
            "28": "achtundzwanzigsten",
            "29": "neunundzwanzigsten",
            "30": "dreißigsten",
            "31": "einunddreißigsten",
            "32": "zweiunddreißigsten",
        }

        self.numb_to_hour = {
            "01": "ein",
            "02": "zwei",
            "03": "drei",
            "04": "vier",
            "05": "fünf",
            "06": "sechs",
            "07": "sieben",
            "08": "acht",
            "09": "neun",
            "10": "zehn",
            "11": "elf",
            "12": "zwölf",
            "13": "dreizehn",
            "14": "vierzehn",
            "15": "fünfzehn",
            "16": "sechzehn",
            "17": "siebzehn",
            "18": "achtzehn",
            "19": "neunzehn",
            "20": "zwanzig",
            "21": "einundzwanzig",
            "22": "zweiundzwanzig",
            "23": "dreiundzwanzig",
            "24": "vierundzwanzig",
        }

        self.numb_to_minute = {
            "01": "eins",
            "02": "zwei",
            "03": "drei",
            "04": "vier",
            "05": "fünf",
            "06": "sechs",
            "07": "sieben",
            "08": "acht",
            "09": "neun",
            "10": "zehn",
            "11": "elf",
            "12": "zwölf",
            "13": "dreizehn",
            "14": "vierzehn",
            "15": "fünfzehn",
            "16": "sechzehn",
            "17": "siebzehn",
            "18": "achtzehn",
            "19": "neunzehn",
            "20": "zwanzig",
            "21": "einundzwanzig",
            "22": "zweiundzwanzig",
            "23": "dreiundzwanzig",
            "24": "vierundzwanzig",
            "25": "fünfundzwanzig",
            "26": "sechsundzwanzig",
            "27": "siebenundzwanzig",
            "28": "achtundzwanzig",
            "29": "neunundzwanzig",
            "30": "dreißig",
            "31": "einunddreißig",
            "32": "zweiunddreißig",
            "33": "dreiunddreißig",
            "34": "vierunddreißig",
            "35": "fünfunddreißig",
            "36": "sechsunddreißig",
            "37": "siebenunddreißig",
            "38": "achtunddreißig",
            "39": "neununddreißig",
            "40": "vierzig",
            "41": "einundvierzig",
            "42": "zweiundvierzig",
            "43": "dreiundvierzig",
            "44": "vierundvierzig",
            "45": "fünfundvierzig",
            "46": "sechsundvierzig",
            "47": "siebenundvierzig",
            "48": "achtundvierzig",
            "49": "neunundvierzig",
            "50": "fünfzig",
            "51": "einundfünfzig",
            "52": "zweiundfünfzig",
            "53": "dreiundfünfzig",
            "54": "vierundfünfzig",
            "55": "fünfundfünfzig",
            "56": "sechsundfünfzig",
            "57": "siebenundfünfzig",
            "58": "achtundfünfzig",
            "59": "neunundfünfzig",
        }

        self.numb_to_month = {
            "01": "Januar",
            "02": "Februar",
            "03": "März",
            "04": "April",
            "05": "Mai",
            "06": "Juni",
            "07": "Juli",
            "08": "August",
            "09": "September",
            "10": "Oktober",
            "11": "November",
            "12": "Dezember",
        }

        self.numb_to_ordinal = {
            "1": "erster",
            "2": "zweiter",
            "3": "dritter",
            "4": "vierter",
            "5": "fünfter",
            "6": "sechster",
            "7": "siebter",
            "8": "achter",
            "9": "neunter",
            "10": "zehnter",
            "11": "elfter",
            "12": "zwölfter",
            "13": "dreizehnter",
            "14": "vierzehnter",
            "15": "fünfzehnter",
            "16": "sechzehnter",
            "17": "siebzehnter",
            "18": "achtzehnter",
            "19": "neunzehnter",
            "20": "zwanzigster",
            "21": "einundzwanzigster",
            "22": "zweiundzwanzigster",
            "23": "dreiundzwanzigster",
            "24": "vierundzwanzigster",
            "25": "fünfundzwanzigster",
            "26": "sechsundzwanzigster",
            "27": "siebenundzwanzigster",
            "28": "achtundzwanzigster",
            "29": "neunundzwanzigster",
            "30": "dreißigster",
            "31": "einunddreißigster",
        }


class Skills:
    def __init__(self):
        self.geo_location = Nominatim(user_agent="my_app")
        self.statics: Statics = Statics()

    """ turns an array into an enumeration separated by "," and finally by an "und" ["a", "b", "c"] -> "a, b und c"

    Args:
        array (list): Array to be converted into an enumeration

    Returns:
        string: enumerated text
    """

    @staticmethod
    def get_enumerate(array: list) -> str:
        if type(array) != list:
            logging.debug(f"Get the wrong data type: {type(array)} -> {array}")
            raise ValueError
        result = ", ".join(array)
        result = " und ".join(result.rsplit(", ", 1))
        return result

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
    def get_text_between(start_word: str, text: str, end_word: str = "", output: str = "array",
                         target_included: bool = True) -> str | list:
        if start_word not in text:
            raise ValueError(f"Text does not contain the start_word {start_word}!")
        if end_word == "":
            raise ValueError(f"Text does not contain the end_word {end_word}!")

        start_index = Skills.__get_start_index(start_word, target_included, text)
        target_index = Skills.__get_target_index(end_word, target_included, text)

        result_string = text[start_index:target_index]

        if output == OutputTypes.STRING:
            return result_string
        elif output == OutputTypes.ARRAY:
            return result_string.split(" ")

    @staticmethod
    def __get_start_index(start_word, target_included, text):
        temp_start = re.search(f"{start_word}", text)
        if target_included:
            return temp_start.start()
        else:
            return temp_start.end() + 1

    @staticmethod
    def __get_target_index(end_word, target_included, text):
        if end_word not in text:
            return len(text)
        else:
            temp_end = re.search(f"{end_word}", text)
            if target_included:
                return temp_end.start()
            else:
                return temp_end.end() + 1

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
        hours, minutes = Skills.__get_hour_and_minute_from_time(time)
        return Skills.__convert_time_to_spoken_time(hours, hours % 12, minutes)

    @staticmethod
    def __get_hour_and_minute_from_time(time: datetime | dict) -> tuple[int, int]:
        if type(time) == datetime:
            return time.hour, time.minute
        elif type(time) == dict:
            return time["hour"], time["minute"]
        else:
            raise ValueError("Got time in invalid date format! It has to be datetime or dict.")

    @staticmethod
    def __convert_time_to_spoken_time(hours_24: int, hours_12: int, minutes: int):
        hour_str: str = str(hours_12)
        next_hour_str: str = str((hours_12 + 1) % 12)

        match minutes:
            case 0:
                return str(hours_24) + " Uhr."
            case 5:
                return "fünf nach " + hour_str
            case 10:
                return "zehn nach " + hour_str
            case 15:
                return "viertel nach " + hour_str
            case 20:
                return "zwanzig nach " + hour_str
            case 25:
                return "fünf vor halb " + hour_str
            case 30:
                return "halb " + next_hour_str
            case 35:
                return "fünf nach halb " + next_hour_str
            case 40:
                return "zwanzig vor " + next_hour_str
            case 45:
                return "viertel vor " + next_hour_str
            case 50:
                return "zehn vor " + next_hour_str
            case 55:
                return "fünf vor " + next_hour_str
            case _:
                hour = str(hours_24).rjust(2, "0")
                minute = str(minutes).rjust(2, "0")
                return hour + ":" + minute + " Uhr"

    """ Returns the difference between 2 timestamps as string
    Args:
        start_time  (datetime.time): Timestamp from which the difference is to start
        time    (datetime.time): optional timestamp up to which the time difference should go. If not specified, then it is the current time

    Returns:
        str: time difference
    """

    def get_time_difference(self, start_time: datetime, time: datetime = datetime.now()) -> str:
        years, days, hours, minutes, seconds = self.__split_days_and_seconds_to_time_units(time - start_time)
        output: list[str] = self.__translate_time_units_to_text(years, days, hours, minutes, seconds)
        return self.get_enumerate(output)

    def __translate_time_units_to_text(self, years: int, days: int, hours: int, minutes: int, seconds: int) -> list[
        str]:
        output: list[str] = []

        self.__handle_singular_and_plural(output, years, "einem Jahr", "Jahren")
        self.__handle_singular_and_plural(output, days, "einem Tag", "Tagen")
        self.__handle_singular_and_plural(output, hours, "einer Stunde", "Stunden")
        self.__handle_singular_and_plural(output, minutes, "einer Minute", "Minuten")
        self.__handle_singular_and_plural(output, seconds, "einer Sekunde", "Sekunden")

        return output

    @staticmethod
    def __handle_singular_and_plural(output: list[str], value: int, singular: str, plural: str) -> None:
        if value == 1:
            output.append(singular)
        elif value > 1:
            output.append(f"{value} {plural}")

    @staticmethod
    def __split_days_and_seconds_to_time_units(time_difference: timedelta):
        years: int = 0
        days: int = time_difference.days
        hours: int = 0
        minutes: int = 0
        seconds: int = time_difference.seconds
        microseconds: int = time_difference.microseconds

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
        return years, days, hours, minutes, seconds

    """ Checks whether a user has answered in the affirmative or in the negative

    Args:
        text (string): user input

    Returns:
        bool: True if the user has given hints of consent, otherwise False
    """

    @staticmethod
    def is_desired(text: str) -> bool:
        text = text.lower()
        if "ja" in text or "gern" in text:
            return True
        elif "bitte" in text and "nicht" not in text:
            return True
        elif "danke" in text and "nein" not in text:
            return True
        return False

    """ Returns geological data of a city
    Args:
        city    (str): name of the city from which the data are required
    Returns:
        dict: Dictionary with the values of the city
    """

    def get_data_of_city(self, city: str) -> dict:
        location: Location = self.geo_location.geocode(city)
        return self.__location_to_json(location.raw)

    """ Returns geological data of a city
    Args:
        lat    (int): latutude of the city from which the data are required
        lon    (int): longitude of the city from which the data are required
    Returns:
        dict: Dictionary with the values of the city
    """

    def get_data_of_lat_lon(self, lat: float, lon: float) -> dict:
        location = self.geo_location.reverse(f"{lat}, {lon}")
        return self.__location_to_json(location.raw)

    @staticmethod
    def __location_to_json(location: dict) -> dict:
        display_name = location["display_name"].split(", ")
        return {
            "city": display_name[0],
            "state": display_name[1],
            "county": display_name[2],
            "lat": location["lat"],
            "lon": location["lon"],
        }


if __name__ == "__main__":
    skills = Skills()
