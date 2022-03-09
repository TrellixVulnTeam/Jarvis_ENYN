import logging
from threading import Thread
from datetime import datetime
from datetime import timedelta
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
            url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly&appid={self.__api_key}&lang=de&units=metric'
            data = requests.get(url).json()
            return data["daily"][day_offset]

    def get_forcast_of_range(self, from_offset, until_offset, lat=None, lon=None):
        pass

    def get_sunrise_sunset(self, city_name=None, day_offset=0):
        if city_name is None:
            data = self.current_weather["sys"]
        else:
            url = f'api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={self.__api_key}&lang=de'
            data = requests.get(url).json()["sys"]
        return {data["sunrise"], data["sunset"]}

    def get_current_weather_string(self, city=None, lat=None, lon=None):
        _current_weather = self.get_current_weather(city, lat, lon)
        weather_id = _current_weather["weather"][0]["id"]
        weather_description = "Es gab leider ein Problem in der Analyse der Wetterdaten. Bitte versuche es zu einem " \
                              "späteren Zeitpunkt erneut! "
        temp_inf = f'bei {int(_current_weather["temp"])}°C'
        if city is None:
            city = self.city
        if weather_id in self.Statics.will_be_description_map.keys():
            weather_description = f'In {city} gibt es {self.Statics.will_be_description_map.get(weather_id)} {temp_inf}.'
        elif weather_id in self.Statics.give_description_map.keys():
            weather_description = f'In {city} gibt es {self.Statics.give_description_map.get(weather_id)} {temp_inf}.'
        elif weather_id in self.Statics.will_description_map.keys():
            weather_description = f'In {city} ist es {self.Statics.will_description_map.get(weather_id)} {temp_inf}.'
        return weather_description

    def get_hourly_forecast_string(self, city=None, lat=None, lon=None, offset=1):
        offset += self.get_offset_hours()
        if city is None and lat is None and lon is None:
            _forecast = self.__hourly_forecast[offset]
        if city is not None and city is not self.city:
            if offset > 47:
                raise ValueError('Offset too big! Choose an offset between 0 and 47')
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={self.__api_key}&lang=de'
            _forecast = requests.get(url).json()["hourly"][offset]
        weather_id = _forecast["weather"][0]["id"]
        weather_description = "Es gab leider ein Problem in der Analyse der Wetterdaten. Bitte versuche es zu einem " \
                              "späteren Zeitpunkt erneut! "
        temp_inf = f'bei {int(_forecast["temp"])}°C'
        if city is None:
            city = self.city
        if weather_id in self.Statics.will_be_description_map.keys():
            weather_description = f'In {city} wird es {self.__get_time_string(hours_offset=offset)} {self.Statics.will_be_description_map.get(weather_id)} {temp_inf} geben.'
        elif weather_id in self.Statics.give_description_map.keys():
            weather_description = f'In {city} wird es {self.__get_time_string(hours_offset=offset)} {self.Statics.give_description_map.get(weather_id)} {temp_inf} geben.'
        elif weather_id in self.Statics.will_description_map.keys():
            weather_description = f'In {city} wird es {self.__get_time_string(hours_offset=offset)} {self.Statics.will_description_map.get(weather_id)} {temp_inf}.'
        return weather_description

    def get_daily_forecast_string(self, city=None, lat=None, lon=None, offset=1):
        temp_offset = self.get_offset_hours()
        offset += temp_offset
        if temp_offset > 18:
            offset += 1
        # toDo
        pass

    def __update_current_weather(self):
        url = f'http://api.openweathermap.org/data/2.5/weather?q={self.city}&units=metric&appid={self.__api_key}&lang=de'
        self.current_weather = requests.get(url).json()
        self.__last_updated = datetime.now()
        return self.current_weather

    def __get_current_weather(self, city):
        url = f'http://api.openweathermap.org/data/2.5/weather?q={self.city}&units=metric&appid={self.__api_key}&lang=de'
        self.current_weather = requests.get(url).json()
        return self.current_weather

    def __update_weather_forcast(self):
        lat = self.__geo_data["lat"]
        lon = self.__geo_data["lon"]
        url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&appid={self.__api_key}&lang=de'
        _forecast = requests.get(url).json()
        # toDo
        return self.current_weather

    def __update_all(self):
        lat = self.__geo_data["lat"]
        lon = self.__geo_data["lon"]
        url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&appid={self.__api_key}&lang=de'

        if len(self.old_weather_inf) >= 10 and self.old_weather_inf:
            self.old_weather_inf.pop(0)
        if self.__hourly_forecast:
            self.old_weather_inf.append(self.__hourly_forecast[0])

        weather_data = requests.get(url).json()
        self.current_weather = weather_data["current"]
        self.__minutely_forecast = weather_data["minutely"]
        self.__hourly_forecast = weather_data["hourly"]
        self.__daily_forcast = weather_data["daily"]
        self.__last_updated = datetime.now()

    def __get_time_string(self, days_offset=0, hours_offset=0, minutes_offset=0):
        time_string: str = ''
        time = datetime.now() + timedelta(days=days_offset, hours=hours_offset, minutes=minutes_offset)
        time_difference = time - datetime.now()

        if time_difference.days == 1:
            time_string = 'morgen'
        elif time_difference.days == 2:
            time_string = 'übermorgen'
        elif time_difference.days != 0:
            return f'in {time_difference.days} Tagen'
        else:
            time_string = 'heute'

        if time.hour < 6:
            time_string += ' Nacht'
        elif time.hour < 12:
            time_string += ' Früh'
        elif time.hour < 17:
            time_string += ' Mittag'
        else:
            time_string += ' Abend'

        return time_string

    def get_weather_conditions(self):
        self.__update_all()
        now = datetime.now()
        output = ''
        if self.__minutely_forecast[0]['precipitation'] > 0:
            last_raining_index = 0
            for i in range(59):
                if self.__minutely_forecast[i]['precipitation'] > 0:
                    last_raining_index = i
            if last_raining_index < 15:
                output = f'Der Regen wird in etwa {last_raining_index} Minuten abgeklungen sein.'
            elif last_raining_index == 59:
                output = f'Nimm am besten einen Regenschirm mit. Der Regen dauert wahrscheinlich noch länger als eine Stunde an.'
        elif self.__minutely_forecast[0]['precipitation'] > 0:
            first_raining_index = 0
            for i in range(59):
                if self.__minutely_forecast[0]['precipitation'] > 0:
                    first_raining_index = i
                    break
            output = f'Es wird in etwa {first_raining_index} Minuten beginnen zu regnen. Nimm vielleicht einen Regenschirm mit.'

        max_uvi = 0

        for i in range(24 - now.hour):
            max_uvi = max(self.__hourly_forecast[i]['uvi'], max_uvi)

        if max_uvi >= 8:
            output += ' Creme dich unbedingt ein. Die Sonne scheint heute ziemlich stark.'
        elif max_uvi >= 6:
            output += ' Creme dich am besten ein. Die Sonne scheint heute stark.'
        elif max_uvi >= 4:
            output += ' Pass auf, die Sonne scheint heute mäßig stark. Villeicht solltest du dich eincremen.'

        return output

    def get_offset_minutes(self) -> int:
        delta = datetime.now() - self.__last_updated
        return int(delta.seconds / 60)

    def get_offset_hours(self) -> int:
        delta = datetime.now() - self.__last_updated
        offset: float = delta.seconds / 3600
        if delta.seconds % 3600 > 2700:
            offset += 1
        return int(offset)

    def get_weather_in_web_json(self):
        return None

    class Statics:
        def __init__(self):
            pass

        # wird es ... geben
        will_be_description_map = {
            200: "ein Gewitter bei leichtem Regen",
            201: "ein regnerisches Gewitter",
            202: "ein Gewitter bei starkem Regen",
            210: "ein leichtes Gewitter",
            211: "ein stürmisches Gewitter",
            212: "ein starkes Gewitter",
            221: "ein sehr starkes Gewitter",
            230: "ein Gewitter bei leichtem Nieselregen",
            231: "ein Gewitter bei Nieselregen",
            232: "ein Gewitter bei starkem Nieselregen",
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
            800: "klar",
            804: "bewölkt"
        }


if __name__ == "__main__":
    from src.speechassistant.resources.module_skills import Skills

    w = Weather('bd4d17c6eedcff6efc70b9cefda99082', 'Würzburg', Skills())
    th = Thread(target=w.run, args=())
    th.start()
    time.sleep(2)
    print(w.get_hourly_forecast_string(offset=12))
    print(w.get_hourly_forecast_string(offset=0))
    print(w.get_hourly_forecast_string(offset=1))
    print(w.get_hourly_forecast_string(offset=5))
    print(w.get_hourly_forecast_string(offset=24))
    print(w.get_hourly_forecast_string(offset=29))
    print(w.get_hourly_forecast_string(offset=40))
