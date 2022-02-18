import logging
from threading import Thread
from datetime import datetime
import requests
import time


class Weather:
    def __init__(self, _api_key, _city, _skills):
        self.__api_key = _api_key
        self.__minutely_forecast = None
        self.__hourly_forecast = None
        self.__daily_forcast = None
        self.__sunrise_sunset = None
        self.__skills = _skills
        self.__geo_data = self.__skills.get_data_of_city(_city)
        self.__last_updated = datetime.now()
        self.city = _city
        self.old_weather_inf = []
        self.current_weather = None

        self.updating = True

    def start(self):
        logging.info("[ACTION] Starting weather module...")
        thr = Thread(target=self.run)
        thr.daemon = True
        thr.start()

    def run(self):
        while self.updating:
            self.__update_all()
            time.sleep(3600)

    def get_current_weather(self, city_name=None, lat=None, lon=None):
        if city_name is not None:
            return self.__get_current_weather(city_name)
        elif lat is not None and lon is not None:
            city_name = self.__skills.get_data_of_lat_lan(lat, lon)["city"]
            return self.__get_current_weather(city_name)
        else:
            self.__update_all()
            return self.current_weather

    def get_forcast_of_one_day(self, day_offset, city_name=None, lat=None, lon=None):
        if day_offset > 7:
            raise ValueError("Day offset was higher than 7.")
        if city_name is None and lat is None and lon is None:
            return self.__daily_forcast[day_offset]
        else:
            if city_name is not None:
                geo_data = self.__skills.get_data_of_city(self.city)
                lat = geo_data["lat"]
                lon = geo_data["lon"]
            URL = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly&appid={self.__api_key}&lang=de&units=metric'
            data = requests.get(URL).json()
            return data["daily"][day_offset]

    def get_forcast_of_range(self, from_offset, until_offset, lat=None, lon=None):
        pass

    def get_sunrise_sunset(self, city_name=None, day_offset=0):
        if city_name is None:
            data = self.__current_weather["sys"]
        else:
            URL = f'api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={self.__api_key}&lang=de'
            data = requests.get(URL).json()["sys"]
        return {data["sunrise"], data["sunset"]}

    def get_current_weather_string(self, city=None, lat=None, lon=None):
        _current_weather = self.get_current_weather(city, lat, lon)
        weather_id = _current_weather["weather"]["0"]["id"]
        weather_description = "Es gab leider ein Problem in der Analyse der Wetterdaten. Bitte versuche es zu einem " \
                              "späteren Zeitpunkt erneut! "
        temp_inf = f'bei einer Höchsttemperatur von {int(_current_weather["temp"]["max"])}°C und einer ' \
                   f'Tiefsttemperatur von {int(_current_weather["temp"]["max"])}°C '
        if weather_id in self.Statics.will_be_description_map.keys():
            weather_description = f'In {city} wird es {self.Statics.will_be_description_map.get(weather_id)} {temp_inf} geben.'
        elif weather_id in self.Statics.give_description_map.keys():
            weather_description = f'In {city} gibt es {self.Statics.give_description_map.get(weather_id)} {temp_inf}.'
        elif weather_id in self.Statics.will_description_map.keys():
            weather_description = f'In {city} wird es {self.Statics.will_description_map.get(weather_id)} {temp_inf}.'
        return weather_description

    def get_forecast_string(self, city=None, lat=None, lon=None):
        pass

    def __update_current_weather(self):
        URL = f'http://api.openweathermap.org/data/2.5/weather?q={self.city}&units=metric&appid={self.__api_key}&lang=de'
        self.current_weather = requests.get(URL).json()
        self.__last_updated = datetime.now()
        return self.__current_weather

    def __get_current_weather(self, city):
        URL = f'http://api.openweathermap.org/data/2.5/weather?q={self.city}&units=metric&appid={self.__api_key}&lang=de'
        self.current_weather = requests.get(URL).json()
        return self.__current_weather

    def __update_weather_forcast(self):
        URL = f'http://api.openweathermap.org/data/2.5/weather?q={self.city}&units=metric&appid={self.__api_key}&lang=de'
        self.current_weather = requests.get(URL).json()
        return self.__current_weather

    def __update_all(self):
        lat = self.__geo_data["lat"]
        lon = self.__geo_data["lon"]
        URL = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&appid={self.__api_key}&lang=de'

        if len(self.old_weather_inf) >= 10:
            self.old_weather_inf.pop(0)
        self.old_weather_inf.append(self.__hourly_forecast[0])

        weather_data = requests.get(URL).json()
        self.__current_weather = weather_data["current"]
        self.__minutely_forecast = weather_data["minutely"]
        self.__hourly_forecast = weather_data["hourly"]
        self.__daily_forcast = weather_data["daily"]
        self.__last_updated = datetime.now()

    def get_offset_minutes(self):
        timedelta = datetime.now() - self.__last_updated
        return timedelta.seconds / 60

    def get_offset_houres(self):
        timedelta = datetime.now() - self.__last_updated
        return timedelta.seconds / 3600

    def get_weather_in_web_json(self):
        return None

    class Statics:
        def __init__(self):
            pass

        # wird es ... geben
        will_be_description_map = {
            200: "ein Gewitter bei leichtem Regen",
            201: "ein regnerisches Gewitter",
            202: "ein Gewitter mit starkem Regen",
            210: "ein leichtes Gewitter geben",
            211: "ein stürmisches Gewitter geben",
            212: "ein starkes Gewitter geben",
            221: "ein sehr starkes Gewitter",
            230: "ein Gewitter mit leichtem Nieselregen",
            231: "ein Gewitter mit Nieselregen",
            232: "ein Gewitter mit starkem Nieselregen",
            300: "leichten Nieselregen",
            301: "Nieselregen",
            302: "starken Nieselregen",
            310: "Nieselregen",
            311: "Nieselregen",
            312: "starken Nieselregen",
            313: "Schauerregen",
            314: "starke Schauerregen",
            321: "Nieselschauer"
        }

        # gibt es
        give_description_map = {
            500: "leichten Regen",
            501: "mäßigen Regen",
            502: "starken Regen",
            503: "sehr starken Regen",
            504: "extremen Regen",
            511: "Eisregen",
            520: "leichte Regenschauer",
            521: "Regenschauer",
            522: "starke Regenschauer",
            531: "Regenschauer",
            600: "leichten Schnee",
            601: "Schnee",
            602: "starken Schnee",
            611: "Schneeregen",
            612: "Schneeregen",
            613: "Schneeregen",
            615: "leichten Regen und Schnee",
            616: "Regen und Schnee",
            620: "leichte Schneeschauer",
            621: "Schneeschauer",
            622: "starke Schneeschauer",
            731: "Staubaufwirbelungen",
            762: "Vulkanasche in der Luft",
            771: "Sturmböen",
            781: "einen Tornado",
            801: "ein paar Wolken",
            802: "vereinzelte Wolken",
            803: "vereinzelte Wolken"
        }

        # wird es
        will_description_map = {
            701: "neblig",
            711: "verraucht",
            721: "trüb",
            741: "neblig",
            751: "sandig",
            761: "staubig",
            804: "bewölkt"
        }
