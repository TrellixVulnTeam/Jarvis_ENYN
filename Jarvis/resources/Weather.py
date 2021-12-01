import time
import requests
from datetime import datetime


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

    def run(self):
        while self.updating:
            self.__update_all()
            time.sleep(3600)

    def get_current_weather(self, city_name=None, lat=None, lon=None):
        if city_name is None:
            self.__update_all()
            return self.current_weather
        else:
            if city_name is not None:
                return self.get_current_weather(city_name=city_name)
            elif lat is not None and lon is not None:
                return self.get_current_weather(lat=lat, lon=lon)
            else:
                raise ValueError("Either name of the city or lat and lan are mandatory!")

    def get_forcast_of_one_day(self, day_offset, city_name=None, lat=None, lon=None):
        if day_offset > 7:
            raise ValueError("Day offset was higher than 7.")
        if city_name is None:
            return self.__daily_forcast[day_offset]
        else:
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

        if len(self.old_weather_inf) <= 10:
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
        return timedelta.seconds/60

    def get_offset_houres(self):
        timedelta = datetime.now() - self.__last_updated
        return timedelta.seconds / 3600

    class Statics:
        def __init__(self):
            pass
