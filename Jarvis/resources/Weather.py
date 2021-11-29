import requests


class Weather:
    def __init__(self, _api_key, _city, _skills):
        self.__api_key = _api_key
        self.__minutely_forecast = None
        self.__hourly_forecast = None
        self.__daily_forcast = None
        self.__sunrise_sunset = None
        self.__skills = _skills
        self.city = _city
        self.old_weather_inf = None
        self.current_weather = None

    def run(self):
        pass

    def get_current_weather(self, city_name=None, lat=None, lon=None):
        if city_name is None:
            return self.current_weather

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
        return self.__current_weather

    def __update_weather_forcast(self):
        URL = f'http://api.openweathermap.org/data/2.5/weather?q={self.city}&units=metric&appid={self.__api_key}&lang=de'
        self.current_weather = requests.get(URL).json()
        return self.__current_weather

    def __update_all(self):
        geo_data = self.__skills.get_data_of_city(self.city)
        lat = geo_data["lat"]
        lon = geo_data["lon"]
        URL = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&appid={self.__api_key}&lang=de'
        weather_data = requests.get(URL).json()
        self.__current_weather = weather_data["current"]
        self.__minutely_forecast = weather_data["minutely"]
        self.__hourly_forecast = weather_data["hourly"]
        self.__daily_forcast = weather_data["daily"]

    class Statics:
        def __init__(self):
            pass
